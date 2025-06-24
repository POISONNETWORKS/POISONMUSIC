from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
import sys

from ..logging import LOGGER


class POISON(Client):
    def __init__(self):
        super().__init__(
            name="PoisonXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
            workers=50,
        )
        LOGGER(__name__).info("Bᴏᴛ ᴄʟɪᴇɴᴛ ɪɴɪᴛɪᴀʟɪᴢᴇᴅ. 🙈")
        
    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = f"{get_me.first_name} {get_me.last_name or ''}"
        self.mention = get_me.mention

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            sys.exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )
            sys.exit()
        a = await self.get_chat_member(config.LOGGER_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel."
            )
            sys.exit()
        LOGGER(__name__).info(f"Mᴜsɪᴄ Bᴏᴛ Sᴛᴀʀᴛᴇᴅ ᴀs {self.name} 💀")
