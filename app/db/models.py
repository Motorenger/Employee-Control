from sqlalchemy import Column, Integer, String, Boolean, DateTime

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    username = Column(String(20))
    is_active = Column(Boolean, default=False)
    date_joined = Column(DateTime)
