#Commande utilisé à l'installation :
#	https://docs.docker.com/compose/django/#connect-the-database
#install :
#	sudo docker-compose run web django-admin.py startproject universalConverterLatexSite

# Build the app
build :
	docker-compose up --build

# Run the app
run :
	docker-compose up &

# Stop the app
stop :
	docker-compose stop

# Open a python shell
python :
	docker exec -it universalconverterlatex_web_1 python manage.py shell

# Migrate db
db-migrate :
	docker exec -it universalconverterlatex_web_1 python manage.py makemigrations app

# Update db
db-update :
	docker exec -it universalconverterlatex_web_1 python manage.py migrate

# Access db
db-psql :
	psql -h 127.0.0.1 -U postgres postgres

# Test
test:
	docker exec -it universalconverterlatex_web_1 python manage.py test app

# Admin creation
admin:
	docker exec -it universalconverterlatex_web_1 python manage.py createsuperuser

# Enter the docker
bash:
	docker exec -it universalconverterlatex_web_1 bash