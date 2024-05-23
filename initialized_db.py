import motor.motor_asyncio
from bson.objectid import ObjectId
import asyncio

MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client["selam_transport"]

passenger_collection = database.get_collection("passengers")
staff_collection = database.get_collection("staff")

passengers = [
    {
        "_id": ObjectId(),
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    {
        "_id": ObjectId(),
        "username": "janedoe",
        "full_name": "Jane Doe",
        "email": "janedoe@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": False,
    },
]

staff = [
    {
        "_id": ObjectId(),
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": "fakehashedadmin",
        "disabled": False,
    },
    {
        "_id": ObjectId(),
        "username": "staffuser",
        "full_name": "Staff User",
        "email": "staffuser@example.com",
        "hashed_password": "fakehashedstaff",
        "disabled": False,
    },
]

async def init_db():
    await passenger_collection.insert_many(passengers)
    await staff_collection.insert_many(staff)
    print("Database initialized with sample data.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
