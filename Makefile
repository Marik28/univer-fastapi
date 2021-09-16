run-dev:
	cd src; python -m univer_api

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	echo "Все зависимости установлены"

dump:
	sqlite3 db.sqlite3 .dump > dump-$$(date "+%d-%m-%y_%H-%M-%S").sql
	echo "Дамп БД успешно создан"

restore:
	sqlite3 db.sqlite3 < $(file)
	echo "БД восстановлена из дампа"

create-db:
	cd src; python -m scripts.create_db
	echo "БД успешно создана"

add-table:
	cd src; python -m scripts.add_table -t $(t) -f ../$(f)
	echo "Таблица добавлена в БД"

drop-db:
	cd src; python -m scripts.drop_db
	echo "База данных удалена"

create-example: create-db
	cd src; python -m scripts.create_example

add-all-data:
	make add-table t=teachers f=data/csv_data/teachers.csv
	make add-table t=classrooms f=data/csv_data/lessons.csv
	make add-table t=subjects f=data/csv_data/lessons.csv
	make add-table t=groups f=data/csv_data/groups.csv
	make add-table t=lessons f=data/csv_data/lessons.csv

parse-schedule:
	cd src; python -m scripts.parse_schedule --html=../$(html) --group=$(group) --subgroup=$(subgroup) --csv ../$(csv)

admin-run-dev:
	cd src; python -m admin

admin-run-prod:
	cd src; gunicorn -b 127.0.0.1:5000 admin.wsgi:app

revision:
	cd src; alembic revision --autogenerate

migrate:
	cd src; alembic upgrade head