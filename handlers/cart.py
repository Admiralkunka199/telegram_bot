# handlers/cart.py
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from keyboards.user_kb import get_cart_keyboard, get_checkout_keyboard, get_main_keyboard
from states.user_states import OrderStates
from database.db_manager import DatabaseManager
from utils.helpers import format_price

db = DatabaseManager()

async def show_cart(message: types.Message, state: FSMContext = None):
    """Показать корзину пользователя"""
    if state:
        await state.finish()
    
    user_id = message.from_user.id
    
    # Получаем товары из корзины
    cart_items = db.get_cart_items(user_id)
    
    if not cart_items:
        await message.answer(
            "Ваша корзина пуста. Воспользуйтесь меню для выбора товаров.",
            reply_markup=get_main_keyboard()
        )
        return
    
    # Подсчитываем общую сумму
    total_price = sum(item['total_price'] for item in cart_items)
    
    # Формируем сообщение с товарами в корзине
    cart_text = "🛒 <b>Ваша корзина</b>\n\n"
    
    for item in cart_items:
        cart_text += f"• {item['name']} - {item['quantity']} шт. x {format_price(item['price'])} = {format_price(item['total_price'])} руб.\n"
    
    cart_text += f"\n<b>Итого: {format_price(total_price)} руб.</b>"
    
    await message.answer(
        cart_text,
        reply_markup=get_cart_keyboard(cart_items),
        parse_mode="HTML"
    )

async def process_remove_from_cart(callback_query: types.CallbackQuery):
    """Удалить товар из корзины"""
    cart_item_id = int(callback_query.data.split('_')[-1])
    
    # Удаляем товар из корзины
    db.remove_from_cart(cart_item_id)
    
    # Обновляем отображение корзины
    user_id = callback_query.from_user.id
    cart_items = db.get_cart_items(user_id)
    
    if not cart_items:
        await callback_query.message.edit_text(
            "Ваша корзина пуста. Воспользуйтесь меню для выбора товаров."
        )
        await callback_query.answer("Товар удален из корзины")
        return
    
    # Подсчитываем общую сумму
    total_price = sum(item['total_price'] for item in cart_items)
    
    # Формируем обновленное сообщение
    cart_text = "🛒 <b>Ваша корзина</b>\n\n"
    
    for item in cart_items:
        cart_text += f"• {item['name']} - {item['quantity']} шт. x {format_price(item['price'])} = {format_price(item['total_price'])} руб.\n"
    
    cart_text += f"\n<b>Итого: {format_price(total_price)} руб.</b>"
    
    await callback_query.message.edit_text(
        cart_text,
        reply_markup=get_cart_keyboard(cart_items),
        parse_mode="HTML"
    )
    
    await callback_query.answer("Товар удален из корзины")

async def process_clear_cart(callback_query: types.CallbackQuery):
    """Очистить корзину"""
    user_id = callback_query.from_user.id
    
    # Очищаем корзину
    db.clear_cart(user_id)
    
    await callback_query.message.edit_text(
        "Ваша корзина очищена.",
        reply_markup=get_main_keyboard()
    )
    await callback_query.answer("Корзина очищена")

async def start_checkout(callback_query: types.CallbackQuery, state: FSMContext):
    """Начать оформление заказа"""
    user_id = callback_query.from_user.id
    
    # Получаем товары из корзины
    cart_items = db.get_cart_items(user_id)
    
    if not cart_items:
        await callback_query.answer("Корзина пуста, невозможно оформить заказ")
        return
    
    # Запрашиваем номер телефона для связи
    await OrderStates.waiting_for_phone.set()
    
    # Сохраняем ID сообщения с корзиной для последующего редактирования
    await state.update_data(cart_message_id=callback_query.message.message_id)
    
    await callback_query.message.answer(
        "Для оформления заказа введите ваш номер телефона в формате +79XXXXXXXXX\n"
        "Для отмены отправьте /cancel"
    )
    await callback_query.answer()

async def process_phone_input(message: types.Message, state: FSMContext):
    """Обработка ввода номера телефона"""
    phone = message.text.strip()
    
    # Простая проверка формата номера телефона
    if not (phone.startswith('+7') and len(phone) == 12 and phone[1:].isdigit()):
        await message.answer(
            "Пожалуйста, введите номер телефона в формате +79XXXXXXXXX"
        )
        return
    
    # Сохраняем номер телефона
    await state.update_data(phone=phone)
    
    # Переходим к выбору способа доставки
    await OrderStates.waiting_for_delivery_method.set()
    
    await message.answer(
        "Выберите способ получения заказа:",
        reply_markup=get_checkout_keyboard()
    )

async def process_delivery_method(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработка выбора способа доставки"""
    method = callback_query.data.split('_')[-1]  # "delivery" или "pickup"
    
    # Получаем данные из состояния
    data = await state.get_data()
    phone = data.get('phone')
    
    user_id = callback_query.from_user.id
    
    # Получаем товары из корзины
    cart_items = db.get_cart_items(user_id)
    
    if not cart_items:
        await callback_query.answer("Корзина пуста, невозможно оформить заказ")
        await state.finish()
        return
    
    # Подсчитываем общую сумму
    total_price = sum(item['total_price'] for item in cart_items)
    
    # Создаем заказ в БД
    # Здесь нужно дополнить метод в db_manager.py для создания заказа
    # db.create_order(user_id, total_price, method, phone, cart_items)
    
    # Очищаем корзину
    db.clear_cart(user_id)
    
    # Завершаем процесс оформления заказа
    await state.finish()
    
    await callback_query.message.edit_text(
        f"Ваш заказ успешно оформлен!\n\n"
        f"Способ получения: {'Доставка' if method == 'delivery' else 'Самовывоз'}\n"
        f"Телефон для связи: {phone}\n"
        f"Сумма заказа: {format_price(total_price)} руб.\n\n"
        f"Мы свяжемся с вами в ближайшее время для подтверждения заказа."
    )
    await callback_query.answer("Заказ оформлен")

async def cancel_checkout(callback_query: types.CallbackQuery, state: FSMContext):
    """Отмена оформления заказа"""
    await state.finish()
    
    await callback_query.message.edit_text(
        "Оформление заказа отменено.",
        reply_markup=get_main_keyboard()
    )
    await callback_query.answer("Оформление заказа отменено")