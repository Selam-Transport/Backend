import motor.motor_asyncio # type: ignore

MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client["selam_transport"]

user_collection = database.get_collection("users")
