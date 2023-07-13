import copy

from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kbMenu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
kbM1 = "Reset chat"
kbM2 = "My balance"
kbMenu.add(kbM1,kbM2)

ikbBalance = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
ikbB1 = InlineKeyboardButton(text="Support development", url='https://boosty.to/lomos_andrew')
ikbBalance.add(ikbB1)
