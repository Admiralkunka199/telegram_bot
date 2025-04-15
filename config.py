import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# ID администратора (список ID администраторов)
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))

# Параметры базы данных
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'telegram_shop')

# Максимальный размер файла для загрузки (в байтах)
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

# Параметры магазина
SHOP_NAME = os.getenv('SHOP_NAME', 'Telegram Shop')
SHOP_DESCRIPTION = os.getenv('SHOP_DESCRIPTION', 'Добро пожаловать в наш магазин!')
SHOP_LOGO_URL = os.getenv('SHOP_LOGO_URL', '')  # URL логотипа магазина
SHOP_CONTACTS = os.getenv('SHOP_CONTACTS', 'Наши контакты: телефон, email, адрес')