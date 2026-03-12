from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RequestBase(BaseModel):
    clientName: str
    phone: str
    address: str
    problemText: str

class RequestCreate(RequestBase):
    pass

class Request(RequestBase):
    id: int
    status: str
    assignedTo: Optional[int] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    id: int
    username: str
    full_name: str
    role: str

class User(UserBase):
    class Config:
        from_attributes = True