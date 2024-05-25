from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import timedelta
from app.config.database import user_collection
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.utils.token import create_access_token, decode_access_token
from app.config.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

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
        hashed_password=hashed_password,
    )
    await user_collection.insert_one(new_user.dict(by_alias=True))
    return UserResponse(**new_user.dict())

@router.post("/token", response_model=dict)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user_record = await user_collection.find_one({"username": form_data.username})
    if not user_record or not pwd_context.verify(form_data.password, user_record["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_record["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await user_collection.find_one({"username": payload.get("sub")})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get("/user/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserResponse(**current_user)
