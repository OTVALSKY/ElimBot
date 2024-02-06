import sqlite3 as sql
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
dbPath = script_directory+'/tgBot.sqlite'

con = sql.connect(dbPath)
cur = con.cursor()

async def db_start():
    #create tables, ChatSettings is to store chats where bot were added and store 
    #overlay localisation ID(lang_id), which then can be joined on LangDef, where 
    #detailed Language name and path to overlay is located. 
    await cur.execute(
                    "CREATE TABLE IF NOT EXISTS ChatSettings("
                    "id INTEGER PRIMARI KEY AUTOINCREMENT, "
                    "chat_id INTEGER, "
                    "lang_id INTEGER) "
                    "CREATE TABLE IF NOT EXISTS LangDef("
                    "id INTEGER PRIMARI KEY AUTOINCREMENT, "
                    "Lang TEXT, "
                    "LangImagePath TEXT)"
                    )
    con.commit()
    return 

 
    


