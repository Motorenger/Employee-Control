from datetime import datetime

from pydantic import BaseModel, conlist


class AnswerCreate(BaseModel):
    answer: str


class QuestionCreate(BaseModel):
    title: str
    correct_answer: int
    answers: dict[int, AnswerCreate]


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


class Answer(AnswerCreate):
    question_id: int


class Question(QuestionCreate):
    id: int

class QuestionList(BaseModel):
    questions: list[Question]


class QuizzFull(QuizzCreate):
    id: int
    questions: list[Question]


class QuestionData(BaseModel):
    answer: int


class QuizzData(BaseModel):
    questions: dict[int, QuestionData]
