from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from POISONMUSIC import app


@app.on_message(filters.command("id"))
async def get_id(client, message: Message):
    chat, user, reply = message.chat, message.from_user, message.reply_to_message
    out = []

    if message.link:
        out.append(f"**[ϻєssᴧɢє ɪᴅ:]({message.link})** `{message.id}`")
    else:
        out.append(f"**ϻєssᴧɢє ɪᴅ:** `{message.id}`")

    out.append(f"**[ʏσυʀ ɪᴅ:](tg://user?id={user.id})** `{user.id}`")

    if len(message.command) == 2:
        try:
            target = message.text.split(maxsplit=1)[1]
            tgt_user = await client.get_users(target)
            out.append(f"**[υsєʀ ɪᴅ:](tg://user?id={tgt_user.id})** `{tgt_user.id}`")
        except Exception:
            return await message.reply_text("**ᴛʜɪs υsєʀ ᴅσєsη'ᴛ єxɪsᴛ.**", quote=True)

    if chat.username and chat.type != "private":
        out.append(f"**[ᴄʜᴧᴛ ɪᴅ:](https://t.me/{chat.username})** `{chat.id}`")
    else:
        out.append(f"**ᴄʜᴧᴛ ɪᴅ:** `{chat.id}`")

    if reply:
        if reply.link:
            out.append(f"**[ʀєᴘʟɪєᴅ ϻєssᴧɢє ɪᴅ:]({reply.link})** `{reply.id}`")
        else:
            out.append(f"**ʀєᴘʟɪєᴅ ϻєssᴧɢє ɪᴅ:** `{reply.id}`")

        if reply.from_user:
            out.append(
                f"**[ʀєᴘʟɪєᴅ υsєʀ ɪᴅ:](tg://user?id={reply.from_user.id})** "
                f"`{reply.from_user.id}`"
            )

        if reply.forward_from_chat:
            out.append(
                f"ᴛʜє ғσʀᴡᴧʀᴅєᴅ ᴄʜᴧηηєʟ **{reply.forward_from_chat.title}** "
                f"ʜᴧs ɪᴅ `{reply.forward_from_chat.id}`"
            )

        if reply.sender_chat:
            out.append(f"ɪᴅ σғ ᴛʜє ʀєᴘʟɪєᴅ ᴄʜᴧᴛ/ᴄʜᴧηηєʟ: `{reply.sender_chat.id}`")

    await message.reply_text(
        "\n".join(out),
        disable_web_page_preview=True,
        parse_mode=ParseMode.MARKDOWN,
    )
