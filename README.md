# UNIVER_API

REST-API на python с использованием фреймворка FastAPI.
Предоставляет API с информацией о расписании с возможностью 
фильтрации по группам, дням недели, четности недели и т.д.

## Требования

Версия python >=3.9

## Установка и запуск

    git clone https://github.com/Marik28/univer-fastapi.git    
    cd univer-fastapi
    pip install -r requirements.txt
    cd src/   
    python -m univer_api

## или при наличии утилиты *make*
    git clone https://github.com/Marik28/univer-fastapi.git    
    cd univer-fastapi
    make install
    make run-dev

## Документация
Документацию в спецификации OpenAPI можно просмотреть на 
эндпоинтах __/docs__ или __/redoc__ после запуска сервера