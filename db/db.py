import sqlite3 as sql
from pathlib import Path
#init variables
#db
here = Path(__file__).parent
dbPath=here/"botdb.sqlite"
#locale
imgres = Path.glob(here.parent/"getimg"/"img", "overlay-??.png")
#overlay images gotta be strictly in format overlay-**.png, otherwise it won't work 
#you can control number bot of locales by adding\deleting overlay pictures, 
#^although if no additional locale strings added, then english text will be returned by default

d = {} #declare dictionary with lang names and paths to overlay pics 
for path in imgres: #iterate over path in img directory to append into list 
    d[str(path.name)[8:10]]=str(path)

#logic
async def new_db():
    #create tables, ChatSettings is to store chats where bot were added and store 
    #overlay localisation ID(lang_id), which then can be joined on LangDef, where 
    #detailed Language name and path to overlay is located. 
    con = sql.connect(dbPath) #db handle
    cur = con.cursor() #cur handle
    cur.execute("CREATE TABLE IF NOT EXISTS ChatSettings(id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER, lang_id INTEGER)") #table for chat settings
    cur.execute("CREATE TABLE IF NOT EXISTS LangDef(id INTEGER PRIMARY KEY AUTOINCREMENT, LangName TEXT, ovPath TEXT)")  #table for languages and paths to overlays
    
    for keys, values in d.items(): #insert data into lang table about languages and path to overlay image
        cur.execute("INSERT INTO LangDef(LangName, ovPath) VALUES(?,?)", (keys,values))
    cur.close()
    con.commit()  #write to db 🔥