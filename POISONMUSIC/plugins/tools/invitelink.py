import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from POISONMUSIC import app
from POISONMUSIC.misc import SUDOERS


@app.on_message(filters.command("givelink"))
async def give_link_command(client: Client, message: Message):
    try:
        link = await app.export_chat_invite_link(message.chat.id)
        await message.reply_text(
            f"🔗 **ɪηᴠɪᴛє ʟɪηᴋ ғσʀ** `{message.chat.title}`:\n{link}"
        )
    except Exception as e:
        await message.reply_text(f"❌ єʀʀσʀ ɢєηєʀᴧᴛɪηɢ ʟɪηᴋ:\n`{e}`")


@app.on_message(filters.command(["link", "invitelink"], prefixes=["/", "!", ".", "#", "?"]) & SUDOERS)
async def link_command_handler(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply("**υsᴧɢє:** `/link <group_id>`")

    group_id = message.command[1]
    file_name = f"group_info_{group_id}.txt"

    try:
        chat = await client.get_chat(int(group_id))
        if not chat:
            return await message.reply("⚠️ **ᴄσυʟᴅ ησᴛ ғєᴛᴄʜ ɢʀσυᴘ ɪηғσ.**")

        try:
            invite_link = await client.export_chat_invite_link(chat.id)
        except FloodWait as e:
            return await message.reply(f"⏳ ʀᴧᴛє ʟɪϻɪᴛ: ᴡᴧɪᴛ `{e.value}` seconds.")

        group_data = {
            "id": chat.id,
            "type": str(chat.type),
            "title": chat.title,
            "members_count": chat.members_count,
            "description": chat.description,
            "invite_link": invite_link,
            "is_verified": chat.is_verified,
            "is_restricted": chat.is_restricted,
            "is_creator": chat.is_creator,
            "is_scam": chat.is_scam,
            "is_fake": chat.is_fake,
            "dc_id": chat.dc_id,
            "has_protected_content": chat.has_protected_content,
        }

        with open(file_name, "w", encoding="utf-8") as file:
            for key, value in group_data.items():
                file.write(f"{key}: {value}\n")

        await client.send_document(
            chat_id=message.chat.id,
            document=file_name,
            caption=(
                f"📂 **ɢʀσυᴘ ɪηғσ ꜰσʀ** `{chat.title}`\n"
                f"📌 **sᴄʀᴧᴘєᴅ ʙʏ:** @{app.username}"
            ),
        )

    except Exception as e:
        await message.reply_text(f"❌ єʀʀσʀ:\n`{str(e)}`")

    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
