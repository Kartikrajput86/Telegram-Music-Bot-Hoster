import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from ..buttons import start_kb, help_kb
from ..strings import START_BANNER, START_ANIM_FRAMES

@Client.on_message(filters.command("start"))
async def start_cmd(c: Client, m: Message):
    msg = await m.reply_text("ʟᴏᴧᴅɪηɢ.")
    for f in START_ANIM_FRAMES:
        await asyncio.sleep(0.25)
        await msg.edit_text(f)
    me = await c.get_me()
    await msg.edit_text(
        START_BANNER.format(mention=m.from_user.mention, bot=me.mention),
        reply_markup=start_kb(me.username),
        disable_web_page_preview=True,
    )

@Client.on_callback_query(filters.regex("^help$"))
async def on_help(c: Client, q: CallbackQuery):
    text = (
        "<b>Commands</b>\n\n"
        "• ᴘɪηɢ — ping\n"
        "• ɪᴅ — show ids\n"
        "• ɪɴғᴏ — user/chat info\n"
        "• ᴍᴇɴᴛɪᴏɴᴀʟʟ &lt;msg&gt; — mention everyone\n\n"
        "• ᴘʟᴀʏ &lt;query/url&gt; — audio\n"
        "• ᴠ-ᴘʟᴀʏ &lt;query/url&gt; — video\n"
        "• sᴋɪᴘ / sᴛᴏᴘ / ᴘᴀᴜsᴇ / ʀᴇsᴜᴍᴇ\n"
        "• ʟᴏᴏᴘ — toggle\n"
        "• sʜᴜғғʟᴇ — queue\n"
        "• sᴇᴇᴋ &lt;sec&gt; — (basic)\n"
        "• sᴘᴇᴇᴅ &lt;1.25&gt; — (basic)\n\n"
        "• /broadcast — Owner/Sudo"
    )
    await q.message.edit_text(text, reply_markup=help_kb())

@Client.on_callback_query(filters.regex("^back$"))
async def on_back(c: Client, q: CallbackQuery):
    me = await c.get_me()
    await q.message.edit_text(
        START_BANNER.format(mention=q.from_user.mention, bot=me.mention),
        reply_markup=start_kb(me.username),
        disable_web_page_preview=True,
    )
