"""fixes

Revision ID: c2d1512dd510
Revises: 1853e4cbbe65
Create Date: 2023-03-11 09:49:58.508177

"""
from alembic import op
import sqlalchemy as sa
import databases


# revision identifiers, used by Alembic.
revision = 'c2d1512dd510'
down_revision = '1853e4cbbe65'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company_members',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('compnay_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['compnay_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.drop_table('company_users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company_users',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('compnay_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['compnay_id'], ['companies.id'], name='company_users_compnay_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='company_users_user_id_fkey')
    )
    op.drop_table('company_members')
    # ### end Alembic commands ###