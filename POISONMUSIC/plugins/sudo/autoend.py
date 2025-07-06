from pyrogram import filters
from pyrogram.types import Message

from POISONMUSIC import app
from POISONMUSIC.misc import SUDOERS
from POISONMUSIC.utils.database import autoend_off, autoend_on


@app.on_message(filters.command("autoend") & SUDOERS)
async def auto_end_stream(_, message: Message):
    usage = "<b>єxᴧϻᴘʟє :</b>\n\n/autoend [єηᴧʙʟє | ᴅɪsᴧʙʟє]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "enable":
        await autoend_on()
        await message.reply_text(
            "» ᴧυᴛσ єηᴅ sᴛʀєᴧϻ єηᴧʙʟєᴅ.\n\nᴧssɪsᴛᴧηᴛ ᴡɪʟʟ ᴧυᴛσϻᴧᴛɪᴄᴧʟʟʏ ʟєᴧᴠє ᴛʜє ᴠɪᴅєσᴄʜᴧᴛ ᴧғᴛєʀ ғєᴡ ϻɪηs ᴡʜєη ησ σηє ɪs ʟɪsᴛєηɪηɢ."
        )
    elif state == "disable":
        await autoend_off()
        await message.reply_text("» ᴧυᴛσ єηᴅ sᴛʀєᴧϻ ᴅɪsᴧʙʟєᴅ.")
    else:
        await message.reply_text(usage)
