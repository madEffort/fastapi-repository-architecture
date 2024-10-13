from typing import List
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import Todo, User


class TodoRepository:

    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_todos(self) -> List[Todo]:

        return list(self.session.scalars(select(Todo)))

    def get_todo_by_todo_id(self, todo_id: int) -> Todo | None:

        stmt = select(Todo).where(Todo.id == todo_id)
        result = self.session.scalar(stmt)

        return result

    def create_todo(self, todo: Todo) -> Todo:
        self.session.add(instance=todo)
        self.session.commit()
        self.session.refresh(instance=todo)
        return todo

    def update_todo(self, todo: Todo) -> Todo:
        self.session.add(instance=todo)
        self.session.commit()
        self.session.refresh(instance=todo)
        return todo

    def delete_todo(self, todo: Todo) -> None:
        self.session.delete(instance=todo)
        self.session.commit()


class UserReposotory:

    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def save_user(self, user: User) -> User:
        self.session.add(instance=user)
        self.session.commit()
        self.session.refresh(instance=user)
        return user
