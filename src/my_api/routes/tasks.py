from fastapi import APIRouter, HTTPException
from my_api.schemas import TaskCreate, TaskResponse, TaskUpdate
from my_api.services.task_service import create_task, get_all_tasks, get_task_by_id, update_task, delete_task

router = APIRouter()

@router.get("/tasks")
def get_tasks():
    return get_all_tasks()

@router.post("/tasks",response_model=TaskResponse)
def add_task(task: TaskCreate):
    return create_task(task.title, task.priority)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task_route(task_id: int, task_update: TaskUpdate):
    task = update_task(
        task_id,
        task_update.title,
        task_update.priority
    )
    if task is None:
        raise HTTPException(status_code=400, detail="Task not found")    
    return task

@router.delete("/tasks/{task_id}")
def remove_task(task_id:int):
    deleted = delete_task(task_id)
    
    if not deleted:
        raise HTTPException(status_code=400, detail="Task not found")
    
    return {"message": "Task deleted successfully!"}