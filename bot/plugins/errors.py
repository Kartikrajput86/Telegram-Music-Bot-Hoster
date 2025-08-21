from pyrogram import Client
@Client.on_raw_update()
async def _errors(_, __):
    pass
