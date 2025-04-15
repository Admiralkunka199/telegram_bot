from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from config import ADMIN_IDS
from database.db_manager import DatabaseManager

db = DatabaseManager()

class AdminMiddleware(BaseMiddleware):
    """Middleware для проверки, является ли пользователь администратором"""
    
    async def on_process_message(self, message: types.Message, data: dict):
        """Обработка сообщений"""
        await self._process_admin_check(message.from_user.id, message)
    
    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        """Обработка callback-запросов"""
        await self._process_admin_check(callback_query.from_user.id, callback_query)
    
    async def _process_admin_check(self, user_id: int, obj):
        """Проверка прав администратора"""
        # Если обработчик требует права администратора
        if getattr(obj, 'require_admin', False):
            # Проверяем, является ли пользователь администратором
            # Сначала проверяем в конфиге
            if user_id in ADMIN_IDS:
                return
            
            # Затем проверяем в базе данных
            is_admin = db.is_admin(user_id)
            if not is_admin:
                if isinstance(obj, types.Message):
                    await obj.answer("У вас нет прав для выполнения этой команды.")
                elif isinstance(obj, types.CallbackQuery):
                    await obj.answer("У вас нет прав для выполнения этого действия.", show_alert=True)
                raise CancelHandler()