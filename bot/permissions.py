from pyrogram.types import Chat
from pyrogram.enums import ChatMemberStatus

async def bot_can_invite(bot, chat: Chat) -> bool:
    me = await bot.get_chat_member(chat.id, (await bot.get_me()).id)
    if me.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR):
        perms = getattr(me, "privileges", None)
        return bool(perms and perms.can_invite_users)
    return False

async def is_admin(bot, chat_id: int, user_id: int) -> bool:
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR)
