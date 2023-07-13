import openai
from config import TOKEN_OPENAI
from dispatcher import db
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from Keyboards import Buttons

# Set up the OpenAI API client, model and token calculate variable
openai.api_key = TOKEN_OPENAI
MODEL = "gpt-3.5-turbo"


# Make class for conversation history
class ChatGPTstates(StatesGroup):
    dialog_chatgpt = State()


async def chatgpt35turbo_handler(message: types.Message, state: FSMContext):
    try:
        # Checking is there enough tokens
        tokens = db.get_client_tokens(message.from_user.id)
        if tokens[0] <= 0:
            await message.answer('Unfortunately, you are run out of available tokens.\n '
                                 'They update every week')
            return
        # Retrieve the current conversation state and context
        async with state.proxy() as data:
            conversation_history = data.get("conversation_history", [])

        # Add the user's message to the conversation history
        conversation_history.append({'role': 'user', 'content': message.text})

        # Send a request to the ChatGPT model API
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=conversation_history,
            max_tokens=1500,
            n=1,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
        )
        # Get the response text from the API response
        chatgpt_response = response['choices'][0]['message']['content']

        # Calculate spent tokens
        db.count_client_tokens(response['usage']['total_tokens'], message.from_user.id)

        # Add the model's response to the conversation history
        conversation_history.append(response['choices'][0]['message'])

        # Store the updated conversation history in the state
        async with state.proxy() as data:
            data["conversation_history"] = conversation_history

        # Send the response back to the user via the aiogram library
        await message.answer(chatgpt_response, reply_markup=Buttons.kbMenu, parse_mode='html')
    except:
        await message.answer('Currently service is not available due to overload. '
                             'Try later by pressing "<b>Reset chat</b>" button', parse_mode='html')


def openai_registration(dp: Dispatcher):
    dp.register_message_handler(chatgpt35turbo_handler, state=ChatGPTstates.dialog_chatgpt)
