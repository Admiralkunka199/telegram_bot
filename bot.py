import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import BOT_TOKEN, ADMIN_IDS, SHOP_NAME, SHOP_DESCRIPTION
from database.db_manager import DatabaseManager

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DatabaseManager()

# Импорт обработчиков после инициализации диспетчера (чтобы избежать циклических импортов)
from handlers import common, catalog, cart, orders, reviews, admin

# Регистрация обработчиков
def register_handlers():
    # Регистрация общих обработчиков
    dp.register_message_handler(common.cmd_start, commands=['start'])
    dp.register_message_handler(common.cmd_help, commands=['help'])
    
    # Регистрация обработчиков каталога
    dp.register_message_handler(catalog.show_categories, lambda message: message.text == "Меню")
    dp.register_callback_query_handler(catalog.show_products, lambda c: c.data.startswith('category_'))
    dp.register_callback_query_handler(catalog.show_product_details, lambda c: c.data.startswith('product_'))
    
    # Регистрация обработчиков корзины
    dp.register_message_handler(cart.show_cart, lambda message: message.text == "Корзина")
    dp.register_callback_query_handler(cart.add_to_cart, lambda c: c.data.startswith('add_to_cart_'))
    dp.register_callback_query_handler(cart.remove_from_cart, lambda c: c.data.startswith('remove_from_cart_'))
    dp.register_callback_query_handler(cart.clear_cart, lambda c: c.data == 'clear_cart')
    
    # Регистрация обработчиков заказов
    dp.register_callback_query_handler(orders.start_checkout, lambda c: c.data == 'checkout')
    
    # Регистрация обработчиков отзывов
    dp.register_message_handler(reviews.show_shop_reviews, lambda message: message.text == "Отзывы")
    dp.register_callback_query_handler(reviews.start_add_shop_review, lambda c: c.data == 'add_shop_review')
    dp.register_callback_query_handler(reviews.start_add_product_review, lambda c: c.data.startswith('add_product_review_'))
    
    # Регистрация обработчиков для контактов
    dp.register_message_handler(common.show_contacts, lambda message: message.text == "Контакты")
    
    # Регистрация обработчиков для администратора
    dp.register_message_handler(admin.admin_panel, commands=['admin'])

# Инициализация обработчиков
register_handlers()

async def on_startup(dp):
    """Действия при запуске бота"""
    # Установка команд бота
    await bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Получить помощь"),
        types.BotCommand("admin", "Панель администратора (только для админов)")
    ])
    
    logging.info(f"Бот {SHOP_NAME} запущен!")

async def on_shutdown(dp):
    """Действия при остановке бота"""
    # Закрытие подключения к базе данных
    db.close()
    
    # Закрытие хранилища состояний
    await dp.storage.close()
    await dp.storage.wait_closed()
    
    logging.info(f"Бот {SHOP_NAME} остановлен!")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)