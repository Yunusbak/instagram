import logging
import os
import requests
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
load_dotenv()


API_TOKEN=os.getenv('TELEGRAM_API_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("""Hi!\nI'm Instagram bot by @yunusbakk!\n
        /users
    """)


@dp.message_handler(commands=['users'])
async def send_songs(message: types.Message):
    users = requests.get(f"http://127.0.0.1:8000/api/tg/users").json()['users']


    users_text = "\n\n".join([f"Пользователи твоего инстаграма :\n "
                              f""
                              f""
                              f"👤 *Пользователь*: {user['username']}\n"
                              f"📧 *Email*: {user['email']}\n"
                              f"📝 *Имя*: {user['first_name']}\n"
                              f"📝 *Фамилия*: {user['last_name']}\n"
                              f"⏰ *Дата создания*: {user['created_at']}"
                              for user in users])

    await message.reply(users_text, parse_mode='Markdown')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)