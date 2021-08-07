run-dev:
	cd src; python -m univer_api

install:
	pip install -r requirements.txt
	echo "Все зависимости установлены"

dump:
	sqlite3 db.sqlite3 .dump > dump-$$(date "+%d-%m-%y_%H-%M-%S").sql
	echo "Дамп БД успешно создан"

restore:
	sqlite3 db.sqlite3 < $(file)
	echo "БД восстановлена из дампа"

create-db:
	cd src; python -m univer_api.scripts.create_db
	echo "БД успешно создана"

add-table:
	cd src; python -m univer_api.scripts.add_table -t $(t) -f ../$(f)
	echo "Таблица добавлены в БД"

drop-db:
	rm -f db.sqlite3
	echo "База данных удалена"

create-example: create-db
	cd src; python -m univer_api.scripts.create_example