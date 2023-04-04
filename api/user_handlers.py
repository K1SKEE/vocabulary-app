from fastapi import APIRouter, Depends, WebSocket, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect

from api.schemas import AddWordResponse, AddWordForm, Vocabulary, Word
from api.services.auth_services import get_current_user_from_token
from api.services.user_services import (
    add_new_word, get_vocabulary_service, update_word_from_vocabulary,
    delete_word_service, ws_repetition_service,
)
from api.utils import ConnectionManager, get_manager
from db.models import User
from db.session import get_db

user_router = APIRouter()


@user_router.post('/add', response_model=AddWordResponse)
async def add_new_word_to_vocabulary(
        body: AddWordForm,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> AddWordResponse | None:
    return await add_new_word(body, current_user, db)


@user_router.get('/vocabulary', response_model=Vocabulary)
async def get_vocabulary(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> Vocabulary:
    return await get_vocabulary_service(user=current_user, session=db)


@user_router.patch('/vocabulary', response_model=Word)
async def update_word(
        body: Word,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> Word:
    updated_word_params = body.dict(exclude_none=True)
    return await update_word_from_vocabulary(
        body=updated_word_params, session=db, user=current_user)


@user_router.delete('/vocabulary/{word_id}', response_model=None)
async def delete_word(
        word_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> None:
    return await delete_word_service(word_id=word_id, session=db,
                                     user=current_user)


@user_router.websocket('/ws')
async def ws_repetition(
        websocket: WebSocket,
        token: str = Query(...),
        db: AsyncSession = Depends(get_db),
        manager: ConnectionManager = Depends(get_manager)
) -> None:
    try:
        if token:
            current_user = await get_current_user_from_token(token, db)
            await manager.connect(websocket)
            await ws_repetition_service(websocket, db, current_user,
                                        manager)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
