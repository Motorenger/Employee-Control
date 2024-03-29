"""quizz fields

Revision ID: 3756bd33b69a
Revises: 3682b1727b8c
Create Date: 2023-03-17 12:38:27.408776

"""
from alembic import op
import sqlalchemy as sa
import databases


# revision identifiers, used by Alembic.
revision = '3756bd33b69a'
down_revision = '3682b1727b8c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quizzes', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('quizzes', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('quizzes', sa.Column('created_by', sa.Integer(), nullable=False))
    op.add_column('quizzes', sa.Column('updated_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'quizzes', 'users', ['updated_by'], ['id'])
    op.create_foreign_key(None, 'quizzes', 'users', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'quizzes', type_='foreignkey')
    op.drop_constraint(None, 'quizzes', type_='foreignkey')
    op.drop_column('quizzes', 'updated_by')
    op.drop_column('quizzes', 'created_by')
    op.drop_column('quizzes', 'updated_at')
    op.drop_column('quizzes', 'created_at')
    # ### end Alembic commands ###
