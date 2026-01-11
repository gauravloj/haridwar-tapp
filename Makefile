.PHONEY: server

server:
	hatch run python manage.py runserver

createsu:
	hatch run python manage.py createsuperuser
