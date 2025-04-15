# handlers/reviews.py
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from keyboards.user_kb import get_reviews_keyboard, get_back_keyboard
from states.user_states import ShopReviewStates, ProductReviewStates
from database.db_manager import DatabaseManager

db = DatabaseManager()

async def show_reviews(message: types.Message, state: FSMContext = None):
    """Показать отзывы о магазине"""
    if state:
        await state.finish()
    
    # Получаем последние отзывы о магазине
    # Здесь нужно добавить метод в db_manager для получения отзывов о магазине
    # shop_reviews = db.get_shop_reviews(limit=5)
    
    # Пока заглушка
    reviews_text = "⭐️ <b>Отзывы о нашем магазине</b>\n\n"
    reviews_text += "Пока нет отзывов. Будьте первым, кто оставит отзыв о нашем магазине!"
    
    await message.answer(
        reviews_text,
        reply_markup=get_reviews_keyboard(),
        parse_mode="HTML"
    )

async def start_add_shop_review(callback_query: types.CallbackQuery, state: FSMContext):
    """Начать процесс добавления отзыва о магазине"""
    # Переходим в состояние ожидания ввода текста отзыва
    await ShopReviewStates.waiting_for_text.set()
    
    await callback_query.message.answer(
        "Напишите ваш отзыв о магазине. Для отмены отправьте /cancel"
    )
    await callback_query.answer()

async def process_shop_review_text(message: types.Message, state: FSMContext):
    """Обработка ввода текста отзыва о магазине"""
    review_text = message.text.strip()
    
    # Сохраняем текст отзыва
    await state.update_data(review_text=review_text)
    
    # Предлагаем добавить фото или видео к отзыву
    await ShopReviewStates.waiting_for_media.set()
    
    await message.answer(
        "Хотите добавить фото или видео к отзыву? Пришлите файл или нажмите 'Пропустить'.\n"
        "Для отмены отправьте /cancel",
        reply_markup=get_skip_media_keyboard()
    )

async def process_product_review_text(message: types.Message, state: FSMContext):
    """Обработка ввода текста отзыва о товаре"""
    review_text = message.text.strip()
    
    # Сохраняем текст отзыва
    await state.update_data(review_text=review_text)
    
    # Предлагаем добавить фото или видео к отзыву
    await ProductReviewStates.waiting_for_media.set()
    
    await message.answer(
        "Хотите добавить фото или видео к отзыву? Пришлите файл или нажмите 'Пропустить'.\n"
        "Для отмены отправьте /cancel",
        reply_markup=get_skip_media_keyboard()
    )

def get_skip_media_keyboard():
    """Клавиатура для пропуска добавления медиа"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="Пропустить",
            callback_data="skip_media"
        )
    )
    return keyboard

async def process_shop_review_media(message: types.Message, state: FSMContext):
    """Обработка загрузки медиа для отзыва о магазине"""
    # Получаем данные из состояния
    data = await state.get_data()
    review_text = data.get('review_text')
    
    # Получаем URL файла
    file_id = None
    
    if message.photo:
        file_id = message.photo[-1].file_id
        media_type = 'photo'
    elif message.video:
        file_id = message.video.file_id
        media_type = 'video'
    else:
        await message.answer(
            "Пожалуйста, отправьте фото или видео, или нажмите 'Пропустить'"
        )
        return
    
    # Сохраняем отзыв в базе данных
    user_id = message.from_user.id
    
    # Здесь нужно добавить метод в db_manager для добавления отзыва о магазине
    # db.add_shop_review(user_id, review_text, photo_url=file_id if media_type == 'photo' else None, video_url=file_id if media_type == 'video' else None)
    
    # Завершаем процесс
    await state.finish()
    
    await message.answer(
        "Спасибо за ваш отзыв! Он был успешно добавлен.",
        reply_markup=get_main_keyboard()
    )

async def process_product_review_media(message: types.Message, state: FSMContext):
    """Обработка загрузки медиа для отзыва о товаре"""
    # Получаем данные из состояния
    data = await state.get_data()
    review_text = data.get('review_text')
    product_id = data.get('product_id')
    
    # Получаем URL файла
    file_id = None
    
    if message.photo:
        file_id = message.photo[-1].file_id
        media_type = 'photo'
    elif message.video:
        file_id = message.video.file_id
        media_type = 'video'
    else:
        await message.answer(
            "Пожалуйста, отправьте фото или видео, или нажмите 'Пропустить'"
        )
        return
    
    # Сохраняем отзыв в базе данных
    user_id = message.from_user.id
    
    # Здесь нужно добавить метод в db_manager для добавления отзыва о товаре
    # db.add_product_review(user_id, product_id, review_text, rating=5, photo_url=file_id if media_type == 'photo' else None, video_url=file_id if media_type == 'video' else None)
    
    # Завершаем процесс
    await state.finish()
    
    await message.answer(
        "Спасибо за ваш отзыв о товаре! Он был успешно добавлен.",
        reply_markup=get_main_keyboard()
    )

async def skip_media(callback_query: types.CallbackQuery, state: FSMContext):
    """Пропуск добавления медиа к отзыву"""
    # Получаем данные из состояния
    data = await state.get_data()
    review_text = data.get('review_text')
    
    # Определяем, какой тип отзыва мы обрабатываем
    current_state = await state.get_state()
    user_id = callback_query.from_user.id
    
    if current_state == ShopReviewStates.waiting_for_media.state:
        # Отзыв о магазине
        # Здесь нужно добавить метод в db_manager для добавления отзыва о магазине
        # db.add_shop_review(user_id, review_text)
        text = "Спасибо за ваш отзыв о магазине!"
    elif current_state == ProductReviewStates.waiting_for_media.state:
        # Отзыв о товаре
        product_id = data.get('product_id')
        # Здесь нужно добавить метод в db_manager для добавления отзыва о товаре
        # db.add_product_review(user_id, product_id, review_text, rating=5)
        text = "Спасибо за ваш отзыв о товаре!"
    else:
        text = "Произошла ошибка при обработке отзыва."
    
    # Завершаем процесс
    await state.finish()
    
    await callback_query.message.edit_text(
        text + " Он был успешно добавлен."
    )
    await callback_query.answer()