from pyrogram import filters
from pyrogram.types import Message
from POISONMUSIC import app


@app.on_message(filters.command("groupinfo", prefixes="/"))
async def get_group_status(_, message: Message):
    if len(message.command) != 2:
        await message.reply(
            "Please provide a group username. Example: `/groupinfo YourGroupUsername`"
        )
        return

    group_username = message.command[1]

    try:
        group = await app.get_chat(group_username)
    except Exception as e:
        await message.reply(f"Error: {e}")
        return

    total_members = await app.get_chat_members_count(group.id)
    group_description = group.description or "N/A"
    group_username_display = f"@{group.username}" if group.username else "Private"

    response_text = (
        "▰▰▰▰▰▰▰▰▰\n"
        f"<b>➲ ɢʀσυᴘ ηᴧϻє : {group.title} ✅</b>\n"
        f"<b>➲ ɢʀσυᴘ ɪᴅ : `{group.id}`</b>\n"
        f"<b>➲ ᴛσᴛᴧʟ ϻєϻʙєʀs : {total_members}</b>\n"
        f"<b>➲ ᴅєsᴄʀɪᴘᴛɪση : `{group_description}`</b>\n"
        f"<b>➲ υsєʀηᴧϻє : {group_username_display}</b>\n"
        "▰▰▰▰▰▰▰▰▰"
    )

    await message.reply(response_text)
