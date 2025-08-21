from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(["gban", "g-unban", "auth", "bl-chat", "bl-user"]))
async def placeholders(c: Client, m: Message):
    await m.reply_text("Admin/Auth/GBan/Blacklist features are placeholders in this build. Add your logic here.")
