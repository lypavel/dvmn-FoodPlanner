from django.core.management.base import BaseCommand
from django.conf import settings
from django.http.response import Http404
from django.shortcuts import get_object_or_404
import telebot
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    Message, CallbackQuery


from telegram_bot.models import Client
from telegram_bot.management.commands.bot_utils import bot_buttons as btn
from telegram_bot.management.commands.bot_utils import bot_messages as msg


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token=settings.TELEGRAM_BOT_TOKEN,
                      state_storage=state_storage)


class BotStates(StatesGroup):
    approve_pd = State()
    get_client_name = State()
    get_client_phone_number = State()
    show_recipe = State()
    show_instructions = State()


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    # TODO: Add some images here and user msg.WELCOME as caption.
    bot.send_message(message.chat.id, msg.WELCOME)

    try:
        client = get_object_or_404(Client, telegram_id=message.from_user.id)
    except Http404:
        client = None

    if not client:
        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        button_yes = InlineKeyboardButton(btn.YES, callback_data='yes')
        button_no = InlineKeyboardButton(btn.NO, callback_data='no')
        inline_keyboard.add(button_yes, button_no)

        bot.send_message(
            message.chat.id,
            msg.PD_AGREEMENT,
            reply_markup=inline_keyboard
        )
        bot.set_state(
            message.from_user.id,
            BotStates.approve_pd, message.chat.id
        )
        return

    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(
        InlineKeyboardButton(btn.SHOW_RECIPES, callback_data='new_recipe')
    )

    bot.send_message(
        message.chat.id,
        msg.FOR_REGULAR_CUSTOMERS,
        reply_markup=inline_keyboard
    )

    bot.set_state(
        message.from_user.id,
        BotStates.show_recipe, message.chat.id
    )


@bot.callback_query_handler(state=BotStates.approve_pd,
                            func=lambda call: call.data == 'yes')
def pd_approved(call: CallbackQuery) -> None:
    message = call.message
    chat_id = message.chat.id

    bot.send_document(chat_id, open('agreement.pdf', 'rb'))
    bot.edit_message_reply_markup(chat_id, message.message_id)

    get_client_name(call)


@bot.callback_query_handler(state=BotStates.approve_pd,
                            func=lambda call: call.data == 'no')
def pd_not_approved(call: CallbackQuery) -> None:
    message = call.message
    chat_id = message.chat.id
    bot.edit_message_reply_markup(chat_id, message.message_id)

    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(
        InlineKeyboardButton(btn.PD_YES, callback_data='yes')
    )

    bot.send_message(
        chat_id,
        msg.PD_RESTRICT,
        reply_markup=inline_keyboard
    )


def get_client_name(call: CallbackQuery) -> None:
    message = call.message
    chat_id = message.chat.id

    bot.send_message(chat_id, msg.GET_CLIENT_NAME)
    bot.set_state(chat_id, BotStates.get_client_name)


@bot.message_handler(state=BotStates.get_client_name,
                     func=lambda message: True)
def get_client_phone_number(message: Message):
    name = message.text
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_name'] = name

    bot.send_message(
        message.chat.id,
        '\n'.join([msg.generate_user_greeting(name), msg.GET_CLIENT_PHONE])
    )
    bot.set_state(message.from_user.id, BotStates.get_client_phone_number)


@bot.message_handler(state=BotStates.get_client_phone_number,
                     func=lambda message: True)
def proccess_client_information(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        user_name = data['user_name']
    user_phone = message.text

    Client.objects.create(
        telegram_id=message.from_user.id,
        name=user_name,
        phonenumber=user_phone,
    )

    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(
        InlineKeyboardButton(btn.SHOW_RECIPES, callback_data='new_recipe')
    )

    bot.send_message(
        message.chat.id,
        msg.AUTH_SUCCESSFUL,
        reply_markup=inline_keyboard
    )

    bot.set_state(
        message.from_user.id,
        BotStates.show_recipe, message.chat.id
    )


@bot.callback_query_handler(state=BotStates.approve_pd,
                            func=lambda call: call.data == 'new_recipe')
@bot.callback_query_handler(state=BotStates.show_recipe,
                            func=lambda call: call.data == 'new_recipe')
def show_random_recipe(call: CallbackQuery) -> None:
    message = call.message
    chat_id = message.chat.id
    bot.edit_message_reply_markup(chat_id, message.message_id)

    # TODO: get recipes from db, send image and description.
    # TODO: Add logic for changing recipes on every call of 'show recipe'

    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(
        InlineKeyboardButton(btn.SHOW_INSTRUCTIONS,
                             callback_data='show_instructions'),
        InlineKeyboardButton(btn.ANOTHER_RECIPE, callback_data='new_recipe')
    )

    bot.send_message(
        chat_id,
        'Рецепт',
        reply_markup=inline_keyboard
    )

    bot.set_state(
        message.from_user.id,
        BotStates.show_recipe, chat_id
    )


@bot.callback_query_handler(state=BotStates.show_recipe,
                            func=lambda call: call.data == 'show_instructions')
def show_recipe_instructions(call: CallbackQuery) -> None:
    message = call.message
    chat_id = message.chat.id
    bot.edit_message_reply_markup(chat_id, message.message_id)

    bot.send_message(
        chat_id,
        'Описание рецепта',
    )

    bot.set_state(
        message.from_user.id,
        BotStates.show_instructions, message.chat.id
    )


class Command(BaseCommand):
    help = 'Command for launching Telegram bot.'

    def handle(self, *args, **kwargs) -> None:
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.add_custom_filter(custom_filters.StateFilter(bot))
        bot.infinity_polling()
