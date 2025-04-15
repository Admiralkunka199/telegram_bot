import logging
from typing import Union, List, Dict
from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated
from config import ADMIN_IDS

async def send_admin_notification(bot: Bot, message: str):
    """
    Отправляет уведомление всем администраторам
    
    Args:
        bot: Экземпляр бота
        message: Текст уведомления
    """
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, message)
        except (BotBlocked, ChatNotFound, UserDeactivated) as e:
            logging.error(f"Не удалось отправить уведомление администратору {admin_id}: {e}")

def format_price(price: Union[int, float]) -> str:
    """
    Форматирует цену для отображения
    
    Args:
        price: Цена в виде числа
        
    Returns:
        str: Отформатированная цена с разделителями
    """
    return f"{float(price):,.2f}".replace(",", " ").replace(".00", "") + " ₽"

def format_cart_summary(cart_items: List[Dict]) -> str:
    """
    Форматирует содержимое корзины для отображения
    
    Args:
        cart_items: Список товаров в корзине
        
    Returns:
        str: Отформатированное содержимое корзины
    """
    if not cart_items:
        return "🛒 Ваша корзина пуста"
    
    total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
    items_count = sum(item['quantity'] for item in cart_items)
    
    result = "🛒 Ваша корзина:\n\n"
    
    for item in cart_items:
        result += f"• {item['name']} - {item['quantity']} шт. x {format_price(item['price'])} = {format_price(item['price'] * item['quantity'])}\n"
    
    result += f"\nВсего товаров: {items_count} шт."
    result += f"\nИтого: {format_price(total_amount)}"
    
    return result

def format_order_summary(order: Dict, order_items: List[Dict]) -> str:
    """
    Форматирует информацию о заказе для отображения
    
    Args:
        order: Информация о заказе
        order_items: Товары в заказе
        
    Returns:
        str: Отформатированная информация о заказе
    """
    status_text = {
        'pending': '⏳ Ожидает обработки',
        'processing': '⚙️ В обработке',
        'shipped': '🚚 Отправлен',
        'delivered': '✅ Доставлен',
        'cancelled': '❌ Отменён'
    }.get(order['status'], '⏳ Ожидает обработки')
    
    delivery_method = {
        'delivery': '🚚 Доставка',
        'pickup': '🏪 Самовывоз'
    }.get(order['delivery_method'], '🚚 Доставка')
    
    result = f"📦 Заказ #{order['order_id']}\n"
    result += f"Статус: {status_text}\n"
    result += f"Способ получения: {delivery_method}\n"
    result += f"Дата заказа: {order['created_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
    
    result += "Товары в заказе:\n"
    for item in order_items:
        result += f"• {item['name']} - {item['quantity']} шт. x {format_price(item['price'])} = {format_price(item['price'] * item['quantity'])}\n"
    
    result += f"\nИтого: {format_price(order['total_amount'])}"
    
    return result