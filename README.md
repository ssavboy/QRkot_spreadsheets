# QRKot Spreadsheets

QRKot Spreadsheets — это дополнение к проекту [QRKot](https://github.com/ssavboy/cat_charity_fund), которое выгружает данные фонда в Google Sheets для последующего анализа и отчётности.

## Возможности

- Экспорт данных о благотворительных проектах и пожертвованиях QRKot в Google Sheets.
- Формирование сводной таблицы для аналитики (например, незакрытые проекты, суммы пожертвований и т.п.) через интеграцию с Google API.
- Асинхронное взаимодействие с Google Sheets с помощью библиотеки Aiogoogle.
- API на FastAPI, совместимый по стилю и архитектуре с основным проектом QRKot.

## Стек технологий

- Python 3.9.
- FastAPI.
- SQLAlchemy (async).
- Asyncio.
- SQLite.
- Aiogoogle для работы с Google API.
- Alembic для миграций БД.

## Установка и запуск

Клонируйте репозиторий и перейдите в его директорию:

```bash
git clone git@github.com:ssavboy/QRkot_spreadsheets.git
cd QRkot_spreadsheets
```

Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
source venv/scripts/activate
```

Обновите `pip` и установите зависимости:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполните миграции базы данных:

```bash
alembic upgrade head
```

Запустите приложение:

```bash
uvicorn app.main:app
```

Документация по API будет доступна по адресам:

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Структура проекта

```text
QRkot_spreadsheets/
├── app/
│   ├── api/        # эндпоинты FastAPI
│   ├── core/       # конфигурация, настройки приложения
│   ├── crud/       # слой доступа к БД
│   ├── models/     # модели SQLAlchemy
│   ├── schemas/    # Pydantic-схемы
│   ├── sevices/    # сервисы, в т.ч. интеграция с Google Sheets
│   ├── __init__.py
│   └── main.py     # точка входа приложения
├── alembic/        # миграции
├── tests/          # тесты
├── alembic.ini
├── fastapi.db      # база данных (dev)
├── pytest.ini
├── requirements.txt
├── .flake8
├── .gitignore
└── README.md
```
