"""empty message

Revision ID: 1e2904b7219b
Revises: None
Create Date: 2016-06-23 00:26:06.138503

"""

# revision identifiers, used by Alembic.
revision = '1e2904b7219b'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('facility',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('facility_name', sa.String(length=64), nullable=True),
    sa.Column('facility_description', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_facility_facility_description'), 'facility', ['facility_description'], unique=True)
    op.create_index(op.f('ix_facility_facility_name'), 'facility', ['facility_name'], unique=True)
    op.create_table('repairpersons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('message', sa.String(length=120), nullable=True),
    sa.Column('phone_no', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_no')
    )
    op.create_index(op.f('ix_repairpersons_name'), 'repairpersons', ['name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_repairperson', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('repairs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('facility_id', sa.Integer(), nullable=False),
    sa.Column('requested_by_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('resolved', sa.Boolean(), nullable=True),
    sa.Column('acknowledged', sa.Boolean(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('progress', sa.Integer(), nullable=True),
    sa.Column('date_requested', sa.DateTime(), nullable=True),
    sa.Column('date_completed', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['facility_id'], ['facility.id'], ),
    sa.ForeignKeyConstraint(['requested_by_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_repairs_date_requested'), 'repairs', ['date_requested'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_repairs_date_requested'), table_name='repairs')
    op.drop_table('repairs')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_repairpersons_name'), table_name='repairpersons')
    op.drop_table('repairpersons')
    op.drop_index(op.f('ix_facility_facility_name'), table_name='facility')
    op.drop_index(op.f('ix_facility_facility_description'), table_name='facility')
    op.drop_table('facility')
    ### end Alembic commands ###
