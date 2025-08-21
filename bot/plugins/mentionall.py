import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from ..permissions import is_admin

BATCH = 20

@Client.on_message(filters.command("mentionall"))
async def mention_all(c: Client, m: Message):
    if not await is_admin(c, m.chat.id, m.from_user.id):
        return await m.reply_text("Admins only.")

    if len(m.command) > 1:
        base_text = m.text.split(maxsplit=1)[1]
    elif m.reply_to_message and (m.reply_to_message.text or m.reply_to_message.caption):
        base_text = m.reply_to_message.text or m.reply_to_message.caption
    else:
        base_text = ""

    members = []
    async for u in c.get_chat_members(m.chat.id):
        if u.user.is_bot:
            continue
        members.append(u.user)

    chunks = [members[i:i+BATCH] for i in range(0, len(members), BATCH)]
    for chunk in chunks:
        text = base_text + "\n\n" + " ".join(u.mention for u in chunk)
        await c.send_message(m.chat.id, text)
        await asyncio.sleep(0.7)
