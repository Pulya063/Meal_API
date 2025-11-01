from typing import List
from pydantic import BaseModel
from datetime import date

class MealBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class CreateMeal(MealBase):
    pass

class ResponseMeal(MealBase):
    id: int

class CreateUser(BaseModel):
    username: str
    password: str

class UserBase(CreateUser):
    date: date
    meals: List[MealBase] = []

    class Config:
        orm_mode = True

class RegisterUser(CreateUser):
    pass

class ResponseUser(UserBase):
    user_id: int
