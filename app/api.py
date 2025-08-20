from flask import Flask, request
from itertools import count
import app.logic as logic
import app.model as model


_events_logic = logic.EventsLogic()
counter1 = count(1)

class ApiException(Exception):
    pass

def _from_raw(raw_note: str) -> model.Events:
    parts = raw_note.split('|')
    events = model.Events()
    
    if len(parts) == 4:  # id|date|title|text
        events.id = parts[0]
        events.dates = parts[1]
        events.title = parts[2]
        events.text = parts[3]
    elif len(parts) == 3:
        events.id = None
        events.dates = parts[0]
        events.title = parts[1]
        events.text = parts[2]
    else:
        raise ApiException(f"invalid RAW note data {raw_note}")
    
    if not model.Events.validate_date(events.dates):
        raise ApiException(f"Invalid date format: {events.dates}. Expected YYYY-MM-DD")
    
    return events

def _to_raw(events: model.Events) -> str:
    logic.EventsLogic.num()
    if events.id is None:
        return f"{events.dates}|{events.title}|{events.text}"
    else:
        return f"{events.id}|{events.dates}|{events.title}|{events.text}"

API_ROOT = "/api/v1"
EVENTS_API_ROOT = API_ROOT + "/events"

def create_app():
    app = Flask(__name__)
    @app.route(EVENTS_API_ROOT + "/", methods=["POST"])
    def create():
        try:
            data = request.get_data().decode('utf-8')
            events = _from_raw(data)
            _id = _events_logic.create(events)
            return f"new id: {_id}", 201
        except ApiException as ex:
            return f"API error: {ex}", 400
        except Exception as ex:
            return f"failed to CREATE with: {ex}", 500

    @app.route(EVENTS_API_ROOT + "/", methods=["GET"])
    def list():
        try:
            events = _events_logic.list()
            raw_notes = ""
            for event in events:
                raw_notes = raw_notes + _to_raw(event) + '\n'
            return raw_notes, 200
        except Exception as ex:
            return f"failed to LIST with: {ex}", 500

    @app.route(EVENTS_API_ROOT + "/<_id>/", methods=["GET"])
    def read(_id: str):
        try:
            events = _events_logic.read(_id)
            if not events:
                return "Event not found", 404
            raw_note = _to_raw(events)
            return raw_note, 200
        except Exception as ex:
            return f"failed to READ with: {ex}", 500

    @app.route(EVENTS_API_ROOT + "/<_id>/", methods=["PUT"])
    def update(_id: str):
        try:
            data = request.get_data().decode('utf-8')
            event = _from_raw(data)
            _events_logic.update(_id, event)
            return "updated", 200
        except ValueError as ex:
            return f"Not found: {ex}", 404
        except ApiException as ex:
            return f"API error: {ex}", 400
        except Exception as ex:
            return f"failed to UPDATE with: {ex}", 500

    @app.route(EVENTS_API_ROOT + "/<_id>/", methods=["DELETE"])
    def delete(_id: str):
        try:
            _events_logic.delete(_id)
            return "deleted", 200
        except Exception as ex:
            return f"failed to DELETE with: {ex}", 500
    return app