import asyncio
from datetime import datetime
from pyrogram import filters
from POISONMUSIC import app
from POISONMUSIC.core.userbot import Userbot
from config import OWNER_ID

userbot = Userbot()

BOT_LIST = [
    "poison_x_music_x_bot",
  
]

@app.on_message(filters.command("botschk") & filters.group)
async def check_bots_command(client, message):
    global last_checked_time

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("🚫 You are not authorized to use this command.")

    if not userbot.one.is_connected:
        await userbot.one.start()

    processing_msg = await message.reply_photo(
        photo="https://graph.org/file/e6b215db83839e8edf831.jpg",
        caption="**ᴄʜєᴄᴋɪηɢ ʙσᴛs sᴛᴧᴛs ᴧʟɪᴠє σʀ ᴅєᴧᴅ...**"
    )

    start_time = datetime.now()

    response = "**ʙσᴛs sᴛᴧᴛυs ᴅєᴧᴅ σʀ ᴧʟɪᴠє ᴄʜєᴄᴋєʀ**\n\n"

    for bot_username in BOT_LIST:
        try:
            bot = await userbot.one.get_users(bot_username)
            await asyncio.sleep(0.5)
            await userbot.one.send_message(bot.id, "/start")
            await asyncio.sleep(3)
            
            async for bot_message in userbot.one.get_chat_history(bot.id, limit=1):
                status = "σηʟɪηє ✨" if bot_message.from_user.id == bot.id else "σғғʟɪηє ❄"
                response += f"╭⎋ {bot.mention}\n╰⊚ **sᴛᴧᴛυs: {status}**\n\n"
        except Exception:
            response += f"╭⎋ {bot_username}\n╰⊚ **sᴛᴧᴛυs: єʀʀσʀ ❌**\n\n"
    
    last_checked_time = start_time.strftime("%Y-%m-%d")
    await processing_msg.edit_caption(f"{response}⏲️ ʟᴧsᴛ ᴄʜєᴄᴋ: {last_checked_time}")

    if userbot.one.is_connected:
        await userbot.one.stop()
