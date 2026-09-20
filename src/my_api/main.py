from fastapi import FastAPI, HTTPException
from my_api.schemas import TaskCreate, TaskResponse, TaskUpdate

app = FastAPI()

tasks = []

@app.get("/")
def home():
    return {"message": "Welcome to my API!"}

@app.post("/tasks",response_model=TaskResponse)
def create_task(task: TaskCreate):
    new_task = {"id": len(tasks) + 1, "title": task.title, "priority": task.priority}
    tasks.append(new_task)
    return new_task

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}",response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if task_update.title is not None:
                task["title"] = task_update.title
            if task_update.priority is not None:
                task["priority"] = task_update.priority
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
