from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_keyboard():
    """Основная клавиатура администратора"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Управление категориями
    keyboard.add(
        InlineKeyboardButton(
            text="➕ Добавить категорию",
            callback_data="admin_add_category"
        ),
        InlineKeyboardButton(
            text="📋 Список категорий",
            callback_data="admin_list_categories"
        )
    )
    
    # Управление товарами
    keyboard.add(
        InlineKeyboardButton(
            text="➕ Добавить товар",
            callback_data="admin_add_product"
        ),
        InlineKeyboardButton(
            text="📋 Список товаров",
            callback_data="admin_list_products"
        )
    )
    
    # Управление заказами
    keyboard.add(
        InlineKeyboardButton(
            text="📦 Заказы",
            callback_data="admin_orders"
        )
    )
    
    # Управление отзывами
    keyboard.add(
        InlineKeyboardButton(
            text="⭐️ Отзывы о товарах",
            callback_data="admin_product_reviews"
        ),
        InlineKeyboardButton(
            text="⭐️ Отзывы о магазине",
            callback_data="admin_shop_reviews"
        )
    )
    
    # Рассылка
    keyboard.add(
        InlineKeyboardButton(
            text="📣 Создать рассылку",
            callback_data="admin_broadcast"
        )
    )
    
    # Кнопка возврата в пользовательский режим
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Выйти из админ-панели",
            callback_data="exit_admin"
        )
    )
    
    return keyboard

def get_categories_management_keyboard(categories):
    """Клавиатура для управления категориями"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    for category in categories:
        keyboard.add(
            InlineKeyboardButton(
                text=category['name'],
                callback_data=f"admin_category_{category['category_id']}"
            )
        )
    
    # Кнопка добавления новой категории
    keyboard.add(
        InlineKeyboardButton(
            text="➕ Добавить категорию",
            callback_data="admin_add_category"
        )
    )
    
    # Кнопка возврата в админ-панель
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Назад в админ-панель",
            callback_data="admin_back_to_panel"
        )
    )
    
    return keyboard

def get_category_actions_keyboard(category_id):
    """Клавиатура действий с категорией"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    keyboard.add(
        InlineKeyboardButton(
            text="✏️ Редактировать",
            callback_data=f"admin_edit_category_{category_id}"
        ),
        InlineKeyboardButton(
            text="❌ Удалить",
            callback_data=f"admin_delete_category_{category_id}"
        )
    )
    
    # Кнопка возврата к списку категорий
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 К списку категорий",
            callback_data="admin_list_categories"
        )
    )
    
    return keyboard

def get_products_management_keyboard(products):
    """Клавиатура для управления товарами"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    for product in products:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{product['name']} - {product['price']} ₽",
                callback_data=f"admin_product_{product['product_id']}"
            )
        )
    
    # Кнопка добавления нового товара
    keyboard.add(
        InlineKeyboardButton(
            text="➕ Добавить товар",
            callback_data="admin_add_product"
        )
    )
    
    # Кнопка возврата в админ-панель
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Назад в админ-панель",
            callback_data="admin_back_to_panel"
        )
    )
    
    return keyboard

def get_product_actions_keyboard(product_id):
    """Клавиатура действий с товаром"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    keyboard.add(
        InlineKeyboardButton(
            text="✏️ Редактировать",
            callback_data=f"admin_edit_product_{product_id}"
        ),
        InlineKeyboardButton(
            text="❌ Удалить",
            callback_data=f"admin_delete_product_{product_id}"
        )
    )
    
    # Кнопка возврата к списку товаров
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 К списку товаров",
            callback_data="admin_list_products"
        )
    )
    
    return keyboard

def get_orders_keyboard(orders):
    """Клавиатура для списка заказов"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    for order in orders:
        status_emoji = {
            'pending': '⏳',
            'processing': '⚙️',
            'shipped': '🚚',
            'delivered': '✅',
            'cancelled': '❌'
        }.get(order['status'], '⏳')
        
        keyboard.add(
            InlineKeyboardButton(
                text=f"{status_emoji} Заказ #{order['order_id']} - {order['total_amount']} ₽",
                callback_data=f"admin_order_{order['order_id']}"
            )
        )
    
    # Кнопка возврата в админ-панель
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Назад в админ-панель",
            callback_data="admin_back_to_panel"
        )
    )
    
    return keyboard

def get_order_actions_keyboard(order_id):
    """Клавиатура действий с заказом"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Кнопки изменения статуса заказа
    keyboard.add(
        InlineKeyboardButton(
            text="⚙️ В обработке",
            callback_data=f"admin_set_order_status_{order_id}_processing"
        ),
        InlineKeyboardButton(
            text="🚚 Отправлен",
            callback_data=f"admin_set_order_status_{order_id}_shipped"
        )
    )
    
    keyboard.add(
        InlineKeyboardButton(
            text="✅ Доставлен",
            callback_data=f"admin_set_order_status_{order_id}_delivered"
        ),
        InlineKeyboardButton(
            text="❌ Отменён",
            callback_data=f"admin_set_order_status_{order_id}_cancelled"
        )
    )
    
    # Кнопка возврата к списку заказов
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 К списку заказов",
            callback_data="admin_orders"
        )
    )
    
    return keyboard

def get_reviews_management_keyboard(reviews, review_type):
    """Клавиатура для управления отзывами"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    for review in reviews:
        # Определяем префикс для callback_data в зависимости от типа отзыва
        prefix = "admin_product_review" if review_type == "product" else "admin_shop_review"
        
        keyboard.add(
            InlineKeyboardButton(
                text=f"Отзыв от {review.get('username') or review.get('first_name', 'пользователя')}",
                callback_data=f"{prefix}_{review['review_id']}"
            )
        )
    
    # Кнопка возврата в админ-панель
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Назад в админ-панель",
            callback_data="admin_back_to_panel"
        )
    )
    
    return keyboard

def get_review_actions_keyboard(review_id, review_type):
    """Клавиатура действий с отзывом"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Определяем префикс для callback_data в зависимости от типа отзыва
    prefix = "admin_product_review" if review_type == "product" else "admin_shop_review"
    back_callback = "admin_product_reviews" if review_type == "product" else "admin_shop_reviews"
    
    keyboard.add(
        InlineKeyboardButton(
            text="❌ Удалить отзыв",
            callback_data=f"{prefix}_delete_{review_id}"
        )
    )
    
    # Кнопка возврата к списку отзывов
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 К списку отзывов",
            callback_data=back_callback
        )
    )
    
    return keyboard

def get_broadcast_confirmation_keyboard():
    """Клавиатура для подтверждения рассылки"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    keyboard.add(
        InlineKeyboardButton(
            text="✅ Отправить",
            callback_data="admin_broadcast_confirm"
        ),
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data="admin_broadcast_cancel"
        )
    )
    
    return keyboard

def get_back_to_admin_keyboard():
    """Клавиатура с кнопкой возврата в админ-панель"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Назад в админ-панель",
            callback_data="admin_back_to_panel"
        )
    )
    return keyboard