# HOW TO RUN #
## with docker image ##
	docker pull ahbar99/flask-mongo:latest
	
	docker run --publish 5000:5000 ahbar99/flask-mongo

## without docker image ##
	git clone https://github.com/Ahbar1999/flask-mongo-api.git

	cd flask-mongo-api

	python -m flask --app main run

# Features #
## Libraries Used ##
	1. Flask - Python microframework for building web apps
	2. PyMongo - Mongodb client library
	3. faker - for generating fake/demo data
