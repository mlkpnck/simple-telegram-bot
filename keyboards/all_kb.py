from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from create_bot import admins, bot
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def paid_kb():
    kb_list = [
        [InlineKeyboardButton(text="Paid", callback_data="paid")],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard
def self_username_tg(username: str):

    kb_list = [
        [KeyboardButton(text=username)],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Type nickname [A-z 0-9 _]"
    )
    return keyboard
def main_kb():
    kb_list = [
        [KeyboardButton(text="/reg")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Use menu:"
    )
    return keyboard