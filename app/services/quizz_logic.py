from datetime import datetime

from databases import Database

from fastapi import HTTPException

from services.company_logic import CompanyService
from db.models import questions, records, users, company_members, notifications
from schemas.quizz_schemas import (
    QuizzCreate,
    QuizzEdit,
    Quizz,
    Question,
    QuestionList,
    QuizzFull,
    QuizzData,
)
from schemas.records_schemas import Record
from schemas.user_schemas import User


class QuizzService(CompanyService):
    def __init__(self, db: Database, current_user: User | None = None):
        super().__init__(db=db, current_user=current_user)
        self.questions = questions
        self.records = records
        self.users = users
        self.company_members = company_members
        self.notifications = notifications

    async def create_questions(self, question, quizz_id: int, question_numb: int):
        if len(question.answers) < 2:
            raise HTTPException(status_code=422, detail="At least 2 answers")
        question_d = {
            "title": question.title,
            "question_numb": question_numb + 1,
            "correct_answer": question.correct_answer,
            "quizz_id": quizz_id,
            "answers": {key: value.dict() for key, value in question.answers.items()},
        }
        query = self.questions.insert()
        await self.db.execute(query=query, values=question_d)

    async def create_quizz(self, company_id: int, quizz_data: QuizzCreate) -> Quizz:
        await self.check_for_existing(company_id=company_id, check_owner_admin=True)

        quizz_d = {
            "title": quizz_data.title,
            "description": quizz_data.description,
            "pass_freq": quizz_data.pass_freq,
            "company_id": company_id,
            "created_at": datetime.now(),
            "created_by": self.current_user.id,
        }

        query = self.quizzes.insert().returning(self.quizzes.c.id)
        quizz_id = await self.db.execute(query=query, values=quizz_d)
        for question_numb, question in enumerate(quizz_data.questions):
            await self.create_questions(
                question=question, quizz_id=quizz_id, question_numb=question_numb
            )

        query = self.company_members.select().where(
            self.company_members.c.company_id == company_id
        )
        members = await self.db.fetch_all(query=query)

        notification_d = {
            "time": datetime.now(),
            "message": "New quizz!!!",
            "status": False,
        }
        for member in members:
            notification_d["user_id"] = member.user_id
            query = self.notifications.insert()
            await self.db.execute(query=query, values=notification_d)

        return Quizz(
            **await self.db.fetch_one(
                query=self.quizzes.select().where(self.quizzes.c.id == quizz_id)
            )
        )

    async def delete_quizz(self, company_id: int, quizz_id: int):
        await self.check_for_existing(company_id=company_id, check_owner_admin=True)

        query = self.quizzes.delete().where(self.quizzes.c.id == quizz_id)
        await self.db.execute(query=query)

    async def update_quizz(
        self, company_id: int, quizz_id: int, quizz_data: QuizzEdit
    ) -> Quizz:
        await self.check_for_existing(company_id=company_id, check_owner_admin=True)

        update_data = {
            field: value
            for field, value in quizz_data.dict().items()
            if value is not None
        }
        update_data["updated_at"] = datetime.now()
        update_data["updated_by"] = self.current_user.id
        query = (
            self.quizzes.update()
            .where(self.quizzes.c.id == quizz_id)
            .values(**update_data)
        )
        await self.db.execute(query=query)

        query = self.quizzes.select().where(self.quizzes.c.id == quizz_id)
        quizz = await self.db.fetch_one(query=query)
        return Quizz(**quizz)

    async def retrieve_quizz(self, company_id: int, quizz_id: int) -> QuestionList:
        await self.check_for_existing(company_id=company_id)

        query = self.questions.select().where(self.questions.c.quizz_id == quizz_id)
        questions = await self.db.fetch_all(query=query)

        questions_d = [Question(**question) for question in questions]
        return QuestionList(questions=questions_d)

    async def pass_quizz(
        self, company_id: int, quizz_id: int, quizz_data: QuizzData
    ) -> Record:
        quizz = await self.retrieve_quizz(company_id=company_id, quizz_id=quizz_id)
        questions_amount = len(quizz.questions)
        if questions_amount < 2:
            raise HTTPException(status_code=404, detail="Quizz not found")
        record = {
            "user_id": self.current_user.id,
            "company_id": company_id,
            "quizz_id": quizz_id,
            "created_at": datetime.now().date(),
            "questions": questions_amount,
        }
        correct = 0
        for question_core in quizz.questions:
            questions_dict = quizz_data.questions
            if (
                question_core.question_numb in questions_dict.keys()
                and questions_dict.get(question_core.question_numb).answer
                == question_core.correct_answer
            ):
                correct += 1
        record["correct"] = correct
        record["record_average_result"] = (correct / questions_amount) * 10
        record["user_average_result"] = (
            (self.current_user.correct + correct)
            / (self.current_user.questions + questions_amount)
        ) * 10

        query = self.records.insert().returning(self.records.c.id)
        record_id = await self.db.execute(query=query, values=record)

        user_data = {
            "questions": self.current_user.questions + questions_amount,
            "correct": self.current_user.correct + correct,
        }
        query = self.users.update().values(**user_data)
        await self.db.execute(query=query)

        query = (
            self.company_members.select()
            .where(self.company_members.c.company_id == company_id)
            .where(self.company_members.c.user_id == self.current_user.id)
        )
        member = await self.db.fetch_one(query=query)
        if member:
            member_data = {
                "questions": member["questions"] + questions_amount,
                "correct": member["correct"] + correct,
            }
            query = self.company_members.update().values(**member_data)
            await self.db.execute(query=query)

        query = self.records.select().where(self.records.c.id == record_id)
        record = await self.db.fetch_one(query=query)
        return Record(**record)
