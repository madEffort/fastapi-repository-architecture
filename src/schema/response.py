from typing import List
from pydantic import BaseModel, ConfigDict


class TodoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    contents: str
    is_done: bool

    # class Config:
    #     from_attributes = True


class ListTodoSchema(BaseModel):
    todos: List[TodoSchema]


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class JWTResponse(BaseModel):
    access_token: str
