"""empty message

Revision ID: 59b7f6df42e7
Revises: 27aa2ed76deb
Create Date: 2022-11-11 10:44:23.021585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59b7f6df42e7'
down_revision = '27aa2ed76deb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('password', sa.String(length=225), nullable=False),
    sa.PrimaryKeyConstraint('admin_id')
    )
    op.create_table('room',
    sa.Column('room_number', sa.String(length=3), nullable=False),
    sa.Column('people', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('economy', 'comfort', 'comfortplus', 'luxe', name='type'), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=False),
    sa.Column('photo_url', sa.String(length=120), nullable=True),
    sa.Column('bed_n', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('room_number')
    )
    op.create_table('reservation',
    sa.Column('reservation_id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=13), nullable=False),
    sa.Column('date_from', sa.Date(), nullable=False),
    sa.Column('date_to', sa.Date(), nullable=False),
    sa.Column('id_room', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['id_room'], ['room.room_number'], ),
    sa.PrimaryKeyConstraint('reservation_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservation')
    op.drop_table('room')
    op.drop_table('admin')
    # ### end Alembic commands ###