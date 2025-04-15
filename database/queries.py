# Запросы для пользователей
GET_USER = "SELECT * FROM users WHERE user_id = %s"
UPDATE_USER = """
    UPDATE users 
    SET username = %s, first_name = %s, last_name = %s, phone_number = %s 
    WHERE user_id = %s
"""
INSERT_USER = """
    INSERT INTO users (user_id, username, first_name, last_name) 
    VALUES (%s, %s, %s, %s)
"""
CHECK_ADMIN = "SELECT is_admin FROM users WHERE user_id = %s"

# Запросы для категорий
GET_ALL_CATEGORIES = "SELECT * FROM categories ORDER BY name"
GET_CATEGORY = "SELECT * FROM categories WHERE category_id = %s"
ADD_CATEGORY = "INSERT INTO categories (name, description, image_url) VALUES (%s, %s, %s)"
UPDATE_CATEGORY = "UPDATE categories SET name = %s, description = %s, image_url = %s WHERE category_id = %s"
DELETE_CATEGORY = "DELETE FROM categories WHERE category_id = %s"

# Запросы для товаров
GET_PRODUCTS_BY_CATEGORY = "SELECT * FROM products WHERE category_id = %s ORDER BY name"
GET_PRODUCT = "SELECT * FROM products WHERE product_id = %s"
ADD_PRODUCT = """
    INSERT INTO products (category_id, name, description, price, image_url) 
    VALUES (%s, %s, %s, %s, %s)
"""
UPDATE_PRODUCT = """
    UPDATE products 
    SET category_id = %s, name = %s, description = %s, price = %s, image_url = %s 
    WHERE product_id = %s
"""
DELETE_PRODUCT = "DELETE FROM products WHERE product_id = %s"

# Запросы для корзины
ADD_TO_CART = "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (%s, %s, %s)"
UPDATE_CART_ITEM = "UPDATE cart_items SET quantity = %s WHERE cart_item_id = %s"
DELETE_CART_ITEM = "DELETE FROM cart_items WHERE cart_item_id = %s"
CLEAR_CART = "DELETE FROM cart_items WHERE user_id = %s"
GET_CART_ITEMS = """
    SELECT ci.*, p.name, p.price, p.image_url, (p.price * ci.quantity) as total_price
    FROM cart_items ci
    JOIN products p ON ci.product_id = p.product_id
    WHERE ci.user_id = %s
"""

# Запросы для заказов
CREATE_ORDER = """
    INSERT INTO orders (user_id, total_amount, delivery_method) 
    VALUES (%s, %s, %s)
"""
ADD_ORDER_ITEM = """
    INSERT INTO order_items (order_id, product_id, quantity, price) 
    VALUES (%s, %s, %s, %s)
"""
GET_USER_ORDERS = """
    SELECT o.*, COUNT(oi.order_item_id) as items_count
    FROM orders o
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.user_id = %s
    GROUP BY o.order_id
    ORDER BY o.created_at DESC
"""
GET_ORDER_DETAILS = """
    SELECT oi.*, p.name, p.image_url
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    WHERE oi.order_id = %s
"""
UPDATE_ORDER_STATUS = "UPDATE orders SET status = %s WHERE order_id = %s"

# Запросы для отзывов о товарах
ADD_PRODUCT_REVIEW = """
    INSERT INTO product_reviews (product_id, user_id, text, rating, photo_url, video_url) 
    VALUES (%s, %s, %s, %s, %s, %s)
"""
GET_PRODUCT_REVIEWS = """
    SELECT pr.*, u.username, u.first_name, u.last_name
    FROM product_reviews pr
    JOIN users u ON pr.user_id = u.user_id
    WHERE pr.product_id = %s
    ORDER BY pr.created_at DESC
"""

# Запросы для отзывов о магазине
ADD_SHOP_REVIEW = "INSERT INTO shop_reviews (user_id, text, photo_url, video_url) VALUES (%s, %s, %s, %s)"
GET_SHOP_REVIEWS = """
    SELECT sr.*, u.username, u.first_name, u.last_name
    FROM shop_reviews sr
    JOIN users u ON sr.user_id = u.user_id
    ORDER BY sr.created_at DESC
"""