from pydantic import BaseModel


class CreateTodoSchema(BaseModel):
    contents: str
    is_done: bool
