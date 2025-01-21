from pydantic import BaseModel
from typing import Literal

class Task(BaseModel):
    taskId: str
    title: str
    description: str
    status: Literal["pending", "in-progress", "completed"]
