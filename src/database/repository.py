from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.orm import Todo


def get_todos(session: Session) -> List[Todo]:

    return list(session.scalars(select(Todo)))


def get_todo_by_todo_id(session: Session, todo_id: int) -> Todo | None:

    stmt = select(Todo).where(Todo.id == todo_id)
    result = session.scalar(stmt)

    return result


def create_todo(session: Session, todo: Todo) -> Todo:
    session.add(instance=todo)
    session.commit()
    session.refresh(instance=todo)
    return todo


def update_todo(session: Session, todo: Todo) -> Todo:
    session.add(instance=todo)
    session.commit()
    session.refresh(instance=todo)
    return todo


def delete_todo(session: Session, todo: Todo) -> None:
    session.delete(instance=todo)
    session.commit()
