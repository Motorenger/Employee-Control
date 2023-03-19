import sqlalchemy
from sqlalchemy.orm import relationship


metadata = sqlalchemy.MetaData()


# User model
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("username", sqlalchemy.String(20)),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean),
    sqlalchemy.Column("date_joined", sqlalchemy.DateTime),
    sqlalchemy.Column("questions", sqlalchemy.Integer),
    sqlalchemy.Column("correct", sqlalchemy.Integer)
)


# Company model
companies = sqlalchemy.Table(
    "companies",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("visible", sqlalchemy.Boolean),
    sqlalchemy.Column("owner_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
)


# Company-users model
company_members = sqlalchemy.Table(
    "company_members",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id"), nullable=False),
    sqlalchemy.Column("admin", sqlalchemy.Boolean),
    sqlalchemy.Column("questions", sqlalchemy.Integer),
    sqlalchemy.Column("correct", sqlalchemy.Integer)
)


# Invite model
invites = sqlalchemy.Table(
    "invites",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id"), nullable=False),
    sqlalchemy.Column("message", sqlalchemy.Text)
)


# Request model
requests = sqlalchemy.Table(
    "requests",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id"), nullable=False),
    sqlalchemy.Column("message", sqlalchemy.Text)
)


# Quizz model
quizzes = sqlalchemy.Table(
    "quizzes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String()),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("pass_freq", sqlalchemy.Integer),
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column("created_by", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("updated_by", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
)


# Question model
questions = sqlalchemy.Table(
    "questions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("quizz_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("correct_answer", sqlalchemy.Integer)
)


# Answer model
answers = sqlalchemy.Table(
    "answers",
    metadata,
    sqlalchemy.Column("question_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("questions.id", ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column("answer", sqlalchemy.String)
)


# Quizz completion recorn
records = sqlalchemy.Table(
    "records",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id"), nullable=False),
    sqlalchemy.Column("quizz_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("quizzes.id"), nullable=False),
    sqlalchemy.Column("average_result", sqlalchemy.Float),
    sqlalchemy.Column("questions", sqlalchemy.Integer),
    sqlalchemy.Column("correct", sqlalchemy.Integer),
    sqlalchemy.Column("created_at", sqlalchemy.Date),
)
