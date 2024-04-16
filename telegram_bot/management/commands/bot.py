from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot import custom_filters, callback_data
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    InlineKeyboardButton


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token=settings.TELEGRAM_BOT_TOKEN,
                      state_storage=state_storage)


class BotStates(StatesGroup):
    # state1 = State()
    pass


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать!")


class Command(BaseCommand):
    help = 'Command for launching Telegram bot.'

    def handle(self, *args, **kwargs) -> None:
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.add_custom_filter(custom_filters.StateFilter(bot))
        bot.infinity_polling()
