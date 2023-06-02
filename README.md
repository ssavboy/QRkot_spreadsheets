# Google Sheets для QRKot
Проект [QRKot](https://github.com/ssavboy/cat_charity_fund) — это приложение для Благотворительного фонда поддержки котиков QRKot.

## Клонирование и запуск проекта

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:ssavboy/cat_charity_fund.git
```
```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
* Если у вас Linux/macOS
    ```
    source venv/bin/activate
    ```
* Если у вас windows
    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Выполнить миграции
```
alembic upgrade head
```

Запустить приложение
```
uvicorn app.main:app 
```

Эндпоинты можно посмотреть в документации
- [Swagger](http://127.0.0.1:8000/docs)
- [Redoc](http://127.0.0.1:8000/redoc)

### Стек:
 - Python 3.9
 - FastAPI
 - SQLAlchemy
 - Asyncio
 - SQlite
 - Aiogoogle

### Автор [Kirill Molchanov](https://github.com/ssavboy)