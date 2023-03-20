from pydantic import BaseModel


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
