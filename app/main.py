from fastapi import FastAPI
from app.routes.user import router as User_router


app = FastAPI()


app.include_router(User_router, tags=["User"], prefix="/user")