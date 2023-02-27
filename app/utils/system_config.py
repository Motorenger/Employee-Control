import os

envs = {
        "HOST": os.environ.get("HOST"),
        "PORT": int(os.environ.get("PORT")),

        "DATABASE_URL": os.environ.get("DATABASE_URL"),
        "DATABASE_URL_TEST": os.environ.get("DATABASE_URL_TEST"),
        "ENVIRONMENT": os.environ.get("ENVIRONMENT"),

        "REDIS_URL": os.environ.get("REDIS_URL"),
}
