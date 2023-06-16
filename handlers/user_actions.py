from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from Keyboards import Buttons
from handlers.HandlerOpenAI import ChatGPTstates
import MessageBox


# Define the start command handler
async def start_handler(message: types.Message):
    await message.answer(MessageBox.START_MESSAGE, reply_markup=Buttons.kbMenu, parse_mode='html')
    await ChatGPTstates.dialog_chatgpt.set()

# Define the cancel command handler
async def rest_handler(message: types.Message, state: FSMContext):
    await message.answer("Chat has been refreshed")
    await state.finish()
    await ChatGPTstates.dialog_chatgpt.set()


def user_action_registration(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'], state='*')
    dp.register_message_handler(rest_handler, Text(equals='Reset chat'), state='*')
