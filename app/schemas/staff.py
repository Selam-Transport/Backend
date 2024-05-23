# app/schemas/staff.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class StaffCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: str

class StaffResponse(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: str
