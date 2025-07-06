import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import MessageDeleteForbidden, RPCError, FloodWait
from pyrogram.types import Message

from POISONMUSIC import app
from POISONMUSIC.utils.admin_filters import admin_filter


def divide_chunks(l: list, n: int = 100):
    for i in range(0, len(l), n):
        yield l[i: i + n]


@app.on_message(filters.command("purge") & admin_filter)
async def purge(app: Client, msg: Message):
    if msg.chat.type != ChatType.SUPERGROUP:
        return await msg.reply("**ɪ ᴄᴧη'ᴛ ᴘυʀɢє ϻєssᴧɢєs ɪη ᴧ ʙᴧsɪᴄ ɢʀσυᴘ. ᴘʟєᴧsє ᴄσηᴠєʀᴛ ɪᴛ ᴛσ ᴧ sυᴘєʀɢʀσυᴘ.**")

    if not msg.reply_to_message:
        return await msg.reply("**ʀєᴘʟʏ ᴛσ ᴧ ϻєssᴧɢє ᴛσ sᴛᴧʀᴛ ᴘυʀɢє!**")

    message_ids = list(range(msg.reply_to_message.id, msg.id))
    m_list = list(divide_chunks(message_ids))

    try:
        for plist in m_list:
            try:
                await app.delete_messages(chat_id=msg.chat.id, message_ids=plist, revoke=True)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.value)
        await msg.delete()
        count = len(message_ids)
        confirm = await msg.reply(f"✅ | **ᴅєʟєᴛєᴅ `{count}` ϻєssᴧɢєs.**")
        await asyncio.sleep(3)
        await confirm.delete()
    except MessageDeleteForbidden:
        await msg.reply("**ɪ ᴄᴧη'ᴛ ᴅєʟєᴛє ϻєssᴧɢєs ɪη ᴛʜɪs ᴄʜᴧᴛ. ϻᴧʏ ʙє ᴛσσ σʟᴅ σʀ ησ ʀɪɢʜᴛs.**")
    except RPCError as e:
        await msg.reply(f"**єʀʀσʀ σᴄᴄυʀʀєᴅ:**\n<code>{e}</code>")


@app.on_message(filters.command("spurge") & admin_filter)
async def spurge(app: Client, msg: Message):
    if msg.chat.type != ChatType.SUPERGROUP:
        return await msg.reply("**ɪ ᴄᴧη'ᴛ ᴘυʀɢє ϻєssᴧɢєs ɪη ᴧ ʙᴧsɪᴄ ɢʀσυᴘ. ᴘʟєᴧsє ᴄσηᴠєʀᴛ ɪᴛ ᴛσ ᴧ sυᴘєʀɢʀσυᴘ.**")

    if not msg.reply_to_message:
        return await msg.reply("**ʀєᴘʟʏ ᴛσ ᴧ ϻєssᴧɢє ᴛσ sᴛᴧʀᴛ ᴘυʀɢє!**")

    message_ids = list(range(msg.reply_to_message.id, msg.id))
    m_list = list(divide_chunks(message_ids))

    try:
        for plist in m_list:
            try:
                await app.delete_messages(chat_id=msg.chat.id, message_ids=plist, revoke=True)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.value)
        await msg.delete()
    except MessageDeleteForbidden:
        await msg.reply("**ɪ ᴄᴧη'ᴛ ᴅєʟєᴛє ϻєssᴧɢєs ɪη ᴛʜɪs ᴄʜᴧᴛ.**")
    except RPCError as e:
        await msg.reply(f"**єʀʀσʀ σᴄᴄυʀʀєᴅ:**\n<code>{e}</code>")


@app.on_message(filters.command("del") & admin_filter)
async def del_msg(app: Client, msg: Message):
    if msg.chat.type != ChatType.SUPERGROUP:
        return await msg.reply("**ɪ ᴄᴧη'ᴛ ᴘυʀɢє ϻєssᴧɢєs ɪη ᴧ ʙᴧsɪᴄ ɢʀσυᴘ.**")

    if not msg.reply_to_message:
        return await msg.reply("**ᴡʜᴧᴛ ᴅσ ʏσυ ᴡᴧηᴛ ᴛσ ᴅєʟєᴛє?**")

    try:
        await msg.delete()
        await app.delete_messages(chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await msg.reply(f"**ғᴧɪʟєᴅ ᴛσ ᴅєʟєᴛє ϻєssᴧɢє:**\n<code>{e}</code>")
