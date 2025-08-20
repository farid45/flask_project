from model import Events as EventsModel
from datetime import datetime
from typing import Dict, List

class EventsLogic:
    def __init__(self):
        self._storage: Dict[str, EventsModel] = {}
        self._date_index: Dict[str, str] = {}  # date -> event_id
    
    def create(self, event: EventsModel) -> str:
        # Проверяем формат даты
        if not EventsModel.validate_date(event.dates):
            raise ValueError(f"Неверный формат даты: {event.dates}. Ожидается YYYY-MM-DD")
        
        # Проверяем, нет ли уже события на эту дату
        if event.dates in self._date_index:
            existing_event_id = self._date_index[event.dates]
            raise ValueError(f"На дату {event.dates} уже существует событие с ID {existing_event_id}")
        
        event_id = str(len(self._storage) + 1)
        event.id = event_id
        
        # Сохраняем в основное хранилище и в индекс по датам
        self._storage[event_id] = event
        self._date_index[event.dates] = event_id
        
        return event_id
    
    def list(self) -> List[EventsModel]:
        return list(self._storage.values())
    
    def read(self, _id: str) -> EventsModel:
        return self._storage.get(_id)
    
    def read_by_date(self, date_str: str) -> EventsModel:
        """Получить событие по дате"""
        if not EventsModel.validate_date(date_str):
            raise ValueError(f"Неверный формат даты: {date_str}")
        
        event_id = self._date_index.get(date_str)
        if event_id:
            return self._storage[event_id]
        return None
    
    def update(self, _id: str, event: EventsModel):
        if _id not in self._storage:
            raise ValueError("Event not found")
        
        # Проверяем формат даты
        if not EventsModel.validate_date(event.dates):
            raise ValueError(f"Неверный формат даты: {event.dates}. Ожидается YYYY-MM-DD")
        
        # Получаем старое событие для проверки изменения даты
        old_event = self._storage[_id]
        
        # Если дата изменилась, проверяем новую дату на уникальность
        if old_event.dates != event.dates:
            if event.dates in self._date_index:
                existing_event_id = self._date_index[event.dates]
                # Если это не текущее событие (которое мы обновляем)
                if existing_event_id != _id:
                    raise ValueError(f"На дату {event.dates} уже существует событие с ID {existing_event_id}")
        
        # Обновляем данные
        event.id = _id
        self._storage[_id] = event
        
        # Обновляем индекс дат
        if old_event.dates in self._date_index:
            del self._date_index[old_event.dates]
        self._date_index[event.dates] = _id
    
    def delete(self, _id: str):
        if _id in self._storage:
            event = self._storage[_id]
            # Удаляем из индекса дат
            if event.dates in self._date_index:
                del self._date_index[event.dates]
            # Удаляем из основного хранилища
            del self._storage[_id]
    
    def is_date_available(self, date_str: str, exclude_event_id: str = None) -> bool:
        if not EventsModel.validate_date(date_str):
            return False
        
        if date_str not in self._date_index:
            return True
        
        # Если указано исключить определенное событие
        if exclude_event_id and self._date_index[date_str] == exclude_event_id:
            return True
        
        return False
    
    @staticmethod
    def num():
        pass