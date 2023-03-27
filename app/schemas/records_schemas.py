import datetime
from pydantic import BaseModel


class Record(BaseModel):
    id: int
    user_id: int
    company_id: int
    quizz_id: int
    record_average_result: float
    user_average_result: float
    questions: int
    correct: int
    created_at: datetime.date


class RecordsList(BaseModel):
    records: list[Record]
