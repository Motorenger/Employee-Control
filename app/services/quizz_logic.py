from datetime import datetime

from databases import Database

from services.company_logic import CompanyService
from db.models import questions, answers, records, users
from schemas.quizz_schemas import (QuizzCreate, QuizzEdit,
                                   Quizz, Questsion,
                                   QuestionList, QuizzFull,
                                   QuizzData)
from schemas.user_schemas import User


class QuizzService(CompanyService):
    def __init__(self, db: Database, current_user: User | None = None):
        super().__init__(db=db, current_user=current_user)
        self.questions = questions
        self.answers = answers
        self.records = records
        self.users = users

    async def create_questions(self, questions):
        for question in questions:
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

    async def create_quizz(self, company_id: int, quizz_data: QuizzCreate) -> Quizz:
        await self.check_for_existing(company_id=company_id, check_owner_admin=True)

        quizz_d = {"title": quizz_data.title,
                   "description": quizz_data.description,
                   "pass_freq": quizz_data.pass_freq,
                   "company_id":company_id,
                   "created_at": datetime.now(),
                   "created_by": self.current_user.id
                  }

        query = self.quizzes.insert().returning(self.quizzes.c.id)
        quizz_id = await self.db.execute(query=query, values=quizz_d)
        await self.create_questions(questions=quizz_data.questions)

        return Quizz(**await self.db.fetch_one(query=self.quizzes.select().where(self.quizzes.c.id == quizz_id)))

    async def delete_quizz(self, company_id: int, quizz_id: int):
        await self.check_for_existing(company_id=company_id, check_owner_admin=True)

        query = self.quizzes.delete().where(self.quizzes.c.id == quizz_id)
        await self.db.execute(query=query)

    async def update_quizz(self, company_id: int, quizz_id: int, quizz_data: QuizzEdit) -> Quizz:
        await self.check_for_existing(company_id=company_id, check_owner_admin=True)

        update_data = {field:value for field, value in quizz_data.dict().items() if value is not None}
        update_data["updated_at"] = datetime.now()
        update_data["updated_by"] = self.current_user.id
        query = self.quizzes.update().where(self.quizzes.c.id == quizz_id).values(**update_data)
        await self.db.execute(query)

        query = self.quizzes.select().where(self.quizzes.c.id == quizz_id)
        quizz = await self.db.fetch_one(query=query)
        return Quizz(**quizz)

    async def retrieve_quizz(self, company_id: int, quizz_id: int):
        await self.check_for_existing(company_id=company_id)

        query = self.quizzes.select().where(self.quizzes.c.id == quizz_id)
        quizz = await self.db.fetch_one(query=query)

        query = self.questions.select()
        questions = await self.db.fetch_all(query=query)

        questsions = []
        for question in questions:
            answers = []
            query = self.answers.select().where(self.answers.c.question_id == question.id)
            answers = await self.db.fetch_all(query=query)
            questsions.append(Questsion(**question, answers=answers))

        return QuizzFull(**quizz, questions=questsions)

    async def pass_quizz(self, company_id: int, quizz_id: int, quizz_data: QuizzData):
        quizz = await self.retrieve_quizz(company_id=company_id, quizz_id=quizz_id)
        questions_amount = len(quizz.questions)
        record = {
            "user_id": self.current_user.id,
            "company_id": company_id,
            "quizz_id": quizz_id,
            "created_at": datetime.now().date(),
            "questions": questions_amount,
            }
        correct = 0
        for quest_numb, question in enumerate(quizz_data.questions):
            for question_core in quizz.questions:
                if question.question_id == question_core.id and question.answer == question_core.correct_answer:
                    correct += 1
        record["correct"] = correct
        if correct == questions_amount:
            record["average_result"] = 10.0
        else:
            record["average_result"] = (correct / questions_amount) * 10

        query = self.records.insert().returning(self.records.c.average_result)
        average_result = await self.db.execute(query=query, values=record)

        user_data = {
            "questions": self.current_user.questions + questions_amount,
            "correct": self.current_user.correct + correct
        }
        query = self.users.update().values(**user_data)
        await self.db.execute(query=query)

        query = self.company_members.select().where(
                                                self.company_members.c.company_id == company_id
                                                ).where(self.company_members.c.user_id == self.current_user.id)
        member = await self.db.fetch_one(query=query)
        if member:
            member_data = {
                "questions": member["questions"] + questions_amount,
                "answers": member["correct"] + correct
            }
            query = self.company_members.update().values(**member_data)
            await self.db.execute(query=query)

        return average_result
