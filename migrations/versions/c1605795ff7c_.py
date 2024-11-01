"""empty message

Revision ID: c1605795ff7c
Revises: 86cd20c6454f
Create Date: 2024-10-20 19:44:06.035568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1605795ff7c'
down_revision = '86cd20c6454f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('favoriteplanets')
    op.drop_table('favoritevehicles')
    op.drop_table('favoritecharacters')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favoritecharacters',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='favoritecharacters_character_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='favoritecharacters_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favoritecharacters_pkey')
    )
    op.create_table('favoritevehicles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('vehicle_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='favoritevehicles_user_id_fkey'),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], name='favoritevehicles_vehicle_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favoritevehicles_pkey')
    )
    op.create_table('favoriteplanets',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], name='favoriteplanets_planet_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='favoriteplanets_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favoriteplanets_pkey')
    )
    op.drop_table('favorite_vehicles')
    op.drop_table('favorite_planets')
    op.drop_table('favorite_characters')
    # ### end Alembic commands ###
