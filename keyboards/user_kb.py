from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    """Основная клавиатура пользователя"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Меню"))
    keyboard.add(KeyboardButton("Корзина"), KeyboardButton("Отзывы"))
    keyboard.add(KeyboardButton("Контакты"))
    return keyboard

def get_categories_keyboard(categories):
    """Клавиатура с категориями товаров"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    for category in categories:
        keyboard.add(
            InlineKeyboardButton(
                text=category['name'],
                callback_data=f"category_{category['category_id']}"
            )
        )
    
    # Кнопка возврата в главное меню
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="back_to_main"
        )
    )
    
    return keyboard

def get_products_keyboard(products, category_id):
    """Клавиатура с товарами категории"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    for product in products:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{product['name']} - {product['price']} ₽",
                callback_data=f"product_{product['product_id']}"
            )
        )
    
    # Кнопка возврата к списку категорий
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 К категориям",
            callback_data="back_to_categories"
        )
    )
    
    return keyboard

def get_product_details_keyboard(product_id):
    """Клавиатура с действиями для товара"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Кнопка добавления в корзину
    keyboard.add(
        InlineKeyboardButton(
            text="🛒 В корзину",
            callback_data=f"add_to_cart_{product_id}"
        )
    )
    
    # Кнопка для просмотра отзывов
    keyboard.add(
        InlineKeyboardButton(
            text="⭐️ Отзывы",
            callback_data=f"product_reviews_{product_id}"
        ),
        InlineKeyboardButton(
            text="✍️ Оставить отзыв",
            callback_data=f"add_product_review_{product_id}"
        )
    )
    
    # Кнопка возврата к списку товаров
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 К товарам",
            callback_data=f"back_to_products"
        )
    )
    
    return keyboard

def get_cart_keyboard(cart_items):
    """Клавиатура для корзины"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    if cart_items:
        # Добавляем кнопки для каждого товара в корзине
        for item in cart_items:
            keyboard.add(
                InlineKeyboardButton(
                    text=f"❌ Удалить {item['name']}",
                    callback_data=f"remove_from_cart_{item['cart_item_id']}"
                )
            )
        
        # Кнопки для операций с корзиной
        keyboard.add(
            InlineKeyboardButton(
                text="🗑 Очистить корзину",
                callback_data="clear_cart"
            ),
            InlineKeyboardButton(
                text="💳 Оформить заказ",
                callback_data="checkout"
            )
        )
    
    # Кнопка возврата в меню
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 В меню",
            callback_data="back_to_categories"
        )
    )
    
    return keyboard

def get_checkout_keyboard():
    """Клавиатура для оформления заказа"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Кнопки выбора способа доставки
    keyboard.add(
        InlineKeyboardButton(
            text="🚚 Доставка",
            callback_data="delivery_method_delivery"
        ),
        InlineKeyboardButton(
            text="🏪 Самовывоз",
            callback_data="delivery_method_pickup"
        )
    )
    
    # Кнопка отмены
    keyboard.add(
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data="cancel_checkout"
        )
    )
    
    return keyboard

def get_reviews_keyboard():
    """Клавиатура для раздела отзывов"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    keyboard.add(
        InlineKeyboardButton(
            text="✍️ Оставить отзыв о магазине",
            callback_data="add_shop_review"
        )
    )
    
    # Кнопка возврата в главное меню
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 В главное меню",
            callback_data="back_to_main"
        )
    )
    
    return keyboard

def get_back_keyboard(callback_data="back_to_main"):
    """Клавиатура с кнопкой "Назад" """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=callback_data
        )
    )
    return keyboard