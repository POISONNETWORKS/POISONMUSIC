from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
from ..logging import LOGGER

LOGGER(__name__).info("Cᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ʏᴏᴜʀ Dᴀᴛᴀʙᴀsᴇ...")

try:
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    mongodb = _mongo_async_.Poison
    LOGGER(__name__).info("Cᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ʏᴏᴜʀ Dᴀᴛᴀʙᴀsᴇ.✅")
except Exception as e:
    LOGGER(__name__).error(f"Failed to connect to your Mongo Database: {e}")
    exit()
