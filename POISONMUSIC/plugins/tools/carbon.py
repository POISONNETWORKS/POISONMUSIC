import aiohttp
from io import BytesIO
from pyrogram import filters
from pyrogram.types import Message
from POISONMUSIC import app

async def make_carbon(code: str) -> BytesIO | None:
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"code": code}) as resp:
            if resp.status != 200:
                return None
            image = BytesIO(await resp.read())
            image.name = "carbon.png"
            return image


@app.on_message(filters.command("carbon"))
async def generate_carbon(_, message: Message):
    replied = message.reply_to_message

    if not replied or not (replied.text or replied.caption):
        return await message.reply_text(
            "**ʀєᴘʟʏ ᴛσ ᴧ ᴛєxᴛ ϻєssᴧɢє ᴛσ ɢєηєʀᴧᴛє ᴧ ᴄᴧʀʙση.**"
        )

    status = await message.reply("🔄 ᴄʀєᴧᴛɪηɢ ʏσυʀ ᴄᴧʀʙση...")
    carbon = None

    try:
        carbon = await make_carbon(replied.text or replied.caption)
        if not carbon:
            return await status.edit("❌ ғᴧɪʟєᴅ ᴛσ ɢєηєʀᴧᴛє ᴄᴧʀʙση.")
        await message.reply_photo(carbon)
        await status.delete()
    except Exception:
        await status.edit("❌ ᴧη єʀʀσʀ σᴄᴄυʀʀєᴅ ᴡʜɪʟє ᴄʀєᴧᴛɪηɢ ᴄᴧʀʙση.")
    finally:
        if carbon:
            carbon.close()
