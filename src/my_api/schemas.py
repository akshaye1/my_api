from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated

TaskTitle = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]

class TaskCreate(BaseModel):
    title: TaskTitle
    priority: int = Field(ge=1, le=5)
    
class TaskResponse(BaseModel):
    id: int
    title: str
    priority: int
    
class TaskUpdate(BaseModel):
    title: str | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
    
