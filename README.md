# HOW TO RUN #
**IMPORTANT: you have to provide username and password for monogodb through environment variables**
## with docker image ##
	-> download env-vars file from repo
	docker pull ahbar99/flask-mongo:latest
	
	docker run --publish 5000:5000 --env-file env_vars ahbar99/flask-mongo

## without docker image ##
	git clone https://github.com/Ahbar1999/flask-mongo-api.git

	cd flask-mongo-api

	python -m flask --app main run

# Features #
## Libraries Used ##
	1. Flask - Python microframework for building web apps
	2. Flask-Rest - Flask extension for building restful apis  	
	3. PyMongo - Mongodb client library
	4. faker - for generating fake/demo data
