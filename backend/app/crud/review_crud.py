from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import ReviewNotAllowedError
from models import Review
from schemas.review_scheme import ReviewRequestScheme, ReviewScheme


async def create(review_create: ReviewRequestScheme, user_id, db: AsyncSession) -> ReviewScheme:
    review = Review(
        user_id=user_id,
        trip_id=review_create.trip_id,
        score=review_create.score,
        text=review_create.text
    )

    try:

        db.add(review)
        await db.commit()
        await db.refresh(review)

        review_scheme: ReviewScheme = ReviewScheme(**review.__dict__)

        return review_scheme

    except IntegrityError as e:
        raise ValueError(str(e))


async def get(review_id, db: AsyncSession) -> ReviewScheme:
    query = select(Review).where(Review.review_id == review_id)
    result = await db.execute(query)

    review = result.scalars().first()

    if not review:
        raise ValueError(f"No review with id {review_id}")

    review_scheme: ReviewScheme = ReviewScheme(**review.__dict__)

    return review_scheme


async def get_user_score(user_id: int, db: AsyncSession) -> float:
    query = select(func.avg(Review.score)).where(Review.user_id == int(user_id))
    try:
        result = await db.execute(query)
        avg_score = result.scalar()

        if avg_score is None:
            return 5.0

        return avg_score

    except IntegrityError as e:
        raise ReviewNotAllowedError(str(e))
