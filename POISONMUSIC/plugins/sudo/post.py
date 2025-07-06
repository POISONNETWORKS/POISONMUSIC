from pyrogram import filters
from POISONMUSIC import app
from config import OWNER_ID

destination_group_id = -1002601268013

@app.on_message(filters.command(["post"], prefixes=["/", "."]) & filters.user(OWNER_ID))
async def copy_messages(_, message):

    if message.reply_to_message:

        await message.reply_to_message.copy(destination_group_id)
        await message.reply("ᴘσsᴛ sυᴄᴄєssғυʟ ᴅσηє ")
