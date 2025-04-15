from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import SHOP_NAME, SHOP_DESCRIPTION, SHOP_LOGO_URL, SHOP_CONTACTS
from database.db_manager import DatabaseManager

db = DatabaseManager()

# Создание основной клавиатуры
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Меню"))
    keyboard.add(KeyboardButton("Корзина"), KeyboardButton("Отзывы"))
    keyboard.add(KeyboardButton("Контакты"))
    return keyboard

async def cmd_start(message: types.Message, state: FSMContext = None):
    """Обработчик команды /start"""
    # Сбрасываем состояние, если оно есть
    if state:
        await state.finish()
    
    # Добавляем пользователя в базу данных или обновляем его данные
    user = message.from_user
    db.add_user(
        user_id=user.id, 
        username=user.username, 
        first_name=user.first_name, 
        last_name=user.last_name
    )
    
    # Отправляем приветственное сообщение
    welcome_text = f"Добро пожаловать в {SHOP_NAME}!\n\n{SHOP_DESCRIPTION}"
    
    # Если есть логотип, отправляем его вместе с текстом
    if SHOP_LOGO_URL:
        await message.answer_photo(
            photo=SHOP_LOGO_URL,
            caption=welcome_text,
            reply_markup=get_main_keyboard()
        )
    else:
        await message.answer(
            text=welcome_text,
            reply_markup=get_main_keyboard()
        )

async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = (
        f"Как пользоваться ботом {SHOP_NAME}:\n\n"
        "🛒 Меню - просмотр категорий и товаров\n"
        "🛍 Корзина - ваши выбранные товары\n"
        "⭐️ Отзывы - отзывы о магазине\n"
        "📞 Контакты - контактная информация магазина\n\n"
        "Для выбора товара нажмите на его название в меню, "
        "затем нажмите 'В корзину'. После этого вы можете оформить заказ через раздел 'Корзина'.\n\n"
        "Если у вас возникли вопросы, обратитесь в раздел 'Контакты'."
    )
    await message.answer(help_text, reply_markup=get_main_keyboard())

async def show_contacts(message: types.Message):
    """Обработчик для отображения контактов магазина"""
    contacts_text = f"📞 Контактная информация:\n\n{SHOP_CONTACTS}"
    await message.answer(contacts_text, reply_markup=get_main_keyboard())