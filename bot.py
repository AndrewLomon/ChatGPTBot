from aiogram import executor
from dispatcher import dp
from handlers import user_actions, HandlerOpenAI
import asyncio


# Main body
user_actions.user_action_registration(dp)
HandlerOpenAI.openAI_registration(dp)


if __name__ == "__main__":
    asyncio.get_event_loop().create_task(user_actions.scheduler())
    executor.start_polling(dp, skip_updates=True)

