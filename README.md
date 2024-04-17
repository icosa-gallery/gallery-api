# Icosa API

Repository for Icosa API

## Docker quick start

Copy the following files:

- `cp example.env .env`
- `cp fastapi/config.example.json fastapi/config.json`
- `cp fastapi/gcp-service-account.example.json fastapi/gcp-service-account.json`

Or create and fill them in manually.

When running in docker, the api service needs its host specified as `db` instead of `localhost` where `db` is the postgres service name. This is currently set in the `dblocation` key inside `config.json`.

Before running for the first time, build the project:

`docker compose build`

Then:

`docker compose up -d`

TODO: When running  `docker compose up -d` for the first time, the api service may start before postgres is fully available and fail to start. Subsequent runs should work as expected.

## Services

### Direct from localhost

- web front end: localhost:3000
- fastapi backend: localhost:8000
- django backend: localhost:8001

### Using the included proxy

Let's say, you've set `DEPLOYMENT_HOST` in `.env` to `icosa.localhost`, you can access the following services thus:

- web front end: http://icosa.localhost
- fastapi backend: http://api.icosa.localhost
- django backend: http://api-django.icosa.localhost

You'll need to add the following line to your `/etc/hosts` file (or the equivalent on Windows):

`127.0.0.1       icosa.localhost`
