from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from schema.request import CreateTodoRequest, SignUpRequest


Base = declarative_base()


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    def __repr__(self):
        return f"Todo(id={self.id}, contents={self.contents}, is_done={self.is_done})"

    @classmethod
    def create(cls, request: CreateTodoRequest) -> "Todo":
        return cls(
            contents=request.contents,
            is_done=request.is_done,
        )

    def done(self) -> "Todo":
        self.is_done = True
        return self

    def undone(self) -> "Todo":
        self.is_done = False
        return self


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    todos = relationship("Todo", lazy="joined")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"

    @classmethod
    def create(cls, username: str, hashed_password: str):
        return cls(
            username=username,
            password=hashed_password,
        )
