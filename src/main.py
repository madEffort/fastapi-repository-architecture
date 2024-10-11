from typing import List
from fastapi import Depends, FastAPI, Body, HTTPException
from pydantic import BaseModel

from database.connection import get_db
from sqlalchemy.orm import Session

from database.orm import Todo
from database.repository import get_todo_by_todo_id, get_todos
from schema.response import ListTodoResponse, ToDoSchema

app = FastAPI()

todo_data = {
    1: {
        "id": 1,
        "contents": "실전! FastAPI 섹션 0 수강",
        "is_done": True,
    },
    2: {
        "id": 2,
        "contents": "실전! FastAPI 섹션 1 수강",
        "is_done": True,
    },
    3: {
        "id": 3,
        "contents": "실전! FastAPI 섹션 2 수강",
        "is_done": True,
    },
}


# 상태 체크
@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


# 전체 조회 & 쿼리 파라미터
@app.get("/todos")
def get_todos_handler(
    order: str | None = None,
    session: Session = Depends(get_db),
) -> ListTodoResponse:
    todos: List[Todo] = get_todos(session=session)
    if order and order == "DESC":
        return ListTodoResponse(
            todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    return ListTodoResponse(todos=[ToDoSchema.from_orm(todo) for todo in todos])

    # ret = list(todo_data.values())
    # if order and order == "DESC":
    #     return ret[::-1]
    # return ret


# 단일 조회
@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
    todo_id: int,
    session: Session = Depends(get_db),
) -> ToDoSchema:

    todo: Todo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)

    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="투두를 찾을 수 없습니다.")


class CreateTodoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool


# 생성
@app.post("/todos", status_code=201)
def create_todos_handler(request: CreateTodoRequest):
    todo_data[request.id] = request.model_dump()
    return todo_data[request.id]


# 수정
@app.patch("/todos/{todo_id}")
def update_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
):
    todo = todo_data.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="투두를 찾을 수 없습니다.")


# 삭제
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int):
    todo = todo_data.pop(todo_id, None)
    if todo:
        return
    raise HTTPException(status_code=404, detail="투두를 찾을 수 없습니다.")
