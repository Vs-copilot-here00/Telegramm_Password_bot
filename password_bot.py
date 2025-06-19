from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import string
import json
import secrets
from const import *


bot = TeleBot(TOKEN)

    #  Побочные функции

#  функция генерации случайного пароля
def random_password(*, chat_id, long: str=12) -> str:
    if (long).isdigit() and int(long) > 4:
        long = int(long)
    else:
        bot.send_message(chat_id, "The value is either absent or unsuitable, so 12 is set by default.")
        long = 12
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ""
    while not all([any(l.isdigit() for l in password),
                    any(l.isalpha() for l in password),
                    any(l in string.punctuation for l in password)]):
        password = ''.join(secrets.choice(chars) for _ in range(long))
    return password


def keyboard_YES_or_NO():
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Добавляем кнопки для каждого языка
    keyboard.add(
        InlineKeyboardButton(NO, callback_data=NO),
        InlineKeyboardButton(YES, callback_data=YES),
    )
    
    return keyboard

   #  Функции бота

#  функция чтения всех паролей из файла
def Passwords(*, message) -> None:
    #  Создаём переменную для вывода всех паролей, а потом записываем в переменную All_passwords
    All_passwords = "You all passwords in the format:\nsite: password \- disk\(❌/✅\)\n🔐  🔐  🔐\n"
    with open(FILE_PATH, "r") as file_read:
        data = json.load(file_read)
        if str(message.chat.id) not in data:
            bot.send_message(message.chat.id, "  You don't have any passwords yet.")
            return
        for name, value in data[str(message.chat.id)].items():
            password, disc = value.values()
            All_passwords += f"`{name}`  \-\>  `{password}`  \-  disc" + (f'{NO}\n' if disc == NO else f'{YES}\n')

    #  Выводим все пароли
    bot.send_message(message.chat.id, All_passwords, parse_mode="MarkdownV2")



#  не рабочая функия добавления пароля в файл
def Add(*, message: TeleBot, needs_text: str) -> None:
    #  Переменные для функции
    int_chat_id = message.chat.id
    str_chat_id = str(int_chat_id)
    Flag = True

    #  Разделяем текст на название, пароль, описание, и проверяем на колличество слов
    text = [str(info).strip().replace('/', '') for info in (message.text + f' / {NO} / "" ').split('/')[1:]]
    text = [elem for elem in text if elem != '']
    if len(text) < 4 or not any([text[0], text[1]]):
        bot.send_message(int_chat_id, TEXT_ERROR)
        return
    name, password, description, *_ = text

    #  Используем функцию random_password для генерации пароля
    password_split = password.split(maxsplit=1)
    if "random" in password_split:
        password = random_password(chat_id=int_chat_id, long=password_split[len(password_split) - 1])

    #  Читаем данные из файла
    with open(FILE_PATH, "r") as file_read:
        data = json.load(file_read)
        data.setdefault(str_chat_id, {})
        
        #  Проверяем, есть ли уже пароль с таким названием
        for last_name, last_password in data[str_chat_id].items():
            if last_name.lower().strip() == name.lower().strip():
                del data[str_chat_id][last_name]
                bot.send_message(int_chat_id,
                                f"The site `{last_name}`\, the password `{last_password['password']}` will be overwritten to \=\> site `{name}` with password `{password}` \!", parse_mode="MarkdownV2")
                Flag = False
                break

    #  Добавляем пароль сначало в данные, а потом в файл
    data[str_chat_id] = data[str_chat_id] | {name: {"password": password, "description": description}}
    with open(FILE_PATH, "w") as file_write:
        json.dump(data, file_write, indent=4)
    
    #  Уведомляем пользователя о добавлении пароля
    if Flag:
        bot.send_message(int_chat_id,
                          f"The site `{name}` with password `{password}` been added to your collection",
                          parse_mode="MarkdownV2")




#  функция поиска пароля по названию сайта (тест)
def Find(*, message, mode: str=f"_[{F}]"):       #  Придумать обработчик для поиска сайтов
    pass

#  функция удаления пароля по названию сайта (тест)
def Remove(*, message):
    pass

#  удаление всех паролей (тест)
def All_clear(*, int_chat_id: int, call_id: int):
    str_chat_id = str(int_chat_id)
    
    #  Читаем данные из файла
    with open(FILE_PATH, "r") as file_read:
        data = json.load(file_read)
        if str_chat_id not in data:
            bot.send_message(int_chat_id, TEXT_ERROR)
            bot.answer_callback_query(call_id, TEXT_ERROR + NO)
            return
        del data[str_chat_id]

    #  Удаляем все пароли и записываем вфайл
    with open(FILE_PATH, "w") as file_write:
        json.dump(data, file_write, indent=4)
    bot.answer_callback_query(call_id, 'All your passwords are deleted' + R)
    



#  обработчики сообщений тг
@bot.message_handler(commands=["start", "help", ])
def send_welcome(message):
    if message.text == '/help':
        bot.send_message(message.chat.id, GREETING)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for command_number in range(0, len(NAME_COMMANDS) - 1, 2):
            item_button = [KeyboardButton(NAME_COMMANDS[command_number]), KeyboardButton(NAME_COMMANDS[command_number + 1])]
            markup.row(*item_button)
        markup.add(NAME_COMMANDS[-1])
        bot.send_message(message.chat.id, FIRST_GREETING, reply_markup=markup)


#  обработчик для кнопок (и функции add) бота
@bot.message_handler(func=lambda message: True)
def process_the_button(message):
    int_chat_id = message.chat.id
    text = message.text
    if text == "Passwords 📂":
        Passwords(message=message)
    elif text == "Add ➕":
        bot.send_message(int_chat_id, COMMAND_ADD)
    elif text.strip().lower().startswith("add"):
        Add(message=message, needs_text=f"{text} / Missing / ''")
    elif text == "Find 🔍":
        bot.delete_my_commands()
        Find(message=message)
    elif text == "Remove 🗑️":
        bot.delete_my_commands()
        Find(message=message, mode=f"_[{R}]")
    elif text == "All clear ⚠️":
        keyboard = keyboard_YES_or_NO()
        bot.send_message(message.chat.id, "Are you sure you want to remove all the passwords?", reply_markup=keyboard)
    else:
        bot.send_message(int_chat_id, NO + " I didn't understand your command, please repeat it again !")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == YES:
            All_clear(int_chat_id=call.message.chat.id, call_id=call.id)
        elif call.data == NO:
            bot.answer_callback_query(call.id, 'Cansel' + NO)
        bot.edit_message_text(FIRST_GREETING, call.message.chat.id, call.message.message_id)
        

bot.set_my_commands(COMMAND_LIST)  #  добавление команд боту

bot.infinity_polling() #  запуск