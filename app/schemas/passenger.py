# app/schemas/passenger.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class PassengerCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: str

class PassengerResponse(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: str
