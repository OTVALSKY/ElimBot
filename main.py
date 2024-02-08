#bot by Otvalsky
#Add bot to group chat, watch for bans administered, 
#take banned user's pfp and return it with "eliminate" caption
#--init
import asyncio
import os
#aiogram imports
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ChatMemberUpdated, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, KICKED, LEFT, MEMBER, \
    RESTRICTED, ADMINISTRATOR, CREATOR, IS_NOT_MEMBER, IS_MEMBER 
#custom modules import
import config as cfg
import getphid
from db import db 

bot=Bot(token=cfg.TOKEN)
dp = Dispatcher()
script_folder = os.path.dirname(os.path.abspath(__file__))

#--init

async def database():
    await db.new_db()
    print("db initalized..")


########### main logic begin
@dp.message(Command(commands=["start", "go", "begin", "run", "wake up" ])) #hewwo uwu
async def start(message: Message):
    print(message)
    await message.answer(f"Hi! Please, add this bot into any group chat and make it an admin!")

@dp.message(Command(commands=["?", "whatdoido","halp", "help",]))#hewp uwu
async def help(message: Message):
    print(message)
    await message.answer(f"Stop it. Get some help.")

@dp.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated):
    #Bot added as admin, so send message
    await event.answer(
        text=f"Привет! Спасибо, что добавили меня в чат "
             f"как администратора."
             f"Я буду следить за забаненными пользователями и делать смешно."
    )

@dp.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def bot_added_as_member(event: ChatMemberUpdated):
    chat_info = await bot.get_chat(event.chat.id)
    if chat_info.permissions.can_send_messages:
        await event.answer(
            text=f"Спасибо, что добавили меня в "
                 f'"{event.chat.title}"'
                 f"как обычного участника. Бот требудет права администратора в чате для корректной работы. "
        )

@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> KICKED )) #monitor kicked users
async def member_kicked(event: ChatMemberUpdated):
    uid = event.old_chat_member.user.id
    cid = event.chat.id
    if uid is None:
        return 100000 #cant find userID
    else:
        ret = await getphid.find_max_pfp_size_by_uid(event.old_chat_member.user.id, event.old_chat_member.user.full_name) 
        if ret == 3333: #user is looser, has 0 pfps 
            await bot.send_message(chat_id=cid, text='User does not have any profile pictures. Le sad 🤡🤮🤡.')
        else:
            FSOut = FSInputFile(ret)
            await bot.send_photo(chat_id=cid, photo=FSOut)
########### main logic end 

#starter
async def main():
    await bot.delete_webhook(drop_pending_updates=True) 
    await database()
    await dp.start_polling(bot)
    
if __name__=="__main__":
    asyncio.run(main())
#starter