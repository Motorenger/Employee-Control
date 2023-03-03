import os

envs = {
        "HOST": os.environ.get("HOST"),
        "PORT": int(os.environ.get("PORT")),
        "SECRET_KEY": (os.environ.get("SECRET_KEY")),

        "DATABASE_URL": os.environ.get("DATABASE_URL"),
        "DATABASE_URL_TEST": os.environ.get("DATABASE_URL_TEST"),
        "ENVIRONMENT": os.environ.get("ENVIRONMENT"),

        "REDIS_URL": os.environ.get("REDIS_URL"),

        "DOMAIN": os.environ.get("DOMAIN"),
        "API_AUDIENCE": os.environ.get("API_AUDIENCE"),
        "ISSUER": os.environ.get("ISSUER"),
        "JWKS_URL": os.environ.get("JWKS_URL"),
        "ALGORITHM_AUTH_0": os.environ.get("ALGORITHM_AUTH_0"),
        "ALGORITHM_AUTH_2": os.environ.get("ALGORITHM_AUTH_2"),
}
