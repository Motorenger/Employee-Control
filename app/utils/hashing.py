from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(*, new_pass: str, old_pass: str):
    return pwd_context.verify(new_pass, old_pass)
