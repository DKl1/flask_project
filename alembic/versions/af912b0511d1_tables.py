"""tables

Revision ID: af912b0511d1
Revises: 
Create Date: 2022-11-10 23:13:22.205002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af912b0511d1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer, nullable = False),
    sa.Column('full_name', sa.String, nullable = False),
    sa.Column('username', sa.String, nullable = False),
    sa.Column('password', sa.String, nullable = False),
    sa.PrimaryKeyConstraint('admin_id')
    )
    op.create_table('room',
    sa.Column('room_number', sa.String, nullable = False),
    sa.Column('people', sa.Integer, nullable = False),
    sa.Column('type', sa.Enum('econom', 'comfort', 'comfort+', 'luxe', name='Type'), nullable = False),
    sa.Column('price', sa.Integer, nullable = False),
    sa.Column('reserved', sa.Boolean, nullable = False),
    sa.Column('description', sa.String, nullable = False),
    sa.Column('photo', sa.String, nullable = True),
    sa.Column('beds', sa.Integer, nullable = True),
    sa.ForeignKeyConstraint(['reserved'], ['reserved.status']),
    sa.PrimaryKeyConstraint('room_number')
    )
    op.create_table('reservation',
    sa.Column('reservation_id', sa.Integer, nullable = False),
    sa.Column('full_name', sa.String, nullable = False),
    sa.Column('phone', sa.String, nullable = False),
    sa.Column('date_from', sa.String, nullable = False),
    sa.Column('date_to', sa.String, nullable = False),
    sa.ForeignKeyConstraint(['room_number'], ['room.room_number']),
    sa.PrimaryKeyConstraint('reservation_id')
    )
    op.create_table('reserved',
    sa.Column('status', sa.Boolean, nullable = False),
    sa.Column('room_number', sa.String, nullable = False),
    sa.Column('date_from', sa.String, nullable = False),
    sa.Column('date_to', sa.String, nullable = False),
    sa.ForeignKeyConstraint(['room_number'], ['room.room_number']),
    sa.ForeignKeyConstraint(['date_from'], ['reservation.date_from']),
    sa.ForeignKeyConstraint(['date_to'], ['reservation.date_to'])
    )


def downgrade() -> None:
    op.drop_table('admin')
    op.drop_table('room')
    op.drop_table('reservation')
    op.drop_table('reserved')
