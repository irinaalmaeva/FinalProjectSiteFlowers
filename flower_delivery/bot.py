from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Состояния для заказа цветов
class OrderState(StatesGroup):
    waiting_for_address = State()
    waiting_for_confirmation = State()

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

# Функция получения каталога с сайта
async def get_flowers_catalog():
    url = 'http://127.0.0.1:8000/api/flowers/'  # URL API для получения каталога
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Обработка кнопки "Каталог цветов"
@dp.message(F.text == "Каталог цветов")
async def show_catalog(message: types.Message):
    flowers_catalog = await get_flowers_catalog()

    if flowers_catalog:
        catalog_message = "Наш каталог цветов:\n\n"
        for flower in flowers_catalog:
            catalog_message += (
                f"Название: {flower['name']}\n"
                f"Цена: {flower['price']} руб.\n"
                f"Описание: {flower['description']}\n\n"
            )
        await message.answer(catalog_message)
    else:
        await message.answer("Не удалось загрузить каталог цветов.")

# Функция отправки POST-запроса на сайт
async def send_order_to_site(user_id, flowers_ids, address):
    url = 'http://127.0.0.1:8000/orders/api/create_order/'  # URL для API
    data = {
        'user_id': user_id,
        'flowers_ids': flowers_ids,
        'address': address
    }
    logger.info(f"Отправка данных на сайт: {data}")  # Логируем данные

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()

# Обработка кнопки "Заказать"

@dp.message(F.text == "Заказать")
async def start_order(message: types.Message):
    await message.answer("Выберите цветок из каталога, чтобы оформить заказ.")
    await show_flowers_catalog(message)

# Функция отображения каталога цветов с кнопками для выбора

async def show_flowers_catalog(message: types.Message):
    flowers_catalog = await get_flowers_catalog()

    if flowers_catalog:
        catalog_message = "Наш каталог цветов:\n\n"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])  # Создаем пустую клавиатуру

        for flower in flowers_catalog:
            catalog_message += (
                f"Название: {flower['name']}\n"
                f"Цена: {flower['price']} руб.\n"
                f"Описание: {flower['description']}\n\n"
            )
            # Создаем кнопку для выбора цветка
            button = InlineKeyboardButton(text=flower['name'], callback_data=f"flower_{flower['id']}")
            keyboard.inline_keyboard.append([button])  # Добавляем кнопку в клавиатуру

        # Отправляем сообщение с каталогом и кнопками
        await message.answer(catalog_message, reply_markup=keyboard)
    else:
        await message.answer("Не удалось загрузить каталог цветов.")


# Обработка выбора цветка
@dp.callback_query(F.data.startswith("flower_"))
async def handle_flower_selection(callback_query: types.CallbackQuery, state: FSMContext):
    selected_flower_id = callback_query.data.split("_")[1]  # Извлекаем ID цветка
    flowers_catalog = await get_flowers_catalog()
    selected_flower = next((flower for flower in flowers_catalog if str(flower["id"]) == selected_flower_id), None)

    if selected_flower:
        await state.update_data(flowers_ids=[selected_flower["id"]])  # Используем ID цветка

        # Запрашиваем адрес у пользователя
        await callback_query.message.answer("Пожалуйста, введите ваш адрес доставки:")
        await state.set_state(OrderState.waiting_for_address)

    await callback_query.answer()

# Обработка ввода адреса
@dp.message(OrderState.waiting_for_address)
async def process_address(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)

    # Достаём данные о цветах и адресе из FSM
    user_data = await state.get_data()
    flowers_ids = user_data.get("flowers_ids", [])
    address = user_data.get("address")

    # Подтверждаем заказ и запрашиваем подтверждение
    confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="confirm_order")],
        [InlineKeyboardButton(text="Отменить", callback_data="cancel_order")]
    ])

    await message.answer(
        f"Вы выбрали цветок с ID {flowers_ids}. Адрес доставки: {address}. Подтвердите заказ:",
        reply_markup=confirmation_keyboard
    )
    await state.set_state(OrderState.waiting_for_confirmation)

# Обработка подтверждения заказа
@dp.callback_query(F.data == "confirm_order")
async def confirm_order(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id  # Идентификатор пользователя Telegram
    user_data = await state.get_data()  # Получение данных о заказе (цветы и адрес)

    flowers_ids = user_data.get("flowers_ids", [])
    address = user_data.get("address")

    # Отправляем заказ на сайт
    response_data = await send_order_to_site(user_id, flowers_ids, address)

    # Логика после отправки запроса
    if response_data.get('status') == 'success':
        await callback_query.message.answer(f"Ваш заказ успешно оформлен и отправлен на сайт!")
    else:
        await callback_query.message.answer(f"Произошла ошибка при оформлении заказа. Попробуйте позже.")

    await state.clear()  # Очищаем состояние
    await callback_query.answer()

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
