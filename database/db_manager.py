import mysql.connector
from mysql.connector import Error
import logging
from typing import Dict, List, Tuple, Any, Optional, Union
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Установка соединения с базой данных"""
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            logging.info("Успешное подключение к базе данных")
        except Error as e:
            logging.error(f"Ошибка подключения к базе данных: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = None) -> int:
        """
        Выполнение запроса к базе данных без возврата результатов
        
        Args:
            query: SQL запрос
            params: Параметры запроса
            
        Returns:
            last_id: ID последней вставленной записи или количество затронутых строк
        """
        cursor = None
        last_id = 0
        
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            self.connection.commit()
            last_id = cursor.lastrowid or cursor.rowcount
            
        except Error as e:
            logging.error(f"Ошибка выполнения запроса: {e}")
            if self.connection:
                self.connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
                
        return last_id
    
    def execute_select(self, query: str, params: tuple = None) -> List[Dict]:
        """
        Выполнение SELECT запроса и возврат результатов
        
        Args:
            query: SQL запрос
            params: Параметры запроса
            
        Returns:
            results: Список словарей с результатами запроса
        """
        cursor = None
        results = []
        
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            results = cursor.fetchall()
            
        except Error as e:
            logging.error(f"Ошибка выполнения SELECT запроса: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
                
        return results
    
    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict]:
        """
        Выполнение SELECT запроса и возврат одной записи
        
        Args:
            query: SQL запрос
            params: Параметры запроса
            
        Returns:
            result: Словарь с результатом запроса или None
        """
        cursor = None
        result = None
        
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            result = cursor.fetchone()
            
        except Error as e:
            logging.error(f"Ошибка выполнения SELECT запроса для одной записи: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
                
        return result
    
    def check_user_exists(self, user_id: int) -> bool:
        """Проверка существования пользователя в базе данных"""
        query = "SELECT user_id FROM users WHERE user_id = %s"
        result = self.fetch_one(query, (user_id,))
        return bool(result)
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None) -> int:
        """Добавление нового пользователя в базу данных"""
        if self.check_user_exists(user_id):
            query = """
                UPDATE users 
                SET username = %s, first_name = %s, last_name = %s 
                WHERE user_id = %s
            """
            self.execute_query(query, (username, first_name, last_name, user_id))
            return user_id
        
        query = """
            INSERT INTO users (user_id, username, first_name, last_name) 
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (user_id, username, first_name, last_name))
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Получение информации о пользователе"""
        query = "SELECT * FROM users WHERE user_id = %s"
        return self.fetch_one(query, (user_id,))
    
    def is_admin(self, user_id: int) -> bool:
        """Проверка, является ли пользователь администратором"""
        query = "SELECT is_admin FROM users WHERE user_id = %s"
        result = self.fetch_one(query, (user_id,))
        return result and result.get('is_admin', False)
    
    def close(self):
        """Закрытие соединения с базой данных"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("Соединение с базой данных закрыто")

    # Методы для работы с категориями
    def get_categories(self) -> List[Dict]:
        """Получение всех категорий"""
        query = "SELECT * FROM categories ORDER BY name"
        return self.execute_select(query)
    
    def get_category(self, category_id: int) -> Optional[Dict]:
        """Получение информации о категории по ID"""
        query = "SELECT * FROM categories WHERE category_id = %s"
        return self.fetch_one(query, (category_id,))
    
    # Методы для работы с товарами
    def get_products_by_category(self, category_id: int) -> List[Dict]:
        """Получение всех товаров в категории"""
        query = "SELECT * FROM products WHERE category_id = %s ORDER BY name"
        return self.execute_select(query, (category_id,))
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        """Получение информации о товаре по ID"""
        query = "SELECT * FROM products WHERE product_id = %s"
        return self.fetch_one(query, (product_id,))
    
    # Методы для работы с корзиной
    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> int:
        """Добавление товара в корзину пользователя"""
        # Проверим, есть ли уже этот товар в корзине
        query = "SELECT * FROM cart_items WHERE user_id = %s AND product_id = %s"
        existing_item = self.fetch_one(query, (user_id, product_id))
        
        if existing_item:
            # Обновляем количество
            query = """
                UPDATE cart_items 
                SET quantity = quantity + %s 
                WHERE user_id = %s AND product_id = %s
            """
            self.execute_query(query, (quantity, user_id, product_id))
            return existing_item['cart_item_id']
        else:
            # Добавляем новый товар в корзину
            query = """
                INSERT INTO cart_items (user_id, product_id, quantity) 
                VALUES (%s, %s, %s)
            """
            return self.execute_query(query, (user_id, product_id, quantity))
    
    def get_cart_items(self, user_id: int) -> List[Dict]:
        """Получение всех товаров в корзине пользователя"""
        query = """
            SELECT ci.*, p.name, p.price, p.image_url, (p.price * ci.quantity) as total_price
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.product_id
            WHERE ci.user_id = %s
        """
        return self.execute_select(query, (user_id,))
    
    def update_cart_item_quantity(self, cart_item_id: int, quantity: int) -> bool:
        """Обновление количества товара в корзине"""
        query = "UPDATE cart_items SET quantity = %s WHERE cart_item_id = %s"
        self.execute_query(query, (quantity, cart_item_id))
        return True
    
    def remove_from_cart(self, cart_item_id: int) -> bool:
        """Удаление товара из корзины"""
        query = "DELETE FROM cart_items WHERE cart_item_id = %s"
        self.execute_query(query, (cart_item_id,))
        return True
    
    def clear_cart(self, user_id: int) -> bool:
        """Очистка корзины пользователя"""
        query = "DELETE FROM cart_items WHERE user_id = %s"
        self.execute_query(query, (user_id,))
        return True