run-dev:
	cd src; python -m univer_api

install:
	pip install -r requirements.txt;

dump:
	sqlite3 db.sqlite3 .dump > dump-$$(date "+%d-%m-%y_%H-%M-%S").sql

restore:
	sqlite3 db.sqlite3 < $(db)

create-db:
	cd src; python -m univer_api.create_db

add-table:
	cd src; python -m univer_api.scripts -t $(t) -f $(f)