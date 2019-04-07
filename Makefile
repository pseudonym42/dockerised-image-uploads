run: build
	python manage.py runserver 0.0.0.0:7771

build: wait-for-db

	python manage.py makemigrations
	python manage.py migrate
	@echo "Creating default 'admin' user with password 'Admin555' ..."
	@python manage.py loaddata users.json

wait-for-db:
	@echo "Waiting until database is up ..."
	@until pg_isready -h db -q -U postgres ; do \
	  sleep 1 ; \
	done
	@echo "Database is up."

# test:
# 	coverage run manage.py test
