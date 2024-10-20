from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'efa285a0052d'
down_revision = '82bc1489986e'
branch_labels = None
depends_on = None


def upgrade():
    # Creación de nuevas tablas
    op.create_table('character',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=200), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('planet_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['planet_id'], ['planet.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table('fav',
        sa.Column('id_user', sa.Integer(), nullable=False),
        sa.Column('id_character', sa.Integer(), nullable=False),
        sa.Column('id_planet', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id_character'], ['character.id']),
        sa.ForeignKeyConstraint(['id_planet'], ['planet.id']),
        sa.ForeignKeyConstraint(['id_user'], ['user.id']),
        sa.PrimaryKeyConstraint('id_user', 'id_character', 'id_planet')
    )

    # Eliminar tablas obsoletas
    op.drop_table('favorites')
    op.drop_table('people')

    # Alteración de la tabla planet
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=200), nullable=True))
        batch_op.alter_column('name', existing_type=sa.VARCHAR(length=120), type_=sa.String(length=50), existing_nullable=False)
        batch_op.create_unique_constraint(None, ['name'])
        batch_op.drop_column('diameter')
        batch_op.drop_column('gravity')
        # Otras columnas eliminadas...

    # Alteración de la tabla user
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firstname', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('lastname', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('address', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('phone', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('date', sa.Date(), nullable=True))
        batch_op.alter_column('username', existing_type=sa.VARCHAR(length=80), type_=sa.String(length=50), existing_nullable=False)
        batch_op.alter_column('email', existing_type=sa.VARCHAR(length=80), type_=sa.String(length=50), existing_nullable=False)
        batch_op.alter_column('password', existing_type=sa.VARCHAR(length=80), type_=sa.String(length=50), existing_nullable=False)
        batch_op.create_unique_constraint(None, ['date'])
        batch_op.drop_column('is_active')


def downgrade():
    # Revertir cambios en user
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('password', existing_type=sa.String(length=50), type_=sa.VARCHAR(length=80), existing_nullable=False)
        batch_op.alter_column('email', existing_type=sa.String(length=50), type_=sa.VARCHAR(length=80), existing_nullable=False)
        batch_op.alter_column('username', existing_type=sa.String(length=50), type_=sa.VARCHAR(length=80), existing_nullable=False)
        batch_op.drop_column('date')
        # Otras columnas revertidas...

    # Revertir cambios en planet
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('climate', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('population', sa.INTEGER(), autoincrement=False, nullable=True))
        # Otras columnas revertidas...

    # Recrear tablas eliminadas
    op.create_table('people', ...)
    op.create_table('favorites', ...)
