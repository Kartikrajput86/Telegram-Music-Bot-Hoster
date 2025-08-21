from pyrogram import Client, filters
from pyrogram.types import Message
import time

@Client.on_message(filters.command("ping"))
async def ping(c: Client, m: Message):
    start = time.perf_counter()
    msg = await m.reply_text("Pinging…")
    delta = (time.perf_counter() - start) * 1000
    await msg.edit_text(f"Pong! <b>{delta:.0f} ms</b>")

@Client.on_message(filters.command(["id", "Id", "ID"]))
async def get_id(c: Client, m: Message):
    uid = m.from_user.id if m.from_user else 0
    cid = m.chat.id
    tid = m.id
    await m.reply_text(f"<b>Chat:</b> <code>{cid}</code>\n<b>User:</b> <code>{uid}</code>\n<b>Message:</b> <code>{tid}</code>")

@Client.on_message(filters.command("info"))
async def info(c: Client, m: Message):
    if m.reply_to_message and m.reply_to_message.from_user:
        u = m.reply_to_message.from_user
    else:
        u = m.from_user
    await m.reply_text(
        f"<b>User:</b> {u.mention}\n"
        f"<b>ID:</b> <code>{u.id}</code>\n"
        f"<b>Username:</b> @{u.username if u.username else '—'}"
    )
