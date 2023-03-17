from datetime import datetime

from pydantic import BaseModel, conlist


class AnswerCreate(BaseModel):
    answer: str


class QuestionCreate(BaseModel):
    title: str
    correct_answer: int
    answers: conlist(AnswerCreate, min_items=2)


class QuizzCreate(BaseModel):
    title: str
    description: str | None = None
    pass_freq: int
    questions: conlist(QuestionCreate, min_items=2)


class Quizz(BaseModel):
    id: int
    title: str
    description: str | None = None
    pass_freq: int
    created_at: datetime
    updated_at: datetime | None = None
    created_by: int
    updated_by: int | None = None

class QuizzEdit(BaseModel):
    title: str | None = None
    description: str | None = None
    pass_freq: int | None = None


class QuizzList(BaseModel):
    quizzes: list[Quizz]