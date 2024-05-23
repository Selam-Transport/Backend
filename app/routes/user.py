# app/routes/user.py
from fastapi import APIRouter, Depends
from app.auth.auth import get_current_active_user, get_current_active_passenger, get_current_active_staff
from app.schemas.passenger import PassengerResponse
from app.schemas.staff import StaffResponse
from pydantic import BaseModel
from typing import Union

router = APIRouter()

@router.get("/users/me", response_model=Union[PassengerResponse, StaffResponse])
async def read_users_me(current_user: BaseModel = Depends(get_current_active_user)):
    return current_user

# Endpoint accessible only by passengers
@router.get("/passenger/reservations")
async def read_passenger_reservations(current_user: BaseModel = Depends(get_current_active_passenger)):
    return {"msg": f"Reservations for passenger {current_user['username']}"}

# Endpoint accessible only by staff
@router.get("/staff/dashboard")
async def read_staff_dashboard(current_user: BaseModel = Depends(get_current_active_staff)):
    return {"msg": f"Dashboard for staff {current_user['username']}"}
