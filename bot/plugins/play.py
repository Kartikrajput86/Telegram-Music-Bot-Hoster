from pyrogram import Client, filters
from pyrogram.types import Message
from ..metadata import yt_search_or_info, best_thumbnail

@Client.on_message(filters.command(["play", "vplay", "ᴘʟᴀʏ", "ᴠ-ᴘʟᴀʏ"]))
async def play_cmd(c: Client, m: Message):
    if len(m.command) < 2 and not (m.reply_to_message and (m.reply_to_message.text or m.reply_to_message.caption)):
        return await m.reply_text("Usage: /play query or reply to a link")

    is_video = m.command[0].lower().startswith("v")
    query = " ".join(m.command[1:]) if len(m.command) > 1 else (m.reply_to_message.text or m.reply_to_message.caption)

    # ensure assistant present
    try:
        await c.get_chat_member(m.chat.id, (await c.get_attribute("assistant").get_me()).id)
    except Exception:
        return await m.reply_text("Use /summon first so I can invite assistant.")

    item = await c.get_attribute("player").enqueue(m.chat.id, m.from_user.id, query, is_video=is_video)

    info = item.info
    title = info.get("title", "Unknown")
    uploader = info.get("uploader") or info.get("channel") or "—"
    duration = info.get("duration") or info.get("duration_string") or "—"
    thumb = best_thumbnail(info)

    caption = (
        f"<b>{'Video' if is_video else 'Song'} queued</b>\n"
        f"<b>Title:</b> {title}\n"
        f"<b>Uploader:</b> {uploader}\n"
        f"<b>Duration:</b> {duration}\n"
        f"<b>Asked by:</b> {m.from_user.mention}"
    )

    if thumb:
        await c.send_photo(m.chat.id, photo=thumb, caption=caption)
    else:
        await m.reply_text(caption)

@Client.on_message(filters.command("skip"))
async def skip_cmd(c: Client, m: Message):
    await c.get_attribute("player").skip(m.chat.id)
    await m.reply_text("⏭️ Skipped")

@Client.on_message(filters.command("stop"))
async def stop_cmd(c: Client, m: Message):
    await c.get_attribute("player").stop(m.chat.id)
    await m.reply_text("⏹️ Stopped")

@Client.on_message(filters.command("pause"))
async def pause_cmd(c: Client, m: Message):
    await c.get_attribute("player").pause(m.chat.id)
    await m.reply_text("⏸️ Paused")

@Client.on_message(filters.command("resume"))
async def resume_cmd(c: Client, m: Message):
    await c.get_attribute("player").resume(m.chat.id)
    await m.reply_text("▶️ Resumed")

@Client.on_message(filters.command("loop"))
async def loop_cmd(c: Client, m: Message):
    state = c.get_attribute("player").toggle_loop(m.chat.id)
    await m.reply_text("🔁 Loop: <b>ON</b>" if state else "🔁 Loop: <b>OFF</b>")

@Client.on_message(filters.command("shuffle"))
async def shuffle_cmd(c: Client, m: Message):
    await c.get_attribute("player").shuffle(m.chat.id)
    await m.reply_text("🔀 Shuffled queue")

@Client.on_message(filters.command("seek"))
async def seek_cmd(c: Client, m: Message):
    await m.reply_text("Seek not implemented in this basic build (will be added in advanced mode).")

@Client.on_message(filters.command("speed"))
async def speed_cmd(c: Client, m: Message):
    await m.reply_text("Speed change not implemented in this basic build (will be added in advanced mode).")
