import logging
import asyncio
from contextlib import suppress
from pyrogram.errors import FloodWait

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("musicbot")

async def safe_edit(msg, text):
    with suppress(Exception):
        return await msg.edit_text(text)

async def flood_safe(func, *args, **kwargs):
    try:
        return await func(*args, **kwargs)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await func(*args, **kwargs)
