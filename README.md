## Установка необходимых пакетов
```
pip install -r requirements.txt
```
## запуск приложения
```
python3 run.py run
```


## cURL тестирование

### добавление новой заметки
```
curl http://127.0.0.1:5000/api/v1/events/ -X POST -d "YYYY-MM-DD|title|text"
```

### получение всего списка заметок
```
curl http://127.0.0.1:5000/api/v1/events/
```

### получение заметки по идентификатору / ID == 1
```
curl http://127.0.0.1:5000/api/v1/events/1/
```

### обновление текста заметки по идентификатору / ID == 1 /  новый текст == "new text"
```
curl http://127.0.0.1:5000/api/v1/events/1/ -X PUT -d "|title|new text"
```

### удаление заметки по идентификатору / ID == 1
```
curl http://127.0.0.1:5000/api/v1/events/1/ -X DELETE
```