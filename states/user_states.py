from aiogram.dispatcher.filters.state import State, StatesGroup

class OrderStates(StatesGroup):
    """Состояния для оформления заказа"""
    waiting_for_phone = State()  # Ожидание ввода номера телефона
    waiting_for_delivery_method = State()  # Ожидание выбора способа доставки

class ProductReviewStates(StatesGroup):
    """Состояния для добавления отзыва о товаре"""
    waiting_for_text = State()  # Ожидание ввода текста отзыва
    waiting_for_media = State()  # Ожидание загрузки фото/видео (опционально)

class ShopReviewStates(StatesGroup):
    """Состояния для добавления отзыва о магазине"""
    waiting_for_text = State()  # Ожидание ввода текста отзыва
    waiting_for_media = State()  # Ожидание загрузки фото/видео (опционально)