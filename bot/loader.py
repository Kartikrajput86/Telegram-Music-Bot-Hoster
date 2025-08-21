import asyncio
from pyrogram import Client
from pyrogram.enums import ParseMode
from .config import CFG
from .player import VoicePlayer
from .strings import START_ANIM_FRAMES
from .utils import logger

BOT = Client(
    name="music-bot",
    api_id=CFG.api_id,
    api_hash=CFG.api_hash,
    bot_token=CFG.bot_token,
    parse_mode=ParseMode.HTML,
    in_memory=True,
)

ASSISTANT = Client(
    name="assistant",
    api_id=CFG.api_id,
    api_hash=CFG.api_hash,
    session_string=CFG.assistant_session,
    parse_mode=ParseMode.HTML,
    in_memory=True,
)

PLAYER = VoicePlayer(assistant_client=ASSISTANT, config=CFG)

async def start_all():
    await ASSISTANT.start()
    await BOT.start()

    await BOT.import_plugins("bot.plugins")

    BOT.set_parse_mode("html")
    BOT.set_attribute("player", PLAYER)
    BOT.set_attribute("assistant", ASSISTANT)
    BOT.set_attribute("config", CFG)

    await PLAYER.start()
    logger.info("Bot and Assistant started.")
    await asyncio.get_event_loop().create_future()
