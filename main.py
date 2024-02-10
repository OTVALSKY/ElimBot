#bot by Otvalsky
#Add bot to group chat, watch for bans administered, 
#take banned user's pfp and return it with "eliminate" caption
#--init
import asyncio
from pathlib import Path
import os
#aiogram imports
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ChatMemberUpdated, FSInputFile
from aiogram.utils.i18n import I18nMiddleware
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, KICKED, LEFT, MEMBER, \
    RESTRICTED, ADMINISTRATOR, CREATOR, IS_NOT_MEMBER, IS_MEMBER
#custom modules import
import config as cfg
import getphid
from lang.strings import GetMsg 
from db import db 

bot=Bot(token=cfg.TOKEN)
dp = Dispatcher()
script_folder = os.path.dirname(os.path.abspath(__file__))
#--init

async def database():
    await db.new_db()
    print("db initalized..")

########### main logic begin
@dp.message(Command(commands=["go", "begin", "run", "wake up", "start"])) #hewwo uwu
async def start(message: Message):
    msg = await GetMsg(message.from_user.language_code, "hi")
    await message.answer(msg)

@dp.message(Command(commands=["?", "whatdoido","halp", "help",]))#hewp uwu
async def help(message: Message):
    msg = await GetMsg(message.from_user.language_code, "help")
    await message.answer(msg)

@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated):
    await event.answer("a)")

@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def bot_added_as_member(event: ChatMemberUpdated):
    chat_info = await bot.get_chat(event.chat.id)
    if chat_info.permissions.can_send_messages:
        await event.answer("a)")

@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> KICKED )) #monitor kicked users
async def member_kicked(event: ChatMemberUpdated):
    uid = event.old_chat_member.user.id
    cid = event.chat.id
    if uid is None:
        return 100000 #cant find userID
    else:
        ret = await getphid.find_max_pfp_size_by_uid(event.old_chat_member.user.id, event.old_chat_member.user.full_name) 
        FSOut = FSInputFile(ret)
        await bot.send_photo(chat_id=cid, photo=FSOut)
########### main logic end 

#starter
async def main():
    await bot.delete_webhook(drop_pending_updates=True) 
    await database()
    print ("bot initialized, started polling")
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
#starter