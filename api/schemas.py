import re

from fastapi import HTTPException
from pydantic import BaseModel, validator

ENG_LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Z\-]+$")
UKR_LETTER_MATCH_PATTERN = re.compile(r"^[а-щьюяєіїґА-ЩЬЮЯЄІЇҐ\-]+$")


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
