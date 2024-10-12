from typing import List
from fastapi import Depends, FastAPI, Body, HTTPException

from database.connection import get_db
from sqlalchemy.orm import Session

from database.orm import Todo
from database.repository import (
    create_todo,
    delete_todo,
    get_todo_by_todo_id,
    get_todos,
    update_todo,
)
from schema.request import CreateTodoSchema
from schema.response import ListTodoSchema, TodoSchema

app = FastAPI()


# 상태 체크
@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


# 전체 조회 & 쿼리 파라미터
@app.get("/todos")
def get_todos_handler(
    order: str | None = None,
    session: Session = Depends(get_db),
) -> ListTodoSchema:

    todos: List[Todo] = get_todos(session=session)
    if order and order == "DESC":
        return ListTodoSchema(
            todos=[TodoSchema.model_validate(todo) for todo in todos[::-1]]
        )
    return ListTodoSchema(todos=[TodoSchema.model_validate(todo) for todo in todos])


# 단일 조회
@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
    todo_id: int,
    session: Session = Depends(get_db),
) -> TodoSchema:

    todo: Todo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)

    if todo:
        return TodoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="투두를 찾을 수 없습니다.")


# 생성
@app.post("/todos", status_code=201)
def create_todos_handler(
    request: CreateTodoSchema, session: Session = Depends(get_db)
) -> TodoSchema:
    todo: Todo = Todo.create(request=request)
    todo: Todo = create_todo(session=session, todo=todo)

    return TodoSchema.model_validate(todo)


# 수정
@app.patch("/todos/{todo_id}")
def update_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    session: Session = Depends(get_db),
) -> TodoSchema:

    todo: Todo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        # update
        todo.done() if is_done else todo.undone()
        todo: Todo = update_todo(session=session, todo=todo)
        return todo
    raise HTTPException(status_code=404, detail="투두를 찾을 수 없습니다.")


# 삭제
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int, session: Session = Depends(get_db)):

    # 삭제할 투두
    todo: Todo = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        # 삭제
        delete_todo(session=session, todo=todo)
        return
    raise HTTPException(status_code=404, detail="투두를 찾을 수 없습니다.")
