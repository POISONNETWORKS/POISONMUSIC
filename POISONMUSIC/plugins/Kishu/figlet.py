import pyfiglet
from random import choice
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from POISONMUSIC import app

import base64

def figle(text: str):
    fonts = pyfiglet.FigletFont.getFonts()
    font = choice(fonts)
    figlet_text = pyfiglet.figlet_format(text, font=font)
    encoded_text = base64.b64encode(text.encode()).decode()
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="🌀 ᴄʜᴧηɢє", callback_data=f"figlet_{encoded_text}"),
            InlineKeyboardButton(text="❌ ᴄʟσsє", callback_data="close_reply")
        ]
    ])
    return figlet_text, keyboard

@app.on_message(filters.command("figlet"))
async def figlet_command(client, message):
    try:
        text = message.text.split(' ', 1)[1]
    except IndexError:
        return await message.reply_text("✏️ Example:\n`/figlet POISON`", quote=True)

    figlet_result, keyboard = figle(text)
    await message.reply_text(
        f"✨ ʜєʀє ɪs ʏσυʀ ғɪɢʟєᴛ:\n<pre>{figlet_result}</pre>",
        quote=True,
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex(r"^figlet_"))
async def figlet_callback(_, query: CallbackQuery):
    try:
        encoded_text = query.data.split("_", 1)[1]
        text = base64.b64decode(encoded_text).decode()
        figlet_result, keyboard = figle(text)
        await query.message.edit_text(
            f"✨ ʜєʀє ɪs ʏσυʀ ғɪɢʟєᴛ:\n<pre>{figlet_result}</pre>",
            reply_markup=keyboard
        )
    except Exception as e:
        await query.answer("Error: Cannot update figlet", show_alert=True)

@app.on_callback_query(filters.regex("close_reply"))
async def close_reply(_, query: CallbackQuery):
    try:
        await query.message.delete()
    except:
        await query.answer("❌ Message already deleted.", show_alert=True)
