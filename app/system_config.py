import os


HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))

DATABASE_URL = os.environ.get("DATABASE_URL")

REDIS_URL = os.environ.get("REDIS_URL")

envs = {
        "HOST": os.environ.get("HOST"),
        "PORT": int(os.environ.get("PORT")),

        "DATABASE_URL": os.environ.get("DATABASE_URL"),

        "REDIS_URL": os.environ.get("REDIS_URL"),
}
