errMsg = 'Cannot find locale string, this is a bug and you should report it!'

async def GetMsg(lc, msgCode):
        if lc not in ("en","ru","ua"):
                lc='en'
                print("Language not found, defaulting to English...")
        if lc == 'en':
                ret=en.get(msgCode)
                if ret:
                        return ret
                else:
                        return errMsg
        if lc == 'ru':
                ret=ru.get(msgCode)
                if ret:
                        return ret
                else:
                        return errMsg
        if lc == 'ua':
                ret=ua.get(msgCode)
                if ret:
                        return ret
                else:
                        return errMsg

en = {
'hi':       '👋🏻! Please add this bot to any group chat and make it an administrator!',
'addmin':   'Hello! Thank you for adding me to the chat as an administrator. I will keep an eye on banned users and do something funny :)',
'notadmin': 'Thank you for adding me to the chat as a regular participant. The bot requires administrator rights in the chat to work correctly.',
'bb':       'Shutting down a machine is a murder...',
'help':     'Stop it! Get some help.',
'save':     'Settings saved for this chat✔️',
'chlang':   'сhoose language for this chat:'

}
ru = {
'hi':       '👋🏻! Пожалуйста, добавьте этого бота в любой групповой чат и сделайте его администратором!',
'addmin':   'Привет! Спасибо, что добавили меня в чат в качестве администратора. Я буду следить за забаненными пользователями и делать смешно :)',
'notadmin': 'Спасибо, что добавили меня в чат в качестве участника. Для корректной работы боту необходимы права администратора в чате.',
'bb':       'Выключение машины - это убийство...',
'help':     'Остановись. Лучше обратись за помощью.',
'save':     'Настройки для этого чата сохранены✔️',
'chlang':   'выберите язык для этого чата:'
}
ua = {
'hi':       '👋🏻! Будь ласка, додайте цього бота в будь-який груповий чат і зробіть його адміном!',
'addmin':   'Вітання! Дякую, що додали мене до чату в якості адміністратора. Я стежитиму за забаненими користувачами і робити смішно :)',
'notadmin': 'Спасибі, що додали мене в чат в якості учасника. Для коректної роботи боту необхідні права адміністратора в чаті.',
'bb':       'Вимкнення машини - це вбивство...',
'help':     'Астанавiтесь. Зверніться по допомогу.',
'save':     'Налаштування для цього чату збережено✔️',
'chlang':   'виберiть мову для цього чату:'
}