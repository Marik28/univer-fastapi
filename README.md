# UNIVER_API

REST-API на python с использованием фреймворка FastAPI.
Предоставляет API с информацией о расписании с возможностью 
фильтрации по группам, дням недели, четности недели и т.д.

## Требования

- Версия python >=3.9
- docker v. 20+ (+ docker compose)

## Установка и запуск при помощи утилиты *make*
    git clone https://github.com/Marik28/univer-fastapi.git    
    cd univer-fastapi
    cp .env-example .env
    make up

## Документация
Документацию в спецификации OpenAPI можно просмотреть на 
эндпоинтах __/docs__ или __/redoc__ после запуска сервера