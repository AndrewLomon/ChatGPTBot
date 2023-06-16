import openai
from config import TOKEN_OPENAI
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


# Set up the OpenAI API client, model and token calculate variable
openai.api_key = TOKEN_OPENAI
MODEL = "gpt-3.5-turbo"
users_tokens = []

# Make class for conversation history
class ChatGPTstates(StatesGroup):
    dialog_chatgpt = State()

async def chatgpt35turbo_handler(message: types.Message, state: FSMContext):
    try:
        # Retrieve the current conversation state and context
        async with state.proxy() as data:
            conversation_history = data.get("conversation_history", [])

        # Adding new user to the list. TODO now he just adding new discts [{326374284: 0}, {326374284: 0}]

        # Add the user's message to the conversation history
        conversation_history.append({'role': 'user', 'content': message.text})

        # Send a request to the ChatGPT model API
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=conversation_history,
            max_tokens=1024,
            n=1,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
        )
        # Get the response text from the API response
        chatgpt_response = response['choices'][0]['message']['content']

        # Add the model's response to the conversation history
        conversation_history.append(response['choices'][0]['message'])

        # Store the updated conversation history in the state
        async with state.proxy() as data:
            data["conversation_history"] = conversation_history

        # Count tokens TODO make a tokens counter
        # for user in users_tokens:
        #     if user == userid:

        # Send the response back to the user via the aiogram library
        await message.answer(chatgpt_response)
    except:
       await message.answer('Currently service is not available due to overload. '
                            'Try later by pressing "<b>Reset chat</b>" button', parse_mode='html')


def openAI_registration(dp: Dispatcher):
    dp.register_message_handler(chatgpt35turbo_handler, state=ChatGPTstates.dialog_chatgpt)