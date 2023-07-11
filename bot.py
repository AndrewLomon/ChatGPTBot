from aiogram import executor
from dispatcher import dp
from handlers import user_actions, HandlerOpenAI


user_actions.user_action_registration(dp)
HandlerOpenAI.openAI_registration(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
