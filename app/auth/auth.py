# app/auth/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated
from app.config.database import passenger_collection, staff_collection
from app.schemas.passenger import PassengerCreate, PassengerResponse
from app.schemas.staff import StaffCreate, StaffResponse
from app.models.passenger import Passenger
from app.models.staff import Staff
from pydantic import BaseModel
from typing import Union
from bson import ObjectId
import hashlib

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

async def authenticate_user(collection, username: str, password: str):
    user = await collection.find_one({"username": username})
    if user and user["hashed_password"] == hash_password(password):
        return user
    return None

async def get_user(collection, username: str):
    user = await collection.find_one({"username": username})
    if user:
        return user
    return None

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await get_user(passenger_collection, token) or await get_user(staff_collection, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: Annotated[BaseModel, Depends(get_current_user)]):
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_passenger(current_user: Annotated[BaseModel, Depends(get_current_active_user)]):
    if current_user["role"] != "passenger":
        raise HTTPException(status_code=403, detail="Access forbidden for non-passengers")
    return current_user

async def get_current_active_staff(current_user: Annotated[BaseModel, Depends(get_current_active_user)]):
    if current_user["role"] != "staff":
        raise HTTPException(status_code=403, detail="Access forbidden for non-staff")
    return current_user

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(passenger_collection, form_data.username, form_data.password) or \
           await authenticate_user(staff_collection, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user["username"], "token_type": "bearer"}

@router.post("/passenger/", response_model=PassengerResponse)
async def create_passenger(passenger: PassengerCreate):
    passenger_dict = passenger.dict()
    passenger_dict["hashed_password"] = hash_password(passenger_dict.pop("password"))
    passenger_dict["role"] = "passenger"
    await passenger_collection.insert_one(passenger_dict)
    return passenger_dict

@router.post("/staff/", response_model=StaffResponse)
async def create_staff(staff: StaffCreate):
    staff_dict = staff.dict()
    staff_dict["hashed_password"] = hash_password(staff_dict.pop("password"))
    staff_dict["role"] = "staff"
    await staff_collection.insert_one(staff_dict)
    return staff_dict

@router.get("/users/me", response_model=Union[PassengerResponse, StaffResponse])
async def read_users_me(current_user: Annotated[BaseModel, Depends(get_current_active_user)]):
    return current_user

# Endpoint accessible only by passengers
@router.get("/passenger/reservations")
async def read_passenger_reservations(current_user: Annotated[BaseModel, Depends(get_current_active_passenger)]):
    return {"msg": f"Reservations for passenger {current_user['username']}"}

# Endpoint accessible only by staff
@router.get("/staff/dashboard")
async def read_staff_dashboard(current_user: Annotated[BaseModel, Depends(get_current_active_staff)]):
    return {"msg": f"Dashboard for staff {current_user['username']}"}
