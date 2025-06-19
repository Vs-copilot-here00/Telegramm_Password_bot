from telebot import types


#  обычные переменные для работы (Поменяйте названия если это необходимо)
FILE_PATH = r"C:\Telegramm_bot\data_passwords.json"


#  токен вашего бота (от @BotFather)
TOKEN = "7858899150:AAG9f0-jaMA-kzQuM5kpJZhOT6SQPbP_2UY"

# example: "0123456789:xXxxXx-XxXx-xxxXXX012xxxXXxX45Xx"


#  тексты ошибок и приветствия (константы)
NO, YES = '❌', '✅'

R, F = "🗑️", "🔍"

TEXT_ERROR = "The fields for name and password are mandatory, please try again."


FIRST_GREETING = """Hi there! 😊  
I'm your personal assistant, here to help with convenient storage
and password recording. 🔐  
/start - Restarting the bot 🔄
/help - Displays all available commands"""

GREETING = """Hi there! 😊  
I'm your personal assistant, here to help with convenient storage
and password recording. 🔐  
/start - Restarting the bot 🔄

Here's the list of commands:    
   Add ➕   ⟹  Add a password to your collection ➕  
   Passwords 📂   ⟹  Your saved passwords 📂  
   Find 🔍   ⟹  Find a saved password 🔍
   Remove 🗑️  ⟹  delete site by name 🗑️
   All clear ⚠️  ⟹  Deletes the entire list of dictionaries 🗂️
"""

COMMAND_ADD = ("""🔐add/ Site/ Password or random (your number)/ description🔐

*Be sure to list them using ⚠️"/"⚠️, the number of spaces does not matter.""")


NAME_COMMANDS = [
   "Passwords 📂",
   "Add ➕",
   "Find 🔍",
   "Remove 🗑️",
   "All clear ⚠️"
]

COMMAND_LIST = [
   types.BotCommand("start", "Start the bot"),
   types.BotCommand("help", "Display available commands"),
]
