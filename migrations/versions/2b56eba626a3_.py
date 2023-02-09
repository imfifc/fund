"""empty message

Revision ID: 2b56eba626a3
Revises: 
Create Date: 2023-02-09 01:30:05.425450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b56eba626a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dayGrowRate',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('dayGrowRate', sa.Float(), nullable=True),
    sa.Column('date', sa.String(length=30), nullable=True),
    sa.Column('create_time', sa.DATETIME(timezone=6), nullable=True),
    sa.Column('update_time', sa.DATETIME(timezone=6), nullable=True),
    sa.Column('is_delete', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dayGrowRate_create_time'), 'dayGrowRate', ['create_time'], unique=False)
    op.create_table('last1month',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('last1month', sa.Float(), nullable=True),
    sa.Column('date', sa.String(length=30), nullable=True),
    sa.Column('create_time', sa.DATETIME(timezone=6), nullable=True),
    sa.Column('update_time', sa.DATETIME(timezone=6), nullable=True),
    sa.Column('is_delete', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_last1month_create_time'), 'last1month', ['create_time'], unique=False)
    op.create_table('last1week',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('last1week', sa.Float(), nullable=True),
    sa.Column('date', sa.String(length=30), nullable=True),
    sa.Column('create_time', sa.DATETIME(timezone=6), nullable=True),
    sa.Column('update_time', sa.DATETIME(timezone=6), nullable=True),
    sa.Column('is_delete', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_last1week_create_time'), 'last1week', ['create_time'], unique=False)
    op.create_table('last1year',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('last1year', sa.Float(), nullable=True),
    sa.Column('date', sa.String(length=30), nullable=True),
    sa.Column('create_time', sa.DATETIME(timezone=6), nullable=True),
    sa.Column('update_time', sa.DATETIME(timezone=6), nullable=True),
    sa.Column('is_delete', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_last1year_create_time'), 'last1year', ['create_time'], unique=False)
    op.create_table('last6month',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('last6month', sa.Float(), nullable=True),
    sa.Column('date', sa.String(length=30), nullable=True),
    sa.Column('create_time', sa.DATETIME(timezone=6), nullable=True),
    sa.Column('update_time', sa.DATETIME(timezone=6), nullable=True),
    sa.Column('is_delete', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_last6month_create_time'), 'last6month', ['create_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_last6month_create_time'), table_name='last6month')
    op.drop_table('last6month')
    op.drop_index(op.f('ix_last1year_create_time'), table_name='last1year')
    op.drop_table('last1year')
    op.drop_index(op.f('ix_last1week_create_time'), table_name='last1week')
    op.drop_table('last1week')
    op.drop_index(op.f('ix_last1month_create_time'), table_name='last1month')
    op.drop_table('last1month')
    op.drop_index(op.f('ix_dayGrowRate_create_time'), table_name='dayGrowRate')
    op.drop_table('dayGrowRate')
    # ### end Alembic commands ###
