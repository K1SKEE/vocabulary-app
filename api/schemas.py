import re
from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, validator

ENG_LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Z\-\(\)\s]+$")
UKR_LETTER_MATCH_PATTERN = re.compile(r"^[а-щьюяєіїґА-ЩЬЮЯЄІЇҐ'\-\(\)\s,]+$")


class Model(BaseModel):
    class Config:
        orm_mode = True


class UserCreateForm(BaseModel):
    username: str
    password_1: str
    password_2: str


class UserCreateResponse(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'


class AddWordForm(BaseModel):
    eng: str
    ukr: str

    @validator('eng')
    def validate_eng(cls, value):
        if not ENG_LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Eng should contains only eng letters"
            )
        return value

    @validator('ukr')
    def validate_ukr(cls, value):
        if not UKR_LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Ukr should contains only ukr letters"
            )
        return value


class AddWordResponse(BaseModel):
    eng: str
    ukr: str


class Word(Model):
    id: int
    eng: Optional[str]
    ukr: Optional[str]
    flag: Optional[bool]

    @validator('eng')
    def validate_eng(cls, value):
        if not ENG_LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Eng should contains only eng letters"
            )
        return value

    @validator('ukr')
    def validate_ukr(cls, value):
        if not UKR_LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Ukr should contains only ukr letters"
            )
        return value


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total_pages: int
    total_rows: int


class Vocabulary(Model):
    vocabulary: List[Word]
    meta: PaginationMeta


class SearchWordResponse(Model):
    result: List[Word]
