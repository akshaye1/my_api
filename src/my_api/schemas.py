from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    priority: int
    
class TaskResponse(BaseModel):
    id: int
    title: str
    priority: int
    
class TaskUpdate(BaseModel):
    title: str | None = None
    priority: int | None = None