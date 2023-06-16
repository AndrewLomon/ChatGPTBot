from aiogram.types import ReplyKeyboardMarkup


kbMenu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
kbM1 = "Reset chat"
kbMenu.add(kbM1)

