from aiogram.dispatcher.filters.state import State, StatesGroup

class CategoryStates(StatesGroup):
    """Состояния для операций с категориями"""
    waiting_for_name = State()  # Ожидание ввода названия категории
    waiting_for_description = State()  # Ожидание ввода описания категории
    waiting_for_image = State()  # Ожидание загрузки изображения категории

class ProductStates(StatesGroup):
    """Состояния для операций с товарами"""
    waiting_for_category = State()  # Ожидание выбора категории
    waiting_for_name = State()  # Ожидание ввода названия товара
    waiting_for_description = State()  # Ожидание ввода описания товара
    waiting_for_price = State()  # Ожидание ввода цены
    waiting_for_image = State()  # Ожидание загрузки изображения товара

class OrderManagementStates(StatesGroup):
    """Состояния для управления заказами"""
    waiting_for_order_id = State()  # Ожидание ввода ID заказа
    waiting_for_status = State()  # Ожидание выбора статуса заказа

class BroadcastStates(StatesGroup):
    """Состояния для массовой рассылки"""
    waiting_for_message = State()  # Ожидание ввода сообщения для рассылки
    waiting_for_confirmation = State()  # Ожидание подтверждения отправки