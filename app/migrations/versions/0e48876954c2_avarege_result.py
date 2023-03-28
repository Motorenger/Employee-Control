"""avarege_result

Revision ID: 0e48876954c2
Revises: 33877d82ab2d
Create Date: 2023-03-27 09:13:41.113406

"""
from alembic import op
import sqlalchemy as sa
import databases
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0e48876954c2'
down_revision = '33877d82ab2d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('records', sa.Column('record_average_result', sa.Float(), nullable=True))
    op.add_column('records', sa.Column('user_average_result', sa.Float(), nullable=True))
    op.drop_column('records', 'average_result')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('records', sa.Column('average_result', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('records', 'user_average_result')
    op.drop_column('records', 'record_average_result')
    # ### end Alembic commands ###
