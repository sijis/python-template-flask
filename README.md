# Python Template Flask

A template of a sample Flask application.

## Build and Run

The steps below builds and runs the local application.

```bash
$ docker build -t python-template-flask .
$ docker run --rm -p 8080:8080 python-template-flask
$ curl http://localhost:8080/health
```

Alternatively, we can run flask directly.

```bash
$ pip install -e .
$ FLASK_ENV=development python -m python_template_flask
```

Send sample data
```
curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST http://0.0.0.0:8080/v1/parser
```

## Configuration

### Database

A database can be defined in `settings.yaml`, as:
```
staging:
  DEBUG: True
  DB:
    URI: "postgresql://postgres:mysecretpassword@localhost:$PORT/postgres"
    OPTIONS:
      pool_recycle: 2
```

Valid options for `URI` are sqlalchemy connection strings.

The `$PORT` variable will be replaced with the temporary port when running tests.

## Testing

We are using `tox` to run through unit and style checks.

```bash
$ pip install -r requirements-dev.txt
$ tox
```
