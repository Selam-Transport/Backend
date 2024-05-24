from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from app.config.database import user_collection
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from bson import ObjectId

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    existing_user = await user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password
    )
    await user_collection.insert_one(new_user.dict(by_alias=True))
    return UserResponse(**new_user.dict())

@router.post("/login")
async def login_user(user: UserCreate):
    user_record = await user_collection.find_one({"username": user.username})
    if not user_record or not pwd_context.verify(user.password, user_record["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful"}
