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


class AnalyticsRecords(BaseModel):
    result: float
    created_at: datetime.date

class QuizzesAnalyticsUser(BaseModel):
    quizz_id: int
    analytics: list[AnalyticsRecords]


class QuizzAnalyticsUser(BaseModel):
    quizz_id: int
    last_pass_date: datetime.date

class AnalyticsUser(BaseModel):
    quizzes: list[QuizzesAnalyticsUser | QuizzAnalyticsUser]



class UserAnalyticsCompany(BaseModel):
    user_id: int
    records: list[AnalyticsRecords]


class UserAnalytics(BaseModel):
    user_id: int
    last_pass_time: datetime.date

class AnalyticsCompany(BaseModel):
    users: list[UserAnalyticsCompany | UserAnalytics]