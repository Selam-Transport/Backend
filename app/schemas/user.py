from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    full_name: str
    email: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool

    class Config:
        orm_mode = True

