from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_kb(bot_username: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❖ ᴧᴅᴅ ϻє ʙᴧʙʏ ❖", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("❍ ᴡηᴇʀ", url="https://t.me/noturrsem"),
         InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/+DOM4zc_zP4VjMTM1")],
        [InlineKeyboardButton("ʜᴇʟᴘ ᴧɴᴅ ᴄᴏϻϻᴧηᴅs", callback_data="help")],
        [InlineKeyboardButton("ϻᴧᴋᴇ ᴜsᴇʀʙᴏᴛ", url="https://t.me/SanataniUserbot")],
    ])

def help_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⟵ ʙᴧᴄᴋ", callback_data="back")]
    ])
