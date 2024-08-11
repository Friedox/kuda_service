"""Add message model

Revision ID: e78e84cb6a21
Revises: 2fa2b807d646
Create Date: 2024-08-02 12:36:20.214516

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e78e84cb6a21"
down_revision: Union[str, None] = "2fa2b807d646"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "message",
        sa.Column(
            "message_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("message_id", name=op.f("pk_message")),
    )
    op.create_index(
        op.f("ix_message_message_id"), "message", ["message_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_message_message_id"), table_name="message")
    op.drop_table("message")
