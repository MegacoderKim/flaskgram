# A FLASK SOCIAL NETWORK REST API

## Running Locally with Docker

Ensure you have docker and docker-compose installed

Enter the project root folder i.e `cd flaskgram`

Run the command `make`

This builds and runs the application

Visit `http://0.0.0.0:5000/swagger-ui` to access the swagger UI to the try out the API endpoints

Run `make build` to build the containers

## Other Commands

Run `make db-migrate` to make alembic migration after changes on the schema.

Run `make db-upgrade` to persist the migrations to the database.

## Testing

Run the command `make test`

## Linting

Run the command `make lint`
