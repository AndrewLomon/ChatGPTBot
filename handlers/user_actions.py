from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import time

from Keyboards import Buttons
from handlers.HandlerOpenAI import ChatGPTstates
import MessageBox
from config import BOT_OWNERS
from dispatcher import bot, db

# Variables
start_token = 100000

# Define the start command handler
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    if not db.user_exists(user_id):
        db.add_client(user_id, time.strftime("%Y-%m-%d", time.localtime()), user_name, start_token)
        await message.answer(MessageBox.START_MESSAGE, reply_markup=Buttons.kbMenu, parse_mode='html')
    else:
        await message.answer(MessageBox.GREETING_MESSAGE, reply_markup=Buttons.kbMenu, parse_mode='html')
    await bot.send_message(BOT_OWNERS[0], f'New user have connected: @{user_name}\n')
    await ChatGPTstates.dialog_chatgpt.set()

# Define the cancel command handler
async def reset_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not db.user_exists(user_id):
        await message.answer("Please, start over /start")
        await state.finish()
    else:
        await message.answer("Chat has been refreshed", reply_markup=Buttons.kbMenu, parse_mode='html')
        await state.finish()
        await ChatGPTstates.dialog_chatgpt.set()

async def My_balance(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    if not db.user_exists(user_id):
        await message.answer("Please, start over /start")
        await state.finish()
    else:
        userTokens = db.get_client_tokens(user_id)[0]
        await message.answer(MessageBox.MY_BALANCE_MESSAGE.format(userTokens),reply_markup=Buttons.kbMenu)
        await message.answer("", reply_markup=Buttons.ikbBalance, parse_mode='html')
        await ChatGPTstates.dialog_chatgpt.set()

def user_action_registration(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'], state='*')
    dp.register_message_handler(reset_handler, Text(equals='Reset chat'), state='*')
    dp.register_message_handler(My_balance, Text(equals='My balance'), state='*')
