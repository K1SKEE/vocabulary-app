from typing import Generator
import random

from fastapi import HTTPException, Depends, WebSocket
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from websockets.exceptions import ConnectionClosedError

import settings
from api.schemas import (UserCreateForm, UserCreateResponse, Token,
                         AddWordResponse, AddWordForm, Vocabulary, Word)
from db.managers import UserManager, DictionaryManager
from db.models import User
from api.utils import Hasher, JWT, ConnectionManager
from db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _create_new_user(body: UserCreateForm,
                           session: AsyncSession) -> UserCreateResponse | None:
    if body.password_1 != body.password_2:
        return
    hashed_password, salt = Hasher.hash_password(body.password_1)
    async with session.begin():
        user_manager = UserManager(session)
        await user_manager.create_user(
            username=body.username,
            hashed_password=hashed_password,
            salt=salt
        )
        return UserCreateResponse(username=body.username,
                                  password=body.password_1)


async def _get_user_for_auth(
        username: str,
        session: AsyncSession) -> User | None:
    async with session.begin():
        user_manager = UserManager(session)
        return await user_manager.get_user(username=username)


async def _authenticate_user(username: str,
                             password: str,
                             session: AsyncSession
                             ) -> Token | None:
    user = await _get_user_for_auth(username, session)
    if user is None:
        return
    if not Hasher.check_password(password, user.hashed_password, user.salt):
        return
    token = JWT.create_access_token(user=user)
    return token


async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_for_auth(username=username, session=db)
    if user is None:
        raise credentials_exception
    return user


async def _add_new_word(
        body: AddWordForm, user: User,
        session: AsyncSession) -> AddWordResponse | None:
    async with session.begin():
        user_manager = DictionaryManager(session)
        result = await user_manager.add_to_vocabulary(
            eng=body.eng, ukr=body.ukr, user=user
        )
        return AddWordResponse(eng=result.eng, ukr=result.ukr)


async def _get_vocabulary(user: User,
                          session: AsyncSession) -> Vocabulary:
    async with session.begin():
        user_manager = UserManager(session)
        result = await user_manager.get_user_vocabulary(user.username)
        vocabulary = [{
            'eng': row.eng,
            'ukr': row.ukr,
            'flag': row.flag,
            'id': row.id
        } for row in result]
        return Vocabulary(vocabulary=vocabulary)


async def update_word_from_vocabulary(
        body: dict,
        session: AsyncSession,
        user: User) -> Word:
    word_id = body.pop('id')
    async with session.begin():
        dictionary_manager = DictionaryManager(session)
        result = await dictionary_manager.update_vocabulary(
            word_id=word_id,
            user_id=user.user_id,
            **body
        )
        return Word(
            id=result.id,
            eng=result.eng,
            ukr=result.ukr,
            flag=result.flag,
            user_id=result.user_id
        )


def _get_word_generator(vocabulary: list) -> Generator:
    random.shuffle(vocabulary)
    for word in vocabulary:
        yield word


def check_answer(answer: str, word: str) -> bool | None:
    if answer == word:
        return True
    word_list = word.split(', ')
    if answer in word_list:
        return True


async def _ws_repetition_service(websocket: WebSocket,
                                 session: AsyncSession,
                                 user: User,
                                 manager: ConnectionManager) -> None:
    async with session.begin():
        user_manager = UserManager(session)
        vocabulary = await user_manager.get_user_vocabulary_for_repetition(
            user.username
        )
    for word in _get_word_generator(vocabulary):
        try:
            await manager.send_personal_message({"eng": word.eng}, websocket)
            answer = await websocket.receive_text()
            if check_answer(answer, word.ukr):
                await manager.send_personal_message(
                    {"result": "Right answer!"}, websocket)
            else:
                await manager.send_personal_message(
                    {"result": "Wrong answer!"}, websocket)
        except ConnectionClosedError:
            pass
