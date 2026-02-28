from jose.exceptions import ExpiredSignatureError
from jose import jwt
from datetime import datetime, timedelta
import bcrypt
from app.core.settings import settings


def hash_password(plain_passowrd: str):
    return bcrypt.hashpw(plain_passowrd.encode(), bcrypt.gensalt()).decode()


def is_password_valid(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def generate_token(data: dict):
    copied_data = data.copy()
    copied_data["exp"] = datetime.utcnow() + timedelta(minutes=settings.JWT_EXP_MINUTES)
    return jwt.encode(copied_data, settings.SECRET_KEY, algorithm="HS256")


def validate_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError as err:
        print(err, "Token expired")
        return None
    except Exception as err:
        print(err)
        return None
