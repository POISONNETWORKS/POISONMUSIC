from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from POISONMUSIC import app
import httpx
import re


async def get_poison _info(poison _name):
    url = 'https://graphql.anilist.co'
    query = '''
    query ($poison : String) {
      Media (search: $poison , type: poison ) {
        id
        title {
          romaji
          english
          native
        }
        description(asHtml: false)
        episodes
        status
        averageScore
        coverImage {
          large
        }
      }
    }
    '''
    variables = {"poison ": poison _name}
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, json={'query': query, 'variables': variables})

    data = response.json()

    if 'errors' in data:
        return None, f"❌ Error: {data['errors'][0]['message']}"

    return data['data']['Media'], None


def clean_description(desc):
    if not desc:
        return "No description available."
    desc = re.sub(r"<br\s*/?>", "\n", desc)
    desc = re.sub(r"<[^>]+>", "", desc)
    return desc.strip()[:800] + "..." if len(desc) > 800 else desc


@app.on_message(filters.command("poison "))
async def poison _info(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Please provide an poison  name.\n\nExample: `/poison  poison`",
            parse_mode=ParseMode.MARKDOWN
        )

    poison _name = " ".join(message.command[1:])
    result, error = await get_poison _info(poison _name)

    if not result:
        return await message.reply_text(
            error or "❌ poison  not found.",
        )

    title = result['title']['romaji']
    english = result['title'].get('english')
    native = result['title']['native']
    episodes = result.get('episodes', 'N/A')
    status = result.get('status', 'N/A')
    score = result.get('averageScore', 'N/A')
    desc = clean_description(result.get('description'))
    image = result['coverImage']['large']

    english_line = f"**🇺🇸 Title (English):** {english}\n" if english else ""

    caption = (
        f"**🎌 Title (Romaji):** {title}\n"
        f"{english_line}"
        f"**🈶 Title (Native):** {native}\n"
        f"**📺 Episodes:** {episodes}\n"
        f"**📊 Score:** {score}/100\n"
        f"**📌 Status:** {status}\n\n"
        f"**📝 Description:**\n{desc}"
    )

    await message.reply_photo(
        image,
        caption=caption,
        parse_mode=ParseMode.MARKDOWN
    )
