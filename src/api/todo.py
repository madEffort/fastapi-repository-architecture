from typing import List
from fastapi import Depends, Body, HTTPException, APIRouter


from database.orm import Todo

from database.repository import TodoRepository
from schema.request import CreateTodoSchema
from schema.response import ListTodoSchema, TodoSchema


router = APIRouter(prefix="/todos")


# 전체 조회 & 쿼리 파라미터
@router.get("")
def get_todos_handler(
    order: str | None = None,
    todo_repo: TodoRepository = Depends(TodoRepository),
) -> ListTodoSchema:

    todos: List[Todo] = todo_repo.get_todos()
    if order and order == "DESC":
        return ListTodoSchema(
            todos=[TodoSchema.model_validate(todo) for todo in todos[::-1]]
        )
    return ListTodoSchema(todos=[TodoSchema.model_validate(todo) for todo in todos])


# 단일 조회
@router.get("/{todo_id}", status_code=200)
def get_todo_handler(
    todo_id: int,
    todo_repo: TodoRepository = Depends(TodoRepository),
) -> TodoSchema:

    todo: Todo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)

    if todo:
        return TodoSchema.model_validate(todo)
    raise HTTPException(status_code=404, detail="투두를 찾을 수 없습니다.")


# 생성
@router.post("", status_code=201)
def create_todos_handler(
    request: CreateTodoSchema,
    todo_repo: TodoRepository = Depends(TodoRepository),
) -> TodoSchema:
    todo: Todo = Todo.create(request=request)
    todo: Todo = todo_repo.create_todo(todo=todo)

    return TodoSchema.model_validate(todo)


# 수정
@router.patch("/{todo_id}")
def update_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    todo_repo: TodoRepository = Depends(TodoRepository),
) -> TodoSchema:

    todo: Todo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo:
        # update
        todo.done() if is_done else todo.undone()
        todo: Todo = todo_repo.update_todo(todo=todo)
        return todo
    raise HTTPException(status_code=404, detail="투두를 찾을 수 없습니다.")


# 삭제
@router.delete("/{todo_id}", status_code=204)
def delete_todo_handler(
    todo_id: int,
    todo_repo: TodoRepository = Depends(TodoRepository),
):

    # 삭제할 투두
    todo: Todo = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo:
        # 삭제
        todo_repo.delete_todo(todo=todo)
        return
    raise HTTPException(status_code=404, detail="투두를 찾을 수 없습니다.")
