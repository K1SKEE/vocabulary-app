import base64
import hashlib
import os
from datetime import timedelta, datetime
from typing import Generator
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets

from jose import jwt
from cryptography.fernet import Fernet, InvalidToken
from fastapi import WebSocket
from pydantic import EmailStr

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


class JWT:
    @classmethod
    def create_token_for_access(cls, user: User) -> tuple:
        access_token = cls.create_access_token(user)
        refresh_token = cls.create_refresh_token(user)
        return access_token, refresh_token

    @staticmethod
    def create_access_token(user: User):
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = JWT._create_jwt_token(
            data={"sub": user.username, "other_custom_data": [1, 2, 3, 4]},
            expires_delta=access_token_expires,
        )
        return access_token

    @staticmethod
    def create_refresh_token(user: User):
        refresh_token_expires = timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = JWT._create_jwt_token(
            data={"sub": user.username, "type": "refresh"},
            expires_delta=refresh_token_expires,
        )
        return refresh_token

    @staticmethod
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


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


async def get_manager() -> Generator:
    manager = ConnectionManager()
    yield manager


class EmailClientManager:
    def __init__(self):
        self.config = settings.EMAIL_CONFIG
        self.from_email = settings.EMAIL_CONFIG.get('EMAIL_LOGIN')
        self.server = None

    async def connect(self) -> None:
        self.server = smtplib.SMTP(
            self.config.get('SMTP_SERVER'),
            self.config.get('SMTP_PORT')
        )
        self.server.starttls()
        self.server.login(
            self.config.get('EMAIL_LOGIN'),
            self.config.get('EMAIL_PASSWORD')
        )

    async def send_email(self, to_email: EmailStr) -> str:
        if not self.server:
            await self.connect()
        text, token = await self.make_message(to_email)
        self.server.sendmail(self.from_email, to_email, text)
        self.server.quit()
        return token

    async def make_message(self, to_email: EmailStr) -> tuple:
        msg = MIMEMultipart()
        msg['From'], msg['To'] = self.from_email, to_email
        msg['Subject'] = "Activate your account"
        token = ConfirmationToken.generate_confirmation_token(to_email)
        body = f"""
                <a href="http://localhost/register?token={token}">
                    Activate account
                </a>
                """
        msg.attach(MIMEText(body, 'html'))
        text = msg.as_string()
        return text, token


class ConfirmationToken:
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    @classmethod
    def generate_confirmation_token(cls, email: EmailStr) -> str:
        token = secrets.token_urlsafe(32)
        payload = base64.urlsafe_b64encode(
            cls.cipher_suite.encrypt(email.encode())).decode()
        return f'{token}.{payload}.{cls.key.decode()}'

    @classmethod
    def decrypt_confirmation_token(cls, token: str) -> tuple | None:
        try:
            token_parts = token.split('.')
            token_key = token_parts[2].encode()
            suite = Fernet(token_key)
            email = suite.decrypt(
                base64.urlsafe_b64decode(token_parts[1].encode())).decode()
            return email, token_parts[0]
        except (IndexError, ValueError, TypeError, InvalidToken):
            return None
