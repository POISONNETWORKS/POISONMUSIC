import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from POISONMUSIC import app


@app.on_message(filters.command(["github", "git"]))
async def github(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("**υsᴧɢє:** `/git <username>`")

    username = message.text.split(None, 1)[1]
    url = f"https://api.github.com/users/{username}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 404:
                return await message.reply_text("🚫 **υsєʀ ησᴛ ғσυηᴅ!**")
            elif response.status != 200:
                return await message.reply_text("⚠️ **єʀʀσʀ ғєᴛᴄʜɪηɢ ᴅᴧᴛᴧ!**")

            data = await response.json()

    name = data.get("name", "Not specified")
    bio = data.get("bio", "No bio available.")
    blog = data.get("blog", "N/A")
    location = data.get("location", "Unknown")
    company = data.get("company", "N/A")
    created = data.get("created_at", "N/A")
    url = data.get("html_url", "N/A")
    repos = data.get("public_repos", "0")
    followers = data.get("followers", "0")
    following = data.get("following", "0")
    avatar = data.get("avatar_url", None)

    caption = f"""
✨ **ɢɪᴛʜυʙ ᴘʀσғɪʟє ɪηꜰσ**

👤 **ηᴧϻє:** `{name}`
🔧 **υsєʀηᴧϻє:** `{username}`
📌 **ʙɪσ:** {bio}
🏢 **ᴄσϻᴘᴧηʏ:** {company}
📍 **ʟσᴄᴧᴛɪση:** {location}
🌐 **ʙʟσɢ:** {blog}
🗓 **ᴄʀєᴧᴛєᴅ ση:** `{created}`
📁 **ᴘυʙʟɪᴄ ʀєᴘσs:** `{repos}`
👥 **ғσʟʟσᴡєʀs:** `{followers}` | **ғσʟʟσᴡɪηɢ:** `{following}`
🔗 **ᴘʀσғɪʟє:** [ᴠɪєᴡ ση ɢɪᴛʜυʙ]({url})
""".strip()

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("❌ ᴄʟσsє", callback_data="close")]]
    )

    if avatar:
        await message.reply_photo(photo=avatar, caption=caption, reply_markup=keyboard)
    else:
        await message.reply_text(caption, reply_markup=keyboard)
