"""Add phone and telegram fields to User model

Revision ID: 8d59bd7839d0
Revises: 07d4b667e97d
Create Date: 2024-08-10 15:10:32.757514

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8d59bd7839d0"
down_revision: Union[str, None] = "07d4b667e97d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user", sa.Column("telegram", sa.String(), nullable=True))
    op.add_column("user", sa.Column("phone", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("user", "phone")
    op.drop_column("user", "telegram")
