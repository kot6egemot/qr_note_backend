Конфигурация поднимается из файла "PROJECT_FOLDER/.env.$**SERVER_MODE**"    
По умолчанию **SERVER_MODE**=local

Запуск сервера:  
    1. Скопировать ".env.example" в ".env.local"    
    2. Отредактировать строку подключения к Database.  
Выполнить команды:

    alembic upgrade head
    uvicorn app.main:app --reload --port 5000
........................................................................   
Команды для alembic.

    alembic revision --autogenerate -m "init"
    alembic upgrade head
    alembic downgrade -1
