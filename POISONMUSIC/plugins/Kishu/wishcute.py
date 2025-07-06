from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import requests
from POISONMUSIC import app

SUPPORT_CHAT = "PoisonMusicSupport"
SUPPORT_BTN = InlineKeyboardMarkup(
    [[InlineKeyboardButton("ꜱυᴘᴘσʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}")]]
)

CUTE_VIDEO = "https://telegra.ph/file/528d0563175669e123a75.mp4"


@app.on_message(filters.command("wish"))
async def wish(_, m):
    if len(m.command) < 2:
        return await m.reply_text("❌ ᴧᴅᴅ ʏσυʀ ᴡɪꜱʜ ʙᴧʙʏ 🥀!")

    try:
        api = requests.get("https://nekos.best/api/v2/happy").json()
        url = api["results"][0]["url"]
    except Exception:
        return await m.reply_text("⚠️ Couldn't fetch animation, try again later.")

    text = m.text.split(None, 1)[1]
    wish_count = random.randint(1, 100)
    name = m.from_user.first_name or "User"

    caption = (
        f"✨ ʜєʏ {name}!\n"
        f"🪄 ʏσυʀ ᴡɪꜱʜ: {text}\n"
        f"📊 ᴘσꜱꜱɪʙɪʟɪᴛʏ: {wish_count}%"
    )

    await app.send_animation(
        chat_id=m.chat.id,
        animation=url,
        caption=caption,
        reply_markup=SUPPORT_BTN,
    )


@app.on_message(filters.command("cute"))
async def cute(_, message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    percent = random.randint(1, 100)

    caption = f"🍑 {mention} ɪꜱ {percent}% ᴄυᴛє ʙᴧʙʏ 🥀"

    await app.send_document(
        chat_id=message.chat.id,
        document=CUTE_VIDEO,
        caption=caption,
        parse_mode=enums.ParseMode.MARKDOWN,
        reply_markup=SUPPORT_BTN,
        reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None,
    )
