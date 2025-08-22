"""Модель данных для событий."""

from datetime import datetime
from typing import Optional


class Events:
    """Класс представляющий модель события.
    
    Attributes:
        id: Уникальный идентификатор события
        title: Заголовок события
        text: Текст описания события
        dates: Дата события в формате YYYY-MM-DD
    """


    def __init__(self) -> None:
        """Инициализирует объект события с значениями по умолчанию."""
        self.id: Optional[str] = None
        self.title: str = ""
        self.text: str = ""
        self.dates: str = ""


    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Проверяет корректность формата даты.
        
        Args:
            date_str: Строка с датой для проверки
            
        Returns:
            bool: True если дата в формате YYYY-MM-DD, иначе False
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False


    @staticmethod
    def get_current_date() -> str:
        """Возвращает текущую дату в стандартном формате.
        
        Returns:
            str: Текущая дата в формате YYYY-MM-DD
        """
        return datetime.now().strftime("%Y-%m-%d")
