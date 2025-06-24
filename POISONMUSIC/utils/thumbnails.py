import os
import re
import random
import aiohttp
import aiofiles
import traceback

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch


def changeImageSize(maxWidth, maxHeight, image):
    ratio = min(maxWidth / image.size[0], maxHeight / image.size[1])
    newSize = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    return image.resize(newSize, Image.ANTIALIAS)


def truncate(text, max_chars=50):
    words = text.split()
    text1, text2 = "", ""
    for word in words:
        if len(text1 + " " + word) <= max_chars and not text2:
            text1 += " " + word
        else:
            text2 += " " + word
    return [text1.strip(), text2.strip()]


def add_rounded_corners(im, radius):
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
    im.putalpha(alpha)
    return im


def fit_text(draw, text, max_width, font_path, start_size, min_size):
    size = start_size
    while size >= min_size:
        font = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 1
    return ImageFont.truetype(font_path, min_size)


async def get_thumb(videoid: str):
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            title = re.sub(r"\W+", " ", result.get("title", "Unsupported Title")).title()
            duration = result.get("duration", "Unknown Mins")
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            views = result.get("viewCount", {}).get("short", "Unknown Views")
            channel = result.get("channel", {}).get("name", "Unknown Channel")

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        icons = Image.open("POISONMUSIC/assets/icons.png")
        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")

        gradient = Image.new("RGBA", image2.size, (0, 0, 0, 255))
        enhancer = ImageEnhance.Brightness(image2.filter(ImageFilter.GaussianBlur(15)))
        blurred = enhancer.enhance(0.5)
        background = Image.alpha_composite(gradient, blurred)

        Xcenter = image2.width / 2
        Ycenter = image2.height / 2
        logo = youtube.crop((Xcenter - 200, Ycenter - 200, Xcenter + 200, Ycenter + 200))
        logo.thumbnail((340, 340), Image.ANTIALIAS)

        shadow = Image.new("RGBA", logo.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=(0, 0, 0, 100))
        background.paste(shadow, (110, 160), shadow)

        rand = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        logo = ImageOps.expand(logo, border=15, fill=rand)
        background.paste(logo, (100, 150))

        draw = ImageDraw.Draw(background)
        font_info = ImageFont.truetype("POISONMUSIC/assets/font2.ttf", 28)
        font_time = ImageFont.truetype("POISONMUSIC/assets/font2.ttf", 26)
        font_path = "POISONMUSIC/assets/font3.ttf"

        title_max_width = 540
        title_lines = truncate(title, 35)

        title_font1 = fit_text(draw, title_lines[0], title_max_width, font_path, 42, 28)
        draw.text((565, 180), title_lines[0], (255, 255, 255), font=title_font1)

        if title_lines[1]:
            title_font2 = fit_text(draw, title_lines[1], title_max_width, font_path, 36, 24)
            draw.text((565, 225), title_lines[1], (220, 220, 220), font=title_font2)

        draw.text((565, 305), f"{channel} | {views}", (240, 240, 240), font=font_info)

        draw.line([(565, 370), (1130, 370)], fill="white", width=6)
        draw.line([(565, 370), (990, 370)], fill=rand, width=6)
        draw.ellipse([(990, 362), (1010, 382)], outline=rand, fill=rand, width=12)

        draw.text((565, 385), "00:00", (255, 255, 255), font=font_time)
        draw.text((1080, 385), duration, (255, 255, 255), font=font_time)

        picons = icons.resize((580, 62))
        background.paste(picons, (565, 430), picons)

        watermark_font = ImageFont.truetype("POISONMUSIC/assets/font2.ttf", 24)
        watermark_text = "POISONMUSIC"
        text_size = draw.textsize(watermark_text, font=watermark_font)
        x = background.width - text_size[0] - 25
        y = background.height - text_size[1] - 25
        glow_pos = [(x + dx, y + dy) for dx in (-1, 1) for dy in (-1, 1)]
        for pos in glow_pos:
            draw.text(pos, watermark_text, font=watermark_font, fill=(0, 0, 0, 180))
        draw.text((x, y), watermark_text, font=watermark_font, fill=(255, 255, 255, 240))

        background = add_rounded_corners(background, 30)

        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass

        tpath = f"cache/{videoid}.png"
        background.save(tpath)
        return tpath

    except:
        traceback.print_exc()
        return None
