import socket
import time
import heroku3

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from config import HEROKU_API_KEY, HEROKU_APP_NAME, OWNER_ID
from POISONMUSIC.core.mongo import mongodb
from .logging import LOGGER

SUDOERS = filters.user()
COMMANDERS = [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
HAPP = None
_boot_ = time.time()

def is_heroku():
    return "heroku" in socket.getfqdn()

XCB = [
    "/", "@", ".", "com", ":", "git", "heroku", "push",
    str(HEROKU_API_KEY), "https", str(HEROKU_APP_NAME),
    "HEAD", "master"
]

def dbb():
    global db
    db = {}
    LOGGER(__name__).info("ᴅᴧᴛᴧʙᴧsє ʟσᴧᴅєᴅ sυᴄᴄєssϝυʟʟʏ💗")

async def sudo():
    global SUDOERS
    SUDOERS.add(OWNER_ID)
    sudoersdb = mongodb.sudoers
    data = await sudoersdb.find_one({"sudo": "sudo"}) or {}
    sudoers = data.get("sudoers", [])

    if OWNER_ID not in sudoers:
        sudoers.append(OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
        )

    for user_id in sudoers:
        SUDOERS.add(user_id)

    LOGGER(__name__).info("sυᴅσ υsєʀs ᴅσηє..")

def heroku():
    global HAPP
    if is_heroku():
        if HEROKU_API_KEY and HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(HEROKU_API_KEY)
                HAPP = Heroku.app(HEROKU_APP_NAME)
                LOGGER(__name__).info("ʜєʀσᴋυ ᴧᴘᴘ ᴄσηϝɪɢυʀєᴅ..")
            except Exception:
                LOGGER(__name__).warning("ʏσυ sʜσυʟᴅ ʜᴧᴠє ησᴛ ϝɪʟʟєᴅ ʜєʀσᴋυ ᴧᴘᴘ ηᴧϻє σʀ ᴧᴘɪ ᴋєʏ ᴄσʀʀєᴄᴛʟʏ ᴘʟєᴧsє ᴄʜєᴄᴋ ɪᴛ...")
