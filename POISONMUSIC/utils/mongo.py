from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from config import MONGO_DB_URI

mongo = MongoCli(MONGO_DB_URI)
db = mongo["POISONMUSIC"]

coupledb = db["couple"]
impdb = db["pretender"]
