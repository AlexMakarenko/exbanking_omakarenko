from typing import Union

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserBalance(UserBase):
    balance: float


class ChangeBalance(UserBase):
    amount: float


class SendAmount(UserBase):
    amount: float
    receiver_email: str


class User(UserBase):
    id: int
    balance: float

    class Config:
        orm_mode = True
