from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from my_api.database import get_db
from my_api.models import Task
from my_api.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter()


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    statement = select(Task)
    return db.execute(statement).scalars().all()


@router.post("/tasks", response_model=TaskResponse)
def add_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    try:
        new_task = Task(
            title=task.title,
            priority=task.priority
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return new_task

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while adding the task"
        )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    statement = select(Task).where(Task.id == task_id)
    task = db.execute(statement).scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task_route(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    statement = select(Task).where(Task.id == task_id)
    task = db.execute(statement).scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task_update.title is not None:
        task.title = task_update.title

    if task_update.priority is not None:
        task.priority = task_update.priority

    db.commit()
    db.refresh(task)

    return task


@router.delete("/tasks/{task_id}")
def remove_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    statement = select(Task).where(Task.id == task_id)
    task = db.execute(statement).scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully!"}