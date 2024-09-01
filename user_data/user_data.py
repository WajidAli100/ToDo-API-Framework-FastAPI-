from sqlmodel import SQLModel, Field

class TodoItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    