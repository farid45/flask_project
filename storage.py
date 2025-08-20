from typing import List
import model
class LogicException(Exception):
    pass

class StorageException(Exception):
    pass

class LocalStorage:
    def __init__(self):
        self._id_counter = 0
        self._storage = {}

    def create(self, events: model.Events) -> str:
            self._id_counter += 1
            events.id = str(self._id_counter)
            self._storage[events.id] = events
            return events.id
    def list(self) -> List[model.Events]:
        return list(self._storage.values())

    def read(self, _id: str) -> model.Events:
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        return self._storage[_id]

    def update(self, _id: str, note: model.Events):
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        note.id = _id
        self._storage[note.id] = note

    def delete(self, _id: str):
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        del self._storage[_id]
