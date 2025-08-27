"""API для управления событиями."""

from itertools import count

from flask import Flask, request

import app.logic as logic
import app.model as model

# Константы API
API_VERSION = "v1"
API_ROOT = f"/api/{API_VERSION}"
EVENTS_API_ROOT = f"{API_ROOT}/events"

# Логика работы с событиями



_events_logic = logic.EventsLogic()
_event_counter = count(1)


class ApiException(Exception):
    """Базовое исключение для ошибок API."""


class StorageException(Exception):
    """Исключение для ошибок хранилища."""


def _from_raw(raw_note: str) -> model.Events:
    """Преобразует сырые данные в объект Events.

    Args:
        raw_note: Строка в формате 'id|date|title|text' или 'date|title|text'

    Returns:
        Объект Events

    Raises:
        ApiException: При неверном формате данных или даты
    """
    parts = raw_note.split('|')
    events = model.Events()

    if len(parts) == 4:  # id|date|title|text
        events.id = parts[0]
        events.dates = parts[1]
        events.title = parts[2]
        events.text = parts[3]
    elif len(parts) == 3:  # date|title|text
        events.id = None
        events.dates = parts[0]
        events.title = parts[1]
        events.text = parts[2]
    else:
        error_msg = (
            f"Неверный формат данных: {raw_note}. "
            "Ожидаемые форматы: id|date|title|text или date|title|text"
        )
        raise ApiException(error_msg)

    if not model.Events.validate_date(events.dates):
        raise ApiException(
            f"Неверный формат даты: {events.dates}. Ожидается YYYY-MM-DD"
        )

    return events


def _to_raw(events: model.Events) -> str:
    """Преобразует объект Events в сырые данные.

    Args:
        events: Объект Events для преобразования

    Returns:
        Строка в формате 'id|date|title|text' или 'date|title|text'
    """
    logic.EventsLogic.num()
    if events.id is None:
        return f"{events.dates}|{events.title}|{events.text}"
    return f"{events.id}|{events.dates}|{events.title}|{events.text}"


def create_app():
    """Создает и настраивает Flask приложение.

    Returns:
        Flask приложение с настроенными маршрутами API
    """
    app = Flask(__name__)

    @app.route(EVENTS_API_ROOT + "/", methods=["POST"])
    def create():
        """Создает новое событие.

        Returns:
            Ответ с ID созданного события или сообщение об ошибке
        """
        try:
            data = request.get_data().decode('utf-8')
            events = _from_raw(data)
            event_id = _events_logic.create(events)
            return f"Новый ID: {event_id}", 201
        except ApiException as ex:
            return f"Ошибка API: {ex}", 400
        except ValueError as ex:
            return f"Ошибка валидации: {ex}", 400
        except (ImportError, AttributeError, RuntimeError) as ex:
            return f"Внутренняя ошибка сервера: {ex}", 500

    @app.route(EVENTS_API_ROOT + "/", methods=["GET"])
    def list_events():
        """Возвращает список всех событий.

        Returns:
            Список событий в сыром формате или сообщение об ошибке
        """
        try:
            events = _events_logic.list_events()
            raw_notes = ""
            for event in events:
                raw_notes = raw_notes + _to_raw(event) + '\n'
            return raw_notes, 200
        except (ImportError, AttributeError, RuntimeError) as ex:
            return f"Ошибка при получении списка: {ex}", 500

    @app.route(EVENTS_API_ROOT + "/<_id>/", methods=["GET"])
    def read(_id: str):
        """Возвращает событие по ID.

        Args:
            _id: ID события для поиска

        Returns:
            Событие в сыром формате или сообщение об ошибке
        """
        try:
            events = _events_logic.read(_id)
            if not events:
                return "Событие не найдено", 404
            raw_note = _to_raw(events)
            return raw_note, 200
        except (ImportError, AttributeError, RuntimeError) as ex:
            return f"Ошибка при чтении: {ex}", 500

    @app.route(EVENTS_API_ROOT + "/<_id>/", methods=["PUT"])
    def update(_id: str):
        """Обновляет существующее событие.

        Args:
            _id: ID события для обновления

        Returns:
            Сообщение об успехе или ошибке
        """
        try:
            data = request.get_data().decode('utf-8')
            event = _from_raw(data)
            _events_logic.update(_id, event)
            return "Обновлено", 200
        except ApiException as ex:
            return f"Ошибка API: {ex}", 400
        except ValueError as ex:
            return f"Ошибка: {ex}", 404
        except (ImportError, AttributeError, RuntimeError) as ex:
            return f"Ошибка при обновлении: {ex}", 500

    @app.route(EVENTS_API_ROOT + "/<_id>/", methods=["DELETE"])
    def delete(_id: str):
        """Удаляет событие по ID.

        Args:
            _id: ID события для удаления

        Returns:
            Сообщение об успехе или ошибке
        """
        try:
            _events_logic.delete(_id)
            return "Удалено", 200
        except (ImportError, AttributeError, RuntimeError) as ex:
            return f"Ошибка при удалении: {ex}", 500

    return app
