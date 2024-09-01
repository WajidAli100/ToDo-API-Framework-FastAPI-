import select
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel ,create_engine ,Session
from user_data.user_data import TodoItem
from dotenv import load_dotenv
import os

load_dotenv()

connection_string = os.getenv("DATABASE_URL")

engine = create_engine(connection_string)

app : FastAPI = FastAPI()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/todo/", response_model=TodoItem)
def create_todo(todo: TodoItem):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.get("/todo/{todo_id}", response_model=TodoItem)
def read_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(TodoItem, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

@app.get("/todos/", response_model=list[TodoItem])
def read_todos(skip: int = 0, limit: int = 10):
    with Session(engine) as session:
        todos = session.exec(select(TodoItem).offset(skip).limit(limit)).all()
        return todos

@app.patch("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, todo_item: TodoItem):
    with Session(engine) as session:
        todo = session.get(TodoItem, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="TodoItem not found")
        todo.title = todo_item.title
        todo.description = todo_item.description
        session.commit()
        session.refresh(todo)
        return todo

@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(TodoItem, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        session.commit()
        return {"message": "Todo deleted successfully"}
        
            
        

