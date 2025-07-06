import asyncio
from pyrogram import filters, enums, types
from pyrogram.errors import PeerIdInvalid, RPCError, FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from POISONMUSIC import app


def get_full_name(user):
    return f"{user.first_name} {user.last_name}" if user.last_name else user.first_name


def get_last_seen(status):
    if isinstance(status, str):
        status = status.replace("UserStatus.", "").lower()
    elif isinstance(status, enums.UserStatus):
        status = status.name.lower()

    return {
        "online": "☑️ σηʟɪηє",
        "offline": "❄️ σғғʟɪηє",
        "recently": "⏱ ʀєᴄєηᴛʟʏ",
        "last_week": "🗓 ʟᴧsᴛ ᴡєєᴋ",
        "last_month": "📆 ʟᴧsᴛ ϻσηᴛʜ",
        "long_ago": "😴 ʟσηɢ ᴛɪϻє ᴧɢσ"
    }.get(status, "❓ υηᴋησᴡη")


@app.on_message(filters.command(["info", "userinfo", "whois"]))
async def whois_handler(_, message: Message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        elif len(message.command) > 1:
            user = await app.get_users(message.command[1])
        else:
            user = message.from_user

        loading = await message.reply("🔍 <b>ɢᴧᴛʜєʀɪηɢ υsєʀ ɪηғσ...</b>")
        await asyncio.sleep(0.5)

        chat_user = await app.get_chat(user.id)

        name = get_full_name(user)
        username = f"@{user.username}" if user.username else "η/ᴧ"
        bio = chat_user.bio or "ησ ʙɪσ"
        dc_id = getattr(user, "dc_id", "η/ᴧ")
        last_seen = get_last_seen(user.status)
        lang = getattr(user, "language_code", "η/ᴧ")

        text = (
            f"👤 <b>υsєʀ ɪηғσ</b>\n"
            f"━━━━━━━━━━━━━━━\n"
            f"➣ <b>υsєʀ ɪᴅ:</b> <code>{user.id}</code>\n"
            f"➣ <b>ηᴧϻє:</b> {name}\n"
            f"➣ <b>υsєʀηᴧϻє:</b> {username}\n"
            f"➣ <b>ʟᴧsᴛ sєєη:</b> {last_seen}\n"
            f"➣ <b>ᴅᴧᴛᴧᴄєηᴛєʀ ɪᴅ:</b> {dc_id}\n"
            f"➣ <b>ʟᴧηɢυᴧɢє:</b> {lang}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"➣ <b>ᴠєʀɪғɪєᴅ:</b> {'ʏєs ✅' if user.is_verified else 'ησ 🥀'}\n"
            f"➣ <b>ᴘʀєϻɪυϻ:</b> {'ʏєs ☑️' if user.is_premium else 'ησ 🥀'}\n"
            f"➣ <b>ʙσᴛ:</b> {'ʏєs 🤖' if user.is_bot else 'ησ 👤'}\n"
            f"➣ <b>sᴄᴧϻ ᴧᴄᴄσυηᴛ:</b> {'ʏєs ⚠️' if getattr(user, 'is_scam', False) else 'ησ ☑️'}\n"
            f"➣ <b>ғᴧᴋє ᴧᴄᴄσυηᴛ:</b> {'ʏєs 🎭' if getattr(user, 'is_fake', False) else 'ησ ☑️'}\n"
            f"➣ <b>ᴘʀσғɪʟє ᴘɪᴄᴛυʀє:</b> {'ʏєs 🌠' if user.photo else 'ησ 🥀'}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"➣ <b>ʙɪσ:</b> <code>{bio}</code>"
        )

        profile_url = f"https://t.me/{user.username}" if user.username else f"tg://user?id={user.id}"
        buttons = InlineKeyboardMarkup([[
            InlineKeyboardButton("👤 ᴠɪєᴡ ᴘʀσғɪʟє", url=profile_url),
            InlineKeyboardButton("📞 ᴘʜσηє", url="tg://settings")
        ]])

        if user.photo:
            photo = await app.download_media(user.photo.big_file_id)
            await app.edit_message_media(
                chat_id=message.chat.id,
                message_id=loading.id,
                media=types.InputMediaPhoto(media=photo, caption=text, parse_mode=enums.ParseMode.HTML),
                reply_markup=buttons
            )
        else:
            await app.edit_message_text(
                chat_id=message.chat.id,
                message_id=loading.id,
                text=text,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=buttons
            )

    except PeerIdInvalid:
        await message.reply("🥀 ɪ ᴄσυʟᴅη'ᴛ ꜰɪηᴅ ᴛʜᴧᴛ υsєʀ.")
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await whois_handler(_, message)
    except RPCError as e:
        await message.reply(f"⚠️ ʀᴘᴄ єʀʀσʀ:\n<code>{e}</code>")
    except Exception as e:
        await message.reply(f"🥀 єʀʀσʀ:\n<code>{e}</code>")
