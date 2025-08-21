import json, asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from ..config import CFG

DB_PATH = "chat_db.json"

def _load():
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"chats": []}

def _is_sudo(uid: int) -> bool:
    return uid in set(CFG.sudo_user_ids)

@Client.on_message(filters.command("broadcast"))
async def broadcast(c: Client, m: Message):
    if not m.from_user or not _is_sudo(m.from_user.id):
        return await m.reply_text("Only owner/sudo can use /broadcast.")

    # Message to send
    if len(m.command) > 1:
        payload = m.text.split(" ", 1)[1]
        send_mode = "text"
    elif m.reply_to_message:
        payload = m.reply_to_message
        send_mode = "forward"
    else:
        return await m.reply_text("Use: /broadcast <text> or reply to a message.")

    db = _load()
    chats = db.get("chats", [])
    ok = 0
    fail = 0
    for cid in chats:
        try:
            if send_mode == "text":
                await c.send_message(cid, payload, disable_web_page_preview=True)
            else:
                await payload.copy(cid)
            ok += 1
        except Exception:
            fail += 1
        await asyncio.sleep(0.05)

    await m.reply_text(f"Broadcast done. ✅ {ok} sent, ❌ {fail} failed.")
