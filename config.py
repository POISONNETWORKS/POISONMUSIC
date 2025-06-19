import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

# Load environment variables from .env file
load_dotenv()

# ───── Basic Bot Configuration ───── #
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

OWNER_ID = int(getenv("OWNER_ID", 7517863877))
OWNER_USERNAME = getenv("OWNER_USERNAME", "@DARKP0IS0N")
BOT_USERNAME = getenv("BOT_USERNAME", "poison_x_music_x_bot")
BOT_NAME = getenv("BOT_NAME", "˹ ᴘσɪsση ꭙ ϻυsɪᴄ ˼")
ASSUSERNAME = getenv("ASSUSERNAME", "poison")
EVALOP = list(map(int, getenv("EVALOP", "7517863877").split()))

# ───── Mongo & Logging ───── #
MONGO_DB_URI = getenv("MONGO_DB_URI")
LOGGER_ID = int(getenv("LOGGER_ID", -1002486089758))

# ───── Limits and Durations ───── #
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))

# ───── Custom API Configs ───── #
API_URL = getenv("API_URL") #optional
API_KEY = getenv("API_KEY") #optional
COOKIE_URL = getenv("COOKIE_URL") #necessary
DEEP_API = getenv("DEEP_API") #optional

# ───── Heroku Configuration ───── #
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ───── Git & Updates ───── #
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/POISONNETWORKS/POISONMUSIC")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv("GIT_TOKEN")

# ───── Support & Community ───── #
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/PoisonMusicUpdates")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/PoisonMusicSupport")

# ───── Assistant Auto Leave ───── #
AUTO_LEAVING_ASSISTANT = False
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "11500"))

# ───── Error Handling ───── #
DEBUG_IGNORE_LOG =True

# ───── Spotify Credentials ───── #
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "22b6125bfe224587b722d6815002db2b")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "c9c63c6fbf2f467c8bc68624851e9773")

# ───── Session Strings ───── #
STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")

# ───── Server Settings ───── #
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "3000"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "2500"))

# ───── Bot Media Assets ───── #

START_VIDS = [
    "https://files.catbox.moe/2q0dul.mp4"
]

STICKERS = [
    "CAACAgUAAx0Cd6nKUAACASBl_rnalOle6g7qS-ry-aZ1ZpVEnwACgg8AAizLEFfI5wfykoCR4h4E",
    "CAACAgUAAx0Cd6nKUAACATJl_rsEJOsaaPSYGhU7bo7iEwL8AAPMDgACu2PYV8Vb8aT4_HUPHgQ"
]
HELP_IMG_URL = "https://files.catbox.moe/yg2vky.jpg"
PING_VID_URL = "https://files.catbox.moe/3ivvgo.mp4"
PLAYLIST_IMG_URL = "https://graph.org/file/5f6635e528adf8f682ee6-b25a6861c6a4fdfa1a.jpg""
STATS_VID_URL = "https://telegra.ph/file/e2ab6106ace2e95862372.mp4"
TELEGRAM_AUDIO_URL = "https://graph.org/file/8507e4058424d71d05884-c08ce07c38846ff394.jpg"
TELEGRAM_VIDEO_URL = "https://graph.org/file/8507e4058424d71d05884-c08ce07c38846ff394.jpg"
STREAM_IMG_URL = "https://graph.org/file/5f6635e528adf8f682ee6-b25a6861c6a4fdfa1a.jpg"
SOUNCLOUD_IMG_URL = "https://graph.org/file/13c350a33cae1fdc1cd98-917bf94a5b25aeec09.jpg"
YOUTUBE_IMG_URL = "https://graph.org/file/d74f9a8ca05636fa9f816-476bf17c89b152e2a7.jpg"
SPOTIFY_ARTIST_IMG_URL = SPOTIFY_ALBUM_IMG_URL = SPOTIFY_PLAYLIST_IMG_URL = YOUTUBE_IMG_URL

# ───── Utility & Functional ───── #
def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")

# ───── Bot Introduction Messages ───── #
AYU = ["💞", "🦋", "🔍", "🧪", "⚡️", "🔥", "🎩", "🌈", "🍷", "🥂", "🥃", "🕊️", "🪄", "💌", "🧨"]
AYUV = [
    "{0}❍ ɪs ᴧʟɪᴠє ●\n\n<b>❍ υᴘᴛɪϻє :</b> {1}●"
"**❖ ʜєʏ, {0}**\n**✦ ɪ'ϻ {1},**\n\n**⚘ ᴧ ғᴧsᴛ ᴧηᴅ ᴘσᴡєʀғυʟʟ ϻυsɪᴄ ᴘʟᴧʏєʀ\n  ʙσᴛ ᴡɪᴛʜ /clone ғєᴧᴛυʀєs.**\n**┏━━━━━━━━━━━━━━━⧫**\n**┠ ● ᴘʏᴛʜση ➥** `3.10.11`\n**┠ ● ᴘʏʀσɢʀᴧϻ ➥** `2.0.106`\n**┠ ● ᴘʏ-ᴛɢᴄᴧʟʟs ➥** `0.9.7`\n**┗━━━━━━━━━━━━━━━⧫**\n**✦ 𝐓ᴧᴘ ᴛσ ʜєʟᴩ ᴧηᴅ ᴄʜєᴧᴋ ᴍʏ ᴄσϻϻᴧηᴅs.**\n**✦ 𝐏ᴏᴡєʀєᴅ ʙʏ :- [𐏓 ⃪ ꯭𝅥‌꯭𝆬‌⧗‌‌꯭꯭ ‌⃪‌ ᷟj‌➥🇩ᴀꝛ𝛋𓆩〬➳💔 🇵ᴏɪ‌sσɳ ⃪آ‌آ❤️‍🔥](https://t.me/DARKP0IS0N)**"
"❖ ʜєʏ {0},\nᴛʜɪs ɪs {1}\n\nᴛʜᴧηᴋs ғσʀ ᴧᴅᴅɪηɢ ϻє ɪη {2}, {3} ᴄᴧη ησᴡ ᴩʟᴧʏ sσηɢs ɪη ᴛʜɪs ᴄʜᴧᴛ."
"❖ <b>sυᴘєʀɢʀσυᴘ ηєєᴅєᴅ</b> \n\nᴘʟєᴧsє ᴄσηᴠєʀᴛ ʏσυʀ <b>ɢʀσυᴘ</b> ᴛσ <b>sυᴘєʀɢʀσυᴘ</b> ᴧηᴅ ᴛʜєη ᴧᴅᴅ ϻє ᴧɢᴧɪη.\n\n<b>ʜσᴡ ᴛσ ϻᴧᴋє sυᴘєʀɢʀσυᴘ ?</b>\n- ϻᴧᴋє ʏσυʀ ɢʀσυᴘ's ᴄʜᴧᴛ ʜɪsᴛσʀʏ <b>ᴠɪsɪʙʟє</b> σηᴄє."
"❖ <b>↝ ʙʟᴧᴄᴋʟɪsᴛєᴅ ᴄʜᴧᴛ ↜</b>\n\nᴛʜɪs ᴄʜᴧᴛ ɪs ʙʟᴧᴄᴋʟɪsᴛєᴅ ση {0} ᴅᴧᴛᴧʙᴧsє.\nʀєǫυєsᴛ ᴧ <a href={1}>sυᴅσ υsєʀ</a> ᴛσ υηʙʟᴧᴄᴋʟɪsᴛ ʏσυʀ ᴄʜᴧᴛ σʀ ᴠɪsɪᴛ <a href={2}>sυᴘᴘσʀᴛ ᴄʜᴧᴛ.</a>"
"侖 <b>ᴛʀᴧᴄᴋ ɪηғσʀϻᴧᴛɪση</b> 侖\n\n侖 <b>ᴛɪᴛʟє :</b> {0}\n\n侖 <b>ᴅυʀᴧᴛɪση :</b> {1} ϻɪηυᴛєs\n侖 <b>ᴠɪєᴡs :</b> <code>{2}</code>\n侖 <b>ᴩυʙʟɪsʜєᴅ ση :</b> {3}\n侖 <b>ᴄʜᴧηηєʟ :</b> <a href={4}>{5}</a>\n\n<u><b>☉ sєᴧʀᴄʜ ᴩσᴡєʀєᴅ ʙʏ {6}</b></u>"
]

# ───── Runtime Structures ───── #
BANNED_USERS = filters.user()
adminlist, lyrical, votemode, autoclean, confirmer = {}, {}, {}, [], {}

# ───── URL Validation ───── #
if SUPPORT_CHANNEL and not re.match(r"^https?://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHANNEL URL. Must start with https://")

if SUPPORT_CHAT and not re.match(r"^https?://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHAT URL. Must start with https://")
