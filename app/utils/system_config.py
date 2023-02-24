import os

envs = {
        "HOST": os.environ.get("HOST"),
        "PORT": int(os.environ.get("PORT")),

        "DATABASE_URL": os.environ.get("DATABASE_URL"),
        "TEST_DATABASE_URL": os.environ.get("TEST_DATABASE_URL"),

        "REDIS_URL": os.environ.get("REDIS_URL"),
}
