import hashlib
import os
from datetime import timedelta, datetime

from jose import jwt

import settings
from db.models import User


class Hasher:
    @staticmethod
    def hash_password(password: str) -> tuple:
        salt = os.urandom(32)
        encoded_password = password.encode('utf-8')
        password_hash = hashlib.sha256(salt + encoded_password).hexdigest()
        return password_hash, salt

    @staticmethod
    def check_password(password: str, password_hash: str, salt: bytes) -> bool:
        encoded_password = password.encode('utf-8')
        hash_result = hashlib.sha256(salt + encoded_password).hexdigest()
        return hash_result == password_hash


def create_access_token(user: User):
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _create_jwt_token(
        data={"sub": user.username, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    return access_token


def _create_jwt_token(data: dict,
                      expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
