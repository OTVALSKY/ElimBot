#bot by Otvalsky
#Add bot to group chat, watch for bans administered, 
#take banned user's pfp and return it with "eliminate" caption

#init begin
import asyncio
from pathlib import Path
import os
#aiogram imports
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ChatMemberUpdated, FSInputFile, ReplyKeyboardRemove
from aiogram.utils.i18n import I18nMiddleware
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command
from aiogram.filters import ChatMemberUpdatedFilter,  KICKED, LEFT, MEMBER, \
RESTRICTED, ADMINISTRATOR, CREATOR, IS_NOT_MEMBER, IS_MEMBER
#custom modules import
import config as cfg                #bot token and stuff
import getphid                      #get user profile picture module
from lang.strings import GetMsg     #locale strings
from db import db                            #settingsDB

bot=Bot(token=cfg.TOKEN)
dp = Dispatcher()
script_folder = os.path.dirname(os.path.abspath(__file__))
builder = ReplyKeyboardBuilder() #keyboard builder 
kbrm = ReplyKeyboardRemove(remove_keyboard=True)

async def init_db():
    if os.path.isfile(script_folder+"/db/botdb.sqlite"):
            print("db exists..")
            return
    else:
        await db.new_db()
        print("db created..")

#init end


########### main logic begin
@dp.message(Command(commands=["go", "begin", "run", "wake up", "start"])) #start whatever
async def start(message: Message):
    msg = await GetMsg(message.from_user.language_code, "hi") #return localized message
    await message.answer(msg)


@dp.message(Command(commands=["?", "whatdoido","halp", "help",]))#hewp uwu | there will be no help
async def help(message: Message):
    msg = await GetMsg(message.from_user.language_code, "help")
    await message.answer(msg)


@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated):
    chat_info = await bot.get_chat(event.chat.id)
    msg = await GetMsg(event.from_user.language_code, "chlang") #show "shoose language" message on language of user adding the bot
    #msg = await GetMsg(Message.forward_from_chat.language_code, "chlang")
    if chat_info.permissions.can_send_messages:
        lcl = db.getall_lc() #get language list from db | lcl for langcuge code list
        # Create the keyboard
        for l in lcl:  #loop to construct a keyboard with available languages
            builder.button(text=l)
        builder.adjust(3) #make it 3 buttons on one row 
        # Send the message with the keyboard
        await event.answer(f"[{event.from_user.full_name}](tg://user?id={event.from_user.id}), "+msg, parse_mode="markdownV2", reply_markup=builder.as_markup(resize_keybpoard=True, one_time_keyboard=True, selective=True))


@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def bot_added_as_member(event: ChatMemberUpdated):
    msg = await GetMsg(event.from_user.language_code, "notadmin") #show "shoose language" message on language of user adding the bot
    await event.answer(msg)


@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> KICKED)) #monitor kicked users, send funny pic
async def member_kicked(event: ChatMemberUpdated):
    cid = event.chat.id
    ret = await getphid.find_max_pfp_size_by_uid(event.old_chat_member.user.id, event.old_chat_member.user.full_name, cid) 
    FSOut = FSInputFile(ret)
    await bot.send_photo(chat_id=cid, photo=FSOut)


@dp.message(F.text.lower().in_({'en', 'ru', 'ua'}))
async def echo(message: Message):
    umsg=message.text #user choice on keyboard  
    msg = await GetMsg(str.lower(umsg), "save") #bot's reply, get locale str right for languguage user just selected. neat.  
    if umsg in (db.getall_lc()):
        await message.answer(msg, reply_markup=kbrm)
        await db.save_chat(message.chat.id, umsg) #write\update chat's language prefernce to db
    else:
        print("err: language does not exist in db, defaulting to english..")
        print ()
        await message.answer(msg, reply_markup=kbrm)
        await db.save_chat(message.chat.id,'en') #write defaulted chat's language prefernce to db
########### main logic end 

# @dp.message()
# async def echo(event: ChatMemberUpdated):
#     print(event)

#starter################################################
async def main():
    await bot.delete_webhook(drop_pending_updates=True) 
    await init_db()
    print ("starting polling...")
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
#starter#################################################