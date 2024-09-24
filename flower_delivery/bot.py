from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp

from config import TELEGRAM_BOT_TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Создание клавиатуры
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Регистрация"), KeyboardButton(text="Каталог цветов")],
        [KeyboardButton(text="Заказать")]
    ],
    resize_keyboard=True
)

# Состояния для Finite State Machine (FSM) регистрации
class RegistrationState(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "Добро пожаловать в наш цветочный магазин! Выберите действие:",
        reply_markup=main_keyboard
    )

# Обработка кнопки "Регистрация"
@dp.message(F.text == "Регистрация")
async def start_registration(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(RegistrationState.waiting_for_name)

# Ввод имени
@dp.message(RegistrationState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш номер телефона:")
    await state.set_state(RegistrationState.waiting_for_phone)

# Ввод номера телефона и завершение регистрации
@dp.message(RegistrationState.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data['name']
    phone = message.text

    # Здесь можно добавить код для сохранения пользователя в базе данных

    await message.answer(f"Регистрация завершена! Ваше имя: {name}, телефон: {phone}")
    await state.clear()


# Добавим фиксированные данные о цветах
flowers_catalog = [
    {"name": "Букет с калами>", "price": 5000, "description": "Очень красивый букет."},
    {"name": "Букет с лилиями", "price": 6000, "description": "Очень нежный букет."},
    {"name": "Букет с орхидеями", "price": 7000, "description": "Букет заставит вас влюбиться в него."},
    {"name": "Букет из роз", "price": 6500, "description": "Розово-сиреневый букет."},
    {"name": "Букет с тюльпанами", "price": 4500, "description": "Весенний радостный букет."},
    {"name": "Букет с герберами", "price": 6500, "description": "Герберы как всегда обворожительны."},
]


# Обработка кнопки "Каталог цветов"
@dp.message(F.text == "Каталог цветов")
async def show_catalog(message: types.Message):
    catalog_message = "Наш каталог цветов:\n\n"

    for flower in flowers_catalog:
        catalog_message += f"Название: {flower['name']}\nЦена: {flower['price']} руб.\nОписание: {flower['description']}\n\n"

    await message.answer(catalog_message)


# Обработка кнопки "Заказать"
@dp.message(F.text == "Заказать")
async def start_order(message: types.Message):
    # Создаем инлайн-клавиатуру с цветами
    flowers_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=flower['name'], callback_data=f"flower_{flower['name']}")] for flower in
        flowers_catalog
    ])

    await message.answer("Выберите цветок, который хотите заказать:", reply_markup=flowers_keyboard)


# Обработка выбора цветка
@dp.callback_query(F.data.startswith("flower_"))
async def handle_flower_selection(callback_query: types.CallbackQuery):
    selected_flower_name = callback_query.data.split("_")[1]
    selected_flower = next((flower for flower in flowers_catalog if flower["name"] == selected_flower_name), None)

    if selected_flower:

        # Создание клавиатуры с подтверждением заказа
        confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить", callback_data="confirm_order")],
            [InlineKeyboardButton(text="Отменить", callback_data="cancel_order")]
        ])

        await callback_query.message.answer(
            f"Вы выбрали: {selected_flower['name']}\nЦена: {selected_flower['price']} руб.\nОписание: {selected_flower['description']}\nПодтвердите заказ:",
            reply_markup=confirmation_keyboard
        )
    await callback_query.answer()


# Обработка подтверждения заказа
@dp.callback_query(F.data.startswith("confirm_"))
async def confirm_order(callback_query: types.CallbackQuery):
    selected_flower_name = callback_query.data.split("_")[1]

    # Логика для сохранения заказа пользователя в базе данных может быть добавлена здесь

    await callback_query.message.answer(f"Ваш заказ на {selected_flower_name} успешно оформлен!")
    await callback_query.answer()


# Обработка отмены заказа
@dp.callback_query(F.data == "cancel")
async def cancel_order(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Ваш заказ был отменен.")
    await callback_query.answer()


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))