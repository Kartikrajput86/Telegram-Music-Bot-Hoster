from pyrogram import Client, filters
from pyrogram.types import Message
from ..permissions import bot_can_invite

ASSISTANT_USERNAME = None

@Client.on_message(filters.command(["summon", "join", "assistant"]))
async def summon(c: Client, m: Message):
    global ASSISTANT_USERNAME
    player = c.get_attribute("player")
    assistant = c.get_attribute("assistant")

    if ASSISTANT_USERNAME is None:
        me = await assistant.get_me()
        ASSISTANT_USERNAME = me.username

    # Ensure assistant in chat
    try:
        await c.get_chat_member(m.chat.id, (await assistant.get_me()).id)
        in_chat = True
    except Exception:
        in_chat = False

    if not in_chat:
        if await bot_can_invite(c, m.chat):
            try:
                await c.add_chat_members(m.chat.id, [ASSISTANT_USERNAME])
                await m.reply_text("Assistant invited ✅")
            except Exception as e:
                return await m.reply_text(f"Failed to invite assistant: <code>{e}</code>")
        else:
            return await m.reply_text(
                "Please give me <b>Invite Users</b> permission to invite assistant to play music in voice chat."
            )

    await m.reply_text("Assistant is ready. Use <code>/play</code> or <code>/vplay</code>.")
