"""Модуль локального хранилища для событий."""

from typing import List
import app.model as model


class LogicException(Exception):
    """Исключение для ошибок бизнес-логики."""


class StorageException(Exception):
    """Исключение для ошибок работы с хранилищем."""


class LocalStorage:
    """Класс для локального хранения событий в памяти.
    
    Обеспечивает базовые CRUD операции для управления событиями.
    """
    def __init__(self) -> None:
        """Инициализирует локальное хранилище."""
        self._id_counter = 0
        self._storage = {}

    def create(self, events: model.Events) -> str:
        """Создает новое событие в хранилище.
        
        Args:
            events: Объект Events для создания
            
        Returns:
            str: ID созданного события
        """
        self._id_counter += 1
        events.id = str(self._id_counter)
        self._storage[events.id] = events
        return events.id

    def list_events(self) -> List[model.Events]:
        """Возвращает список всех событий из хранилища.
        
        Returns:
            List[model.Events]: Список всех объектов событий
        """
        return list(self._storage.values())

    def read(self, _id: str) -> model.Events:
        """Возвращает событие по указанному ID.
        
        Args:
            _id: ID события для поиска
            
        Returns:
            model.Events: Найденный объект события
            
        Raises:
            StorageException: Если событие с указанным ID не найдено
        """
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        return self._storage[_id]

    def update(self, _id: str, note: model.Events) -> None:
        """Обновляет существующее событие в хранилище.
        
        Args:
            _id: ID события для обновления
            note: Объект Events с новыми данными
            
        Raises:
            StorageException: Если событие с указанным ID не найдено
        """
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        note.id = _id
        self._storage[note.id] = note

    def delete(self, _id: str) -> None:
        """Удаляет событие по указанному ID из хранилища.
        
        Args:
            _id: ID события для удаления
            
        Raises:
            StorageException: Если событие с указанным ID не найдено
        """
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        del self._storage[_id]
