"""cascade

Revision ID: 958ccbb08883
Revises: a2a2022e7955
Create Date: 2023-03-17 09:59:12.244374

"""
from alembic import op
import sqlalchemy as sa
import databases


# revision identifiers, used by Alembic.
revision = '958ccbb08883'
down_revision = 'a2a2022e7955'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('questions_quizz_id_fkey', 'questions', type_='foreignkey')
    op.create_foreign_key(None, 'questions', 'quizzes', ['quizz_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('quizzes_company_id_fkey', 'quizzes', type_='foreignkey')
    op.create_foreign_key(None, 'quizzes', 'companies', ['company_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'quizzes', type_='foreignkey')
    op.create_foreign_key('quizzes_company_id_fkey', 'quizzes', 'companies', ['company_id'], ['id'])
    op.drop_constraint(None, 'questions', type_='foreignkey')
    op.create_foreign_key('questions_quizz_id_fkey', 'questions', 'quizzes', ['quizz_id'], ['id'])
    # ### end Alembic commands ###
