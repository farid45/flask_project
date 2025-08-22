"""Модуль для работы с базой данных событий."""

from typing import List

import app.model as model
import app.storage as storage


class DBException(Exception):
    """Исключение для ошибок работы с базой данных."""


class EventDB:
    """Класс для управления операциями с событиями в базе данных.
    
    Предоставляет CRUD операции для работы с событиями через
    абстракцию хранилища.
    """
    def __init__(self):
        """Инициализирует EventDB с локальным хранилищем."""
        self._storage = storage.LocalStorage()

    def create(self, events: model.Events) -> str:
        """Создает новое событие в базе данных.
        
        Args:
            events: Объект Events для создания
            
        Returns:
            str: ID созданного события
            
        Raises:
            DBException: Если операция создания не удалась
        """
        try:
            return self._storage.create(events)
        except Exception as ex:
            raise DBException("failed CREATE operation with:") from ex

    def list_events(self) -> List[model.Events]:
        """Возвращает список всех событий из базы данных.
        
        Returns:
            List[model.Events]: Список объектов Events
            
        Raises:
            DBException: Если операция получения списка не удалась
        """
        try:
            return self._storage.list()
        except Exception as ex:
            raise DBException("failed LIST operation with:") from ex

    def read(self, _id: str) -> model.Events:
        """Возвращает событие по указанному ID.
        
        Args:
            _id: ID события для поиска
            
        Returns:
            model.Events: Найденный объект Events
            
        Raises:
            DBException: Если операция чтения не удалась
        """
        try:
            return self._storage.read(_id)
        except Exception as ex:
            raise DBException("failed READ operation with:") from ex

    def update(self, _id: str, note: model.Events):
        """Обновляет существующее событие в базе данных.
        
        Args:
            _id: ID события для обновления
            note: Объект Events с новыми данными
            
        Raises:
            DBException: Если операция обновления не удалась
        """
        try:
            return self._storage.update(_id, note)
        except Exception as ex:
            raise DBException("failed UPDATE operation with:") from ex

    def delete(self, _id: str):
        """Удаляет событие по указанному ID из базы данных.
        
        Args:
            _id: ID события для удаления
            
        Raises:
            DBException: Если операция удаления не удалась
        """
        try:
            return self._storage.delete(_id)
        except Exception as ex:
            raise DBException("failed DELETE operation with:") from ex
