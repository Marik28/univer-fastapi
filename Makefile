run-dev:
	cd src; python -m univer_api

install: create-db
	pip install -r requirements.txt

dump:
	sqlite3 db.sqlite3 .dump > dump-$$(date "+%d-%m-%y_%H-%M-%S").sql

restore:
	sqlite3 db.sqlite3 < $(file)

create-db:
	cd src; python -m univer_api.scripts.create_db

add-table:
	cd src; python -m univer_api.scripts.add_table -t $(t) -f ../$(f)