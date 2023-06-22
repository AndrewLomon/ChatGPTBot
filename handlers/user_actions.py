from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from Keyboards import Buttons
from handlers.HandlerOpenAI import ChatGPTstates
import MessageBox
from config import BOT_OWNERS
from dispatcher import bot


# Define the start command handler
async def start_handler(message: types.Message):
    await message.answer(MessageBox.START_MESSAGE, reply_markup=Buttons.kbMenu, parse_mode='html')
    user_id = message.from_user.id
    user_name = message.from_user.full_name
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
