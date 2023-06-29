from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import time

from Keyboards import Buttons
from handlers.HandlerOpenAI import ChatGPTstates
import MessageBox
from config import BOT_OWNERS
from dispatcher import bot, db


# Define the start command handler
async def start_handler(message: types.Message):
    await message.answer(MessageBox.START_MESSAGE, reply_markup=Buttons.kbMenu, parse_mode='html')
    user_id = message.from_user.id
    user_name = message.from_user.username
    if not db.user_exists(user_id):
        start_token = 10000
        db.add_client(user_id, time.asctime(), user_name, start_token)
    await bot.send_message(BOT_OWNERS[0], f'New user have connected: {user_name}\n'
                                          f'His ID: {user_id}')
    await ChatGPTstates.dialog_chatgpt.set()

# Define the cancel command handler
async def rest_handler(message: types.Message, state: FSMContext):
    await message.answer("Chat has been refreshed")
    await state.finish()
    await ChatGPTstates.dialog_chatgpt.set()


def user_action_registration(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'], state='*')
    dp.register_message_handler(rest_handler, Text(equals='Reset chat'), state='*')
