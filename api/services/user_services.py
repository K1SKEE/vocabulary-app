from typing import Generator
import random

from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from websockets.exceptions import ConnectionClosedError

from api.schemas import AddWordResponse, AddWordForm, Vocabulary, Word
from db.managers import UserManager, DictionaryManager
from db.models import User
from api.utils import ConnectionManager


async def add_new_word(
        body: AddWordForm, user: User,
        session: AsyncSession) -> AddWordResponse | None:
    async with session.begin():
        user_manager = DictionaryManager(session)
        result = await user_manager.add_to_vocabulary(
            eng=body.eng, ukr=body.ukr, user=user
        )
        return AddWordResponse(eng=result.eng, ukr=result.ukr)


async def get_vocabulary_service(user: User,
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


async def delete_word_service(word_id: int,
                              session: AsyncSession, user: User) -> None:
    async with session.begin():
        dictionary_manager = DictionaryManager(session)
        await dictionary_manager.delete_word_from_vocabulary(
            word_id=word_id,
            user_id=user.user_id
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


async def ws_repetition_service(websocket: WebSocket,
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
                    {"result": f"Wrong answer! \n({word.ukr})"}, websocket)
        except ConnectionClosedError:
            pass
