# app/models/passenger.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class Passenger(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    hashed_password: str
    role: str = "passenger"

    class Config:
        schema_extra = {
            "example": {
                "username": "passenger1",
                "email": "passenger1@example.com",
                "full_name": "Passenger One",
                "disabled": False,
                "hashed_password": "fakehashedpass1",
                "role": "passenger"
            }
        }
