from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from aiogram.types import Message
from aiogram import Router  # Не забудь импортировать Router

import aiohttp
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from config import TELEGRAM_BOT_TOKEN


# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

router = Router()  # Создаем роутер


# Обработчик для получения уведомлений от сайта
@router.message(F.text)  # Фильтр для текстовых сообщений
async def handle_order_notification(message: Message):
    # Ответ пользователю о том, что уведомление получено
    await message.reply("Получено уведомление о новом заказе:\n" + message.text)

# Регистрируем роутер
dp.include_router(router)

async def main():
    @dp.message(Command("start"))
    async def start_handler(message: Message):
        await message.answer("Бот запущен!")

        try:
            await dp.start_polling(bot)
        except Exception as e:

             print(f"Произошла ошибка: {e}")

# Запуск бота


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
