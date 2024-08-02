from datetime import datetime, UTC
from typing import List, Dict

from fastapi import (
    APIRouter,
    WebSocketDisconnect,
    HTTPException,
    Depends,
    WebSocket, Query,
)
from sqlalchemy.ext.asyncio import AsyncSession

from crud import trip_user_crud, message_crud
from models import database_helper
from schemas.message_scheme import SendMessageScheme, MessageScheme
from schemas.user_scheme import UserScheme
from services import auth_service

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, chat_id: str, websocket: WebSocket):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, chat_id: str, websocket: WebSocket):
        self.active_connections[chat_id].remove(websocket)
        if not self.active_connections[chat_id]:
            del self.active_connections[chat_id]

    async def broadcast(self, chat_id: str, message: str):
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                await connection.send_text(message)


manager = ConnectionManager()


async def verify_access(chat_id: str, user: UserScheme, db):
    user_trips = await trip_user_crud.get_user_trips(user, db)
    trip_ids = [trip.trip_id for trip in user_trips]
    if int(chat_id) not in trip_ids:
        raise HTTPException(status_code=403, detail="User has no permissions")


@router.websocket("/{chat_id}")
async def websocket_endpoint(
        *,
        websocket: WebSocket,
        chat_id: str,
        db: AsyncSession = Depends(database_helper.session_getter),
        limit: int = Query(100, alias="limit"),
        offset: int = Query(0, alias="offset")
):
    try:
        user = await auth_service.get_user_from_session_id(websocket, db)
        await verify_access(chat_id, user, db)
        await manager.connect(chat_id, websocket)

        old_messages = await message_crud.get_chat_messages(db, int(chat_id), limit=limit, offset=offset)
        for message in reversed(old_messages):
            await websocket.send_text(f"{message.user_id}: {message.json()}")

        try:
            while True:
                text = await websocket.receive_text()
                message_scheme = MessageScheme(
                    user_id=user.user_id,
                    chat_id=int(chat_id),
                    message=text,
                    timestamp=datetime.now().replace(tzinfo=None)
                )

                message = await message_crud.save_message(message_scheme, db)

                message_send = SendMessageScheme(
                    **message.dict(),
                    username=user.username
                )

                await manager.broadcast(chat_id, f"{user.user_id}: {message_send.json()}")
        except WebSocketDisconnect:
            manager.disconnect(chat_id, websocket)
    except HTTPException as e:
        print(str(e))
        await websocket.close(code=e.status_code, reason=e.detail)
    except Exception as e:
        print(str(e))
        await websocket.close(code=400, reason=str(e))
