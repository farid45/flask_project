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
curl farid19.pythonanywhere.com/api/v1/events/ -X POST -d "YYYY-MM-DD|title|text"
```

### получение всего списка заметок
```
curl farid19.pythonanywhere.com/api/v1/events/
```

### получение заметки по идентификатору / ID == 1
```
curl farid19.pythonanywhere.com/api/v1/events/1/
```

### обновление текста заметки по идентификатору / ID == 1 /  новый текст == "new text"
```
curl farid19.pythonanywhere.com/api/v1/events/1/ -X PUT -d "|title|new text"
```

### удаление заметки по идентификатору / ID == 1
```
curl farid19.pythonanywhere.com/api/v1/events/1/ -X DELETE
```