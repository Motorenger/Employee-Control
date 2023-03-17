from fastapi import HTTPException

from databases import Database

from services.company_logic import CompanyService
from db.models import companies, quizzes, questions, answers
from schemas.quizz_schemas import QuizzCreate, QuizzEdit, Quizz
from schemas.user_schemas import User


class QuizzService(CompanyService):
    def __init__(self, db: Database, current_user: User | None = None):
        super().__init__(db=db, current_user=current_user)
        self.quizzes = quizzes
        self.questions = questions
        self.answers = answers


    async def create_quizz(self, company_id: int, quizz_data: QuizzCreate):
        await self.check_for_existing(company_id=company_id, check_owner_admin=True)

        quizz_d = {"title": quizz_data.title,
                   "description": quizz_data.description,
                   "pass_freq": quizz_data.pass_freq,
                   "company_id":company_id
                  }

        query = self.quizzes.insert().returning(self.quizzes.c.id)
        quizz_id = await self.db.execute(query=query, values=quizz_d)
        for question in quizz_data.questions:
            question_d = {
                    "title": question.title,
                    "correct_answer": question.correct_answer,
                    "quizz_id": quizz_id
                }
            query = self.questions.insert().returning(self.questions.c.id)
            question_id = await self.db.execute(query=query, values=question_d)
            answers_d = [ 
                {
                    "answer": answer.answer,
                    "question_id": question_id

                }
                for answer in question.answers
            ]

            query = self.answers.insert()
            await self.db.execute_many(query=query, values=answers_d)

        return await self.db.fetch_all(query=self.quizzes.select())

    async def delete_quizz(self, company_id: int, quizz_id: int):
        await self.check_for_existing(company_id=company_id, check_owner_admin=True)

        query = self.quizzes.delete().where(self.quizzes.c.id == quizz_id)
        await self.db.execute(query=query)

    async def update_company(self, company_id: int, quizz_id: int, quizz_data: QuizzEdit) -> Quizz:
        await self.check_for_existing(company_id=company_id, check_owner_admin=True)

        update_data = {field:value for field, value in quizz_data.dict().items() if value is not None}
        
        query = self.quizzes.update().where(self.quizzes.c.id == quizz_id).values(**update_data)
        await self.db.execute(query)

        query = self.quizzes.select().where(self.quizzes.c.id == quizz_id)
        quizz = await self.db.fetch_one(query=query)
        return Quizz(**quizz)
