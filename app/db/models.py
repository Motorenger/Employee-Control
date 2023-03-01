import sqlalchemy


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
