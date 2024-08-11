"""Add car model

Revision ID: f829d11668c9
Revises: 8d59bd7839d0
Create Date: 2024-08-10 16:39:59.754918

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f829d11668c9"
down_revision: Union[str, None] = "8d59bd7839d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "car",
        sa.Column("car_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("model", sa.String(), nullable=False),
        sa.Column("number", sa.String(), nullable=False),
        sa.Column("region_number", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("car_id", name=op.f("pk_car")),
    )
    op.create_index(op.f("ix_car_car_id"), "car", ["car_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_car_car_id"), table_name="car")
    op.drop_table("car")
