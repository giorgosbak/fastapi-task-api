from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Task as TaskDB

app = FastAPI(
    title="Task Manager API",
    description="A REST API for managing tasks",
    version="1.0.0"
)


class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


class Task(TaskCreate):
    id: int


tasks = []
next_task_id = 1


@app.get("/")
def home():
    return {
        "message": "Task Manager API is running"
    }


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskDB(**task.model_dump())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed
        }
    }

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    db_tasks = db.query(TaskDB).all()

    return {
        "total": len(db_tasks),
        "tasks": db_tasks
    }

@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db)
):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed

    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    deleted_task = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully",
        "task": deleted_task
    }


    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
