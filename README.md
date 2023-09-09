# Mood API

This project implements a basic CRUD api for an application that collects mood data, auths/tracks users, and provides insights.

# Basic tech

It uses the python web app framework FastAPI built on modern python tools. Specificly, in this app, it helps provide an asyncronous framework for io bound processing; interactive api docs with swagger; typing and validation with pydantic; OAuth2 with JWT tokens and authorization based on users; and unit tests via pytest and coverage.  It uses MongoDB as the datastore via an async driver and includes Dockerfile/compose files for the basics of potential deployment.

# Setup

To run locally, setup a python environment with python 3.10, e.g. with conda as a package manager:

```sh
conda create --name mood_test python=3.10 -f environment.yml
conda activate mood_test
```

Or in case you have an py310 environment handy but not conda, you can just use the included requirements.txt and get rid of the conda stuff.

To install MongoDB (assuming ubuntu):

```sh
sudo apt install mongodb
```

And start it at the root of the project (in a different terminal):

```sh
mongodb --dbpath /store
```

If all goes well you should be able to, from the root of the project, start the server in dev mode via:

```sh
python main.py
```

And manually send requests such as:

```
 curl -X 'GET' \
  'http://localhost:8080/moodevents/' \
  -H 'accept: application/json'
```

Or you can just visit the interactive docs in browser at `http://127.0.0.1:8080/docs` where you can make requests to any endpoint, including going through the auth flow to get a JWT token and making requests to protected endpoints as a user.

You can run tests for the routes and user process from the root of the project via:

```sh
python -m pytest tests
```

And create and view a coverage report via:

```sh
coverage run -m pytest
coverage report
```

Finally, if you have docker setup, you can build the app in a docker image, pull and build mongodb in another, and then deploy them locally from the root directory with:

```sh
docker build -t mood-test-api .
docker pull mongo
docker-compose up -d
```

NOTE: there was some funkyness going on with env variables (the .env and .env.prod files) that I gave up on.  Before building the docker image, replace 'localhost' in the .env file with 'database' (and vice versa before running locally without docker)

# Data Model

There are two primary Models that tie together the api's endpoints, data structures, and database Collections:
 
 1. Users
    - email
    - password
 2. MoodEvent
    - creator (for auth)
    - mood_type
    - timestamp
    - lat
    - lon

The fields and routes are implemented to be appropriate for the domain while being as simple and quick to complete as possible.  And the requested functionality regarding locations is just mocked/hard coded via an included pretend location module.

There is some general CRUD functionality for Users and MoodEvents but for the endpoints that were specifically requested we have:

1. create a new mood record: POST /moodevents/new
2. get a distribution of moods: GET /moodevents/dist
3. get proximate happy locations: GET /moodevents/happy

These can only be accessed after signing up a User and then Signing in with that user.  And a user only has access to MoodEvents that they created themselves.