# model.py
from datetime import datetime
from typing import Optional

class Events:
    def __init__(self):
        self.id: Optional[str] = None
        self.title: str = ""
        self.text: str = ""
        self.dates: str = ""
    
    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Проверка формата даты YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def get_current_date() -> str:
        """Возвращает текущую дату в формате YYYY-MM-DD"""
        return datetime.now().strftime('%Y-%m-%d')