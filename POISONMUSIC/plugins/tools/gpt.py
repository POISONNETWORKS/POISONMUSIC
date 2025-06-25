import asyncio
import os
from gtts import gTTS

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction

from lexica import AsyncClient, languageModels, Messages
from POISONMUSIC import app


def extract_content(response) -> str:
    if isinstance(response, dict):
        return response.get("content", "No content available.")
    return str(response)


async def get_gpt_response(prompt: str) -> str:
    lexica_client = AsyncClient()
    try:
        messages = [Messages(content=prompt, role="user")]
        response = await lexica_client.ChatCompletion(messages, languageModels.gpt)
        return extract_content(response)
    finally:
        await lexica_client.close()


async def safe_gpt_response(prompt: str, timeout: int = 30) -> str:
    try:
        return await asyncio.wait_for(get_gpt_response(prompt), timeout=timeout)
    except asyncio.TimeoutError:
        raise Exception("⚠️ GPT request timed out. Please try a shorter prompt.")
    except Exception as e:
        raise Exception(f"❌ GPT Error: {e}")


async def send_typing_action(client: Client, chat_id: int, interval: int = 3):
    try:
        while True:
            await client.send_chat_action(chat_id, ChatAction.TYPING)
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        pass


async def process_query(client: Client, message: Message, tts: bool = False):
    if len(message.command) < 2:
        return await message.reply_text(
            f"Hello {message.from_user.first_name}, how can I assist you today?"
        )

    query = message.text.split(" ", 1)[1].strip()

    if len(query) > 4000:
        return await message.reply_text("❌ Your prompt is too long (max 4000 characters). Please shorten it.")

    audio_file = "response.mp3"
    typing_task = asyncio.create_task(send_typing_action(client, message.chat.id))

    try:
        content = await safe_gpt_response(query, timeout=30)

        if not content:
            return await message.reply_text("⚠️ No response from GPT.")

        if tts:
            if len(content) > 1000:
                content = content[:1000] + "..."
            tts_engine = gTTS(text=content, lang="en")
            tts_engine.save(audio_file)
            await client.send_voice(chat_id=message.chat.id, voice=audio_file)
        else:
            if len(content) > 4096:
                for i in range(0, len(content), 4096):
                    await message.reply_text(content[i:i+4096])
            else:
                await message.reply_text(content)

    except Exception as e:
        await message.reply_text(str(e))

    finally:
        typing_task.cancel()
        if os.path.exists(audio_file):
            os.remove(audio_file)


@app.on_message(filters.command(["oison","am","ahto"], prefixes=["p", "P", "r", "R", "m", "M"]))
async def poison_ram_handler(client: Client, message: Message):
    try:
        await asyncio.wait_for(process_query(client, message), timeout=60)
    except asyncio.TimeoutError:
        await message.reply_text("⏳ Timeout. Please try again with a shorter prompt.")


@app.on_message(filters.command(["chatgpt", "ai", "ask", "Master"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def chatgpt_handler(client: Client, message: Message):
    try:
        await asyncio.wait_for(process_query(client, message), timeout=60)
    except asyncio.TimeoutError:
        await message.reply_text("⏳ Timeout. Please try again with a shorter prompt.")


@app.on_message(filters.command(["ssis"], prefixes=["a", "A"]))
async def poison_tts_handler(client: Client, message: Message):
    try:
        await asyncio.wait_for(process_query(client, message, tts=True), timeout=60)
    except asyncio.TimeoutError:
        await message.reply_text("⏳ Timeout. Please try again with a shorter prompt.")
