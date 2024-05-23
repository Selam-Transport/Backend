# app/models/staff.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class Staff(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    hashed_password: str
    role: str = "staff"

    class Config:
        schema_extra = {
            "example": {
                "username": "staff1",
                "email": "staff1@example.com",
                "full_name": "Staff One",
                "disabled": False,
                "hashed_password": "fakehashedstaff1",
                "role": "staff"
            }
        }
