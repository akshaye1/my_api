from fastapi import FastAPI
from my_api.routes.tasks import router as tasks_router
from my_api.database import create_tables

app = FastAPI()

create_tables()

app.include_router(tasks_router)

@app.get("/")
def home():
    return {"message": "Welcome to my API!"}

