# - *- coding: utf- 8 - *-
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

bot = telegram.Bot(token='530068163:AAFwRyGOSY_W6-VmpsZ8ot4d5ZmciKk515E')

print(bot.getMe())
updates = bot.getUpdates()
print([u.message.text for u in updates])
chat_id = bot.getUpdates()[-1].message.chat_id
print(chat_id)

bot.sendMessage(chat_id=chat_id, text="*bold* _italic_ [link](http://google.com).", parse_mode=telegram.ParseMode.MARKDOWN)
