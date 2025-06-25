from pydantic import BaseModel, Field
from typing import List

class TodoListItem(BaseModel):
    title: str = Field(description="Short title for the task")
    description: str = Field(description="Detailed description of the task")
    time: str = Field(description="Time or deadline for the task")

class TodoList(BaseModel):
    todo_list: List[TodoListItem]