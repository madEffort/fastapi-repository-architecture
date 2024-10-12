from typing import List
from pydantic import BaseModel


class TodoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    class Config:
        from_attributes = True


class ListTodoSchema(BaseModel):
    todos: List[TodoSchema]
