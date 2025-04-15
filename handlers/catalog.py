# handlers/catalog.py
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from keyboards.user_kb import (
    get_categories_keyboard,
    get_products_keyboard,
    get_product_details_keyboard,
    get_back_keyboard
)
from states.user_states import OrderStates, ProductReviewStates
from database.db_manager import DatabaseManager
from utils.helpers import format_price

db = DatabaseManager()

async def show_catalog(message: types.Message, state: FSMContext = None):
    """Показывает каталог категорий товаров"""
    if state:
        await state.finish()
    
    # Получаем все категории из БД
    categories = db.get_categories()
    
    if not categories:
        await message.answer("В каталоге пока нет категорий.")
        return
    
    await message.answer(
        "Выберите категорию товаров:",
        reply_markup=get_categories_keyboard(categories)
    )

async def process_category_selection(callback_query: types.CallbackQuery):
    """Обработка выбора категории"""
    category_id = int(callback_query.data.split('_')[1])
    
    # Получаем категорию по ID
    category = db.get_category(category_id)
    
    if not category:
        await callback_query.answer("Категория не найдена")
        return
    
    # Получаем товары в этой категории
    products = db.get_products_by_category(category_id)
    
    if not products:
        await callback_query.answer("В этой категории пока нет товаров")
        await callback_query.message.edit_text(
            f"В категории '{category['name']}' пока нет товаров.",
            reply_markup=get_back_keyboard("back_to_categories")
        )
        return
    
    # Показываем товары категории
    await callback_query.message.edit_text(
        f"Товары в категории '{category['name']}':",
        reply_markup=get_products_keyboard(products, category_id)
    )
    await callback_query.answer()

async def process_product_selection(callback_query: types.CallbackQuery):
    """Обработка выбора товара"""
    product_id = int(callback_query.data.split('_')[1])
    
    # Получаем товар по ID
    product = db.get_product(product_id)
    
    if not product:
        await callback_query.answer("Товар не найден")
        return
    
    # Формируем текст с информацией о товаре
    product_text = f"""
📦 <b>{product['name']}</b>

📝 <b>Описание:</b> {product['description']}

💰 <b>Цена:</b> {format_price(product['price'])} руб.
"""
    
    # Отправляем фото товара, если оно есть
    if product['image_url']:
        await callback_query.message.delete()
        await callback_query.message.answer_photo(
            photo=product['image_url'],
            caption=product_text,
            reply_markup=get_product_details_keyboard(product_id),
            parse_mode="HTML"
        )
    else:
        await callback_query.message.edit_text(
            product_text,
            reply_markup=get_product_details_keyboard(product_id),
            parse_mode="HTML"
        )
    
    await callback_query.answer()

async def add_to_cart(callback_query: types.CallbackQuery):
    """Добавление товара в корзину"""
    product_id = int(callback_query.data.split('_')[-1])
    user_id = callback_query.from_user.id
    
    # Получаем товар по ID для проверки существования
    product = db.get_product(product_id)
    
    if not product:
        await callback_query.answer("Товар не найден")
        return
    
    # Добавляем товар в корзину
    db.add_to_cart(user_id, product_id, 1)
    
    await callback_query.answer(f"Товар '{product['name']}' добавлен в корзину!")

async def back_to_categories(callback_query: types.CallbackQuery):
    """Возврат к списку категорий"""
    await callback_query.message.edit_text(
        "Выберите категорию товаров:",
        reply_markup=get_categories_keyboard(db.get_categories())
    )
    await callback_query.answer()

async def back_to_products(callback_query: types.CallbackQuery):
    """Возврат к списку товаров"""
    # Здесь нужно использовать хранилище состояний или другой способ запомнить,
    # из какой категории пришел пользователь
    # Пока реализуем возврат к списку категорий
    await back_to_categories(callback_query)

async def back_to_main(callback_query: types.CallbackQuery, state: FSMContext = None):
    """Возврат в главное меню"""
    if state:
        await state.finish()
    
    # Отправляем пользователя в главное меню
    from handlers.common import get_main_keyboard
    
    await callback_query.message.edit_text(
        "Вы вернулись в главное меню. Выберите опцию:",
        reply_markup=get_main_keyboard()
    )
    await callback_query.answer()

# Функции обработки просмотра отзывов и добавления отзыва к товару
async def show_product_reviews(callback_query: types.CallbackQuery):
    """Показать отзывы о товаре"""
    product_id = int(callback_query.data.split('_')[-1])
    
    # Здесь нужно добавить логику получения отзывов из БД
    # Пока заглушка
    await callback_query.answer("Функция просмотра отзывов будет доступна позже")

async def start_add_product_review(callback_query: types.CallbackQuery, state: FSMContext):
    """Начать процесс добавления отзыва о товаре"""
    product_id = int(callback_query.data.split('_')[-1])
    
    # Сохраняем ID товара
    await state.update_data(product_id=product_id)
    
    # Переходим в состояние ожидания ввода текста отзыва
    await ProductReviewStates.waiting_for_text.set()
    
    await callback_query.message.answer(
        "Напишите ваш отзыв о товаре. Для отмены отправьте /cancel"
    )
    await callback_query.answer()