from pyrogram import filters
from pyrogram.types import Message
from POISONMUSIC import app
from gpytranslate import Translator

translator = Translator()


@app.on_message(filters.command("tr"))
async def translate(_, message: Message):
    reply = message.reply_to_message

    if not reply or not (reply.text or reply.caption):
        return await message.reply_text("📌 ʀєᴘʟʏ ᴛσ ᴧ ᴛєxᴛ σʀ ᴄᴧᴘᴛɪση ᴛσ ᴛʀᴧηsʟᴧᴛє.")

    content = reply.text or reply.caption

    try:
        arg = message.text.split(maxsplit=1)[1].lower()
        if "//" in arg:
            source_lang, target_lang = arg.split("//")
        else:
            source_lang = await translator.detect(content)
            target_lang = arg
    except IndexError:
        source_lang = await translator.detect(content)
        target_lang = "en"

    try:
        result = await translator(content, sourcelang=source_lang, targetlang=target_lang)
        await message.reply_text(
            f"🌐 **ᴛʀᴧηsʟᴧᴛєᴅ:** `{source_lang}` ➜ `{target_lang}`\n\n"
            f"`{result.text}`"
        )
    except Exception as e:
        await message.reply_text(f"❌ **ᴛʀᴧηsʟᴧᴛɪση ꜰᴧɪʟєᴅ:** `{str(e)}`")
