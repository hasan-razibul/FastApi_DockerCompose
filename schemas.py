from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class ProjectCreate(ProjectBase):
    pdf: Optional[bytes] = None


class Project(ProjectBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
