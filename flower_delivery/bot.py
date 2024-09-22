from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
import asyncio

# Укажите свой токен
from config import TELEGRAM_BOT_TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN )
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Добро пожаловать в наш цветочный магазин! Напишите мне какой букет вы хотите.")


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
