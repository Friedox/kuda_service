"""Add trip <--> car relation, reformat responsibilities

Revision ID: e199ffd56f59
Revises: 16bdf085ca01
Create Date: 2024-08-11 14:20:02.975388

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e199ffd56f59"
down_revision: Union[str, None] = "16bdf085ca01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "car_trip",
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("car_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["car_id"], ["car.car_id"], name=op.f("fk_car_trip_car_id_car")
        ),
        sa.ForeignKeyConstraint(
            ["trip_id"],
            ["trip.trip_id"],
            name=op.f("fk_car_trip_trip_id_trip"),
        ),
        sa.PrimaryKeyConstraint("trip_id", "car_id", name=op.f("pk_car_trip")),
    )
    op.drop_column("trip", "car_type")
    op.drop_column("trip", "driver_tg")
    op.drop_column("trip", "car_number")
    op.drop_column("trip", "driver_phone")


def downgrade() -> None:
    op.add_column(
        "trip",
        sa.Column(
            "driver_phone", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "trip",
        sa.Column(
            "car_number", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "trip",
        sa.Column(
            "driver_tg", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "trip",
        sa.Column(
            "car_type", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
    )
    op.drop_table("car_trip")
