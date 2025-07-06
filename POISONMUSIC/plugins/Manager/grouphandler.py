from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from POISONMUSIC import app
from POISONMUSIC.utils.admin_filters import admin_filter

# ------------------- Utility Functions ------------------- #

def is_group(message: Message) -> bool:
    return message.chat.type not in [ChatType.PRIVATE, ChatType.BOT]

async def has_permission(user_id: int, chat_id: int, permission: str) -> bool:
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return getattr(member.privileges, permission, False)
    except Exception:
        return False

# ------------------- Pin Message ------------------- #

@app.on_message(filters.command("pin") & admin_filter)
async def pin(_, message: Message):
    if not is_group(message):
        return await message.reply_text("**ᴛʜɪs ᴄσϻϻᴧηᴅ ᴡσʀᴋs σηʟʏ ɪη ɢʀσυᴘs!**")

    if not message.reply_to_message:
        return await message.reply_text("**ʀєᴘʟʏ ᴛσ ᴧ ϻєssᴧɢє ᴛσ ᴘɪη ɪᴛ!**")

    if not await has_permission(message.from_user.id, message.chat.id, "can_pin_messages"):
        return await message.reply_text("**ʏσυ ᴅση'ᴛ ʜᴧᴠє ᴘєʀϻɪssɪση ᴛσ ᴘɪη ϻєssᴧɢєs.**")

    try:
        await message.reply_to_message.pin()
        await message.reply_text(
            f"**sυᴄᴄєssғυʟʟʏ ᴘɪηηєᴅ ϻєssᴧɢє!**\n\n**ᴄʜᴧᴛ:** {message.chat.title}\n**ᴧᴅϻɪη:** {message.from_user.mention}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📝 ᴠɪєᴡ ϻєssᴧɢє", url=message.reply_to_message.link)]]
            )
        )
    except Exception as e:
        await message.reply_text(f"**ғᴧɪʟєᴅ ᴛσ ᴘɪη ϻєssᴧɢє:**\n`{str(e)}`")

# ------------------- Unpin Message ------------------- #

@app.on_message(filters.command("unpin") & admin_filter)
async def unpin(_, message: Message):
    if not is_group(message):
        return await message.reply_text("**ᴛʜɪs ᴄσϻϻᴧηᴅ ᴡσʀᴋs σηʟʏ ɪη ɢʀσυᴘs!**")

    if not message.reply_to_message:
        return await message.reply_text("**ʀєᴘʟʏ ᴛσ ᴧ ϻєssᴧɢє ᴛσ υηᴘɪη ɪᴛ!**")

    if not await has_permission(message.from_user.id, message.chat.id, "can_pin_messages"):
        return await message.reply_text("**ʏσυ ᴅση'ᴛ ʜᴧᴠє ᴘєʀϻɪssɪση ᴛσ υηᴘɪη ϻєssᴧɢєs.**")

    try:
        await message.reply_to_message.unpin()
        await message.reply_text(
            f"**sυᴄᴄєssғυʟʟʏ υηᴘɪηηєᴅ ϻєssᴧɢє!**\n\n**ᴄʜᴧᴛ:** {message.chat.title}\n**ᴧᴅϻɪη:** {message.from_user.mention}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📝 ᴠɪєᴡ ϻєssᴧɢє", url=message.reply_to_message.link)]]
            )
        )
    except Exception as e:
        await message.reply_text(f"**ғᴧɪʟєᴅ ᴛσ υηᴘɪη ϻєssᴧɢє:**\n`{str(e)}`")

# ------------------- Set / Remove Photo, Title, Description ------------------- #

@app.on_message(filters.command("setphoto") & admin_filter)
async def set_photo(_, message: Message):
    if not is_group(message):
        return await message.reply_text("**ᴛʜɪs ᴄσϻϻᴧηᴅ ᴡσʀᴋs σηʟʏ ɪη ɢʀσυᴘs!**")
    if not message.reply_to_message:
        return await message.reply_text("**ʀєᴘʟʏ ᴛσ ᴧ ᴘʜσᴛσ σʀ ᴅσᴄυϻєηᴛ.**")
    if not await has_permission(message.from_user.id, message.chat.id, "can_change_info"):
        return await message.reply_text("**ʏσυ ʟᴧᴄᴋ ᴘєʀϻɪssɪση ᴛσ ᴄʜᴧηɢє ɢʀσυᴘ ɪηғσ.**")
    try:
        photo = await message.reply_to_message.download()
        await message.chat.set_photo(photo=photo)
        await message.reply_text(f"**ɢʀσυᴘ ᴘʜσᴛσ υᴘᴅᴧᴛєᴅ sυᴄᴄєssғυʟʟʏ!**\nʙʏ {message.from_user.mention}")
    except Exception as e:
        await message.reply_text(f"**ғᴧɪʟєᴅ ᴛσ sєᴛ ᴘʜσᴛσ:**\n`{str(e)}`")


@app.on_message(filters.command("removephoto") & admin_filter)
async def remove_photo(_, message: Message):
    if not is_group(message):
        return await message.reply_text("**ᴛʜɪs ᴄσϻϻᴧηᴅ ᴡσʀᴋs σηʟʏ ɪη ɢʀσυᴘs!**")
    if not await has_permission(message.from_user.id, message.chat.id, "can_change_info"):
        return await message.reply_text("**ʏσυ ʟᴧᴄᴋ ᴘєʀϻɪssɪση ᴛσ ᴄʜᴧηɢє ɢʀσυᴘ ɪηғσ.**")
    try:
        await app.delete_chat_photo(message.chat.id)
        await message.reply_text(f"**ɢʀσυᴘ ᴘʜσᴛσ ʀєϻσᴠєᴅ!**\nʙʏ {message.from_user.mention}")
    except Exception as e:
        await message.reply_text(f"**ғᴧɪʟєᴅ ᴛσ ʀєϻσᴠє ᴘʜσᴛσ:**\n`{str(e)}`")


@app.on_message(filters.command("settitle") & admin_filter)
async def set_title(_, message: Message):
    if not is_group(message):
        return await message.reply_text("**ᴛʜɪs ᴄσϻϻᴧηᴅ ᴡσʀᴋs σηʟʏ ɪη ɢʀσυᴘs!**")
    if not await has_permission(message.from_user.id, message.chat.id, "can_change_info"):
        return await message.reply_text("**ʏσυ ʟᴧᴄᴋ ᴘєʀϻɪssɪση ᴛσ ᴄʜᴧηɢє ɢʀσυᴘ ɪηғσ.**")

    title = message.text.split(None, 1)[1] if len(message.command) > 1 else (message.reply_to_message.text if message.reply_to_message else None)
    if not title:
        return await message.reply_text("**ᴘʟєᴧsє ᴘʀσᴠɪᴅє ᴧ ηєᴡ ᴛɪᴛʟє.**")

    try:
        await message.chat.set_title(title)
        await message.reply_text(f"**ɢʀσυᴘ ηᴧϻє ᴄʜᴧηɢєᴅ ᴛσ:** {title}\nʙʏ {message.from_user.mention}")
    except Exception as e:
        await message.reply_text(f"**ғᴧɪʟєᴅ ᴛσ sєᴛ ᴛɪᴛʟє:**\n`{str(e)}`")


@app.on_message(filters.command("setdiscription") & admin_filter)
async def set_description(_, message: Message):
    if not is_group(message):
        return await message.reply_text("**ᴛʜɪs ᴄσϻϻᴧηᴅ ᴡσʀᴋs σηʟʏ ɪη ɢʀσυᴘs!**")
    if not await has_permission(message.from_user.id, message.chat.id, "can_change_info"):
        return await message.reply_text("**ʏσυ ʟᴧᴄᴋ ᴘєʀϻɪssɪση ᴛσ ᴄʜᴧηɢє ɢʀσυᴘ ɪηғσ.**")

    desc = message.text.split(None, 1)[1] if len(message.command) > 1 else (message.reply_to_message.text if message.reply_to_message else None)
    if not desc:
        return await message.reply_text("**ᴘʟєᴧsє ᴘʀσᴠɪᴅє ᴧ ηєᴡ ᴅєsᴄʀɪᴘᴛɪση.**")

    try:
        await message.chat.set_description(desc)
        await message.reply_text(f"**ɢʀσυᴘ ᴅєsᴄʀɪᴘᴛɪση υᴘᴅᴧᴛєᴅ!**\nʙʏ {message.from_user.mention}")
    except Exception as e:
        await message.reply_text(f"**ғᴧɪʟєᴅ ᴛσ sєᴛ ᴅєsᴄʀɪᴘᴛɪση:**\n`{str(e)}`")
