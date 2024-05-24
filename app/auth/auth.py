from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.schemas.user import UserInDB
from app.config.database import passenger_collection, staff_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_user(db, username: str):
    user = await db.find_one({"username": username})
    if user:
        return UserInDB(**user)
    return None

async def fake_decode_token(token: str):
    user = await get_user(passenger_collection, token)
    if not user:
        user = await get_user(staff_collection, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: BaseModel = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_passenger(current_user: BaseModel = Depends(get_current_user)):
    if current_user.user_type != "passenger":
        raise HTTPException(status_code=400, detail="Not a passenger")
    return current_user

async def get_current_active_staff(current_user: BaseModel = Depends(get_current_user)):
    if current_user.user_type != "staff":
        raise HTTPException(status_code=400, detail="Not a staff")
    return current_user
