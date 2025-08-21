import json, os
from pyrogram import Client, filters
from pyrogram.types import Message

DB_PATH = "chat_db.json"

def _load():
    if not os.path.exists(DB_PATH):
        return {"chats": []}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f)

def add_chat(chat_id: int):
    data = _load()
    if chat_id not in data["chats"]:
        data["chats"].append(chat_id)
        _save(data)

@Client.on_message(filters.all, group=999)
async def track(c: Client, m: Message):
    add_chat(m.chat.id)
