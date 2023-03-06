import sqlalchemy
from sqlalchemy.orm import relationship


metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("username", sqlalchemy.String(20)),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean),
    sqlalchemy.Column("date_joined", sqlalchemy.DateTime),
)

companies = sqlalchemy.Table(
    "companies",
    metadata,
    sqlalchemy.Column("owner_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("visible", sqlalchemy.Boolean),
)
