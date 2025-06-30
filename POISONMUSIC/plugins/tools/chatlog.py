import asyncio
import random
import urllib.parse
from pyrogram import filters, errors, types
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional

from config import LOGGER_ID
from POISONMUSIC import app

BOT_INFO: Optional[types.User] = None
BOT_ID: Optional[int] = None

PHOTOS = [
    "https://te.legra.ph/file/17d19061f86cb1ebbddec.jpg"
]

def _is_valid_url(url: Optional[str]) -> bool:
    if not url:
        return False
    try:
        parsed = urllib.parse.urlparse(url.strip())
        return parsed.scheme in ("http", "https", "tg") and (parsed.netloc or parsed.path)
    except Exception:
        return False

async def _ensure_bot_info() -> None:
    global BOT_INFO, BOT_ID
    if BOT_INFO is None:
        try:
            BOT_INFO = await app.get_me()
            BOT_ID = BOT_INFO.id
        except Exception as e:
            print(f"Failed to get bot info: {e}")

async def safe_send_photo(chat_id, photo, caption, reply_markup=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await app.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                reply_markup=reply_markup
            )
        except errors.FloodWait as e:
            await asyncio.sleep(e.value + 1)
        except errors.ButtonUrlInvalid:
            return await app.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption
            )
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed to send photo after {max_retries} attempts: {e}")
                raise
            await asyncio.sleep(1)

@app.on_message(filters.new_chat_members)
async def join_watcher(_, message: Message):
    try:
        await _ensure_bot_info()
        if BOT_INFO is None or BOT_ID is None:
            return

        chat = message.chat
        try:
            invite_link = await app.export_chat_invite_link(chat.id)
        except Exception:
            invite_link = None

        for member in message.new_chat_members:
            if member.id != BOT_ID:
                continue

            member_count = "?"
            try:
                member_count = await app.get_chat_members_count(chat.id)
            except errors.FloodWait as fw:
                await asyncio.sleep(fw.value + 1)
                member_count = await app.get_chat_members_count(chat.id)
            except Exception:
                pass

            caption = (
                "📝 **ϻυsɪᴄ ʙσᴛ ᴧᴅᴅєᴅ ɪη ᴧ ηєᴡ ɢʀσυᴘ**\n\n"
                "❅─────✧❅✦❅✧─────❅\n\n"
                f"📌 **ᴄʜᴧᴛ ηᴧϻє:** `{chat.title}`\n"
                f"🍂 **ᴄʜᴧᴛ ɪᴅ:** `{chat.id}`\n"
                f"🔐 **ᴄʜᴧᴛ ᴜsєʀηᴧϻє:** @{chat.username if chat.username else 'Private'}\n"
                f"🛰 **ᴄʜᴧᴛ ʟɪηᴋ:** [ᴄʟɪᴄᴋ ʜᴇʀᴇ]({invite_link or 'https://t.me/'})\n"
                f"📈 **ɢʀσυᴘ ϻєϻʙєʀs:** `{member_count}`\n"
                f"🤔 **ᴧᴅᴅєᴅ ʙʏ:** {message.from_user.mention if message.from_user else 'Unknown'}"
            )

            reply_markup = None
            if _is_valid_url(invite_link):
                reply_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("sᴇᴇ ɢʀᴏᴜᴘ 👀", url=invite_link.strip())]]
                )

            await safe_send_photo(
                LOGGER_ID,
                photo=random.choice(PHOTOS),
                caption=caption,
                reply_markup=reply_markup
            )
    except Exception as e:
        print(f"Error in join_watcher: {e}")

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    try:
        await _ensure_bot_info()
        if BOT_INFO is None or BOT_ID is None:
            return

        if message.left_chat_member.id != BOT_ID:
            return

        remover = message.from_user.mention if message.from_user else "**ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ**"
        chat = message.chat

        text = (
            "✫ **<u>#ʟєғᴛ_ɢʀσυᴘ</u>** ✫\n\n"
            f"📌 **ᴄʜᴧᴛ ηᴧϻє:** `{chat.title}`\n"
            f"🆔 **ᴄʜᴧᴛ ɪᴅ:** `{chat.id}`\n"
            f"👤 **ʀєϻσᴠєᴅ ʙʏ:** {remover}\n"
            f"🤖 **ʙσᴛ:** @{BOT_INFO.username}"
        )

        max_retries = 3
        for attempt in range(max_retries):
            try:
                await app.send_message(LOGGER_ID, text)
                break
            except errors.FloodWait as e:
                await asyncio.sleep(e.value + 1)
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Failed to send left chat message after {max_retries} attempts: {e}")
    except Exception as e:
        print(f"Error in on_left_chat_member: {e}")
