"""Add user <--> car relation

Revision ID: 16bdf085ca01
Revises: f829d11668c9
Create Date: 2024-08-11 11:26:27.769679

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "16bdf085ca01"
down_revision: Union[str, None] = "f829d11668c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_car",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("car_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["car_id"], ["car.car_id"], name=op.f("fk_user_car_car_id_car")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.user_id"],
            name=op.f("fk_user_car_user_id_user"),
        ),
        sa.PrimaryKeyConstraint("user_id", "car_id", name=op.f("pk_user_car")),
    )


def downgrade() -> None:
    op.drop_table("user_car")
