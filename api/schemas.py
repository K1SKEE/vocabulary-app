from typing import Union

from pydantic import BaseModel


class Model(BaseModel):
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str
