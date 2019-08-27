"""Log incoming request data."""
import logging
import sys

import flask
import structlog
from healthcheck import EnvironmentDump, HealthCheck
from prometheus_client import make_wsgi_app
from werkzeug.wsgi import DispatcherMiddleware

from .config import APP_CONFIG
from .parser import ParserAPI

APP = flask.Flask(__name__)
APP.config.update(APP_CONFIG)

APP.add_url_rule('/v1/parser', view_func=ParserAPI.as_view('parser'), methods=['POST'], strict_slashes=False)
HealthCheck(app=APP, path='/health')
EnvironmentDump(
    app=APP, path="/health/env", include_python=False, include_os=False, include_process=False, include_config=True)

APP.wsgi_app = DispatcherMiddleware(APP.wsgi_app, {
    '/metrics': make_wsgi_app(),
})
LOGGING_FORMAT = '%(asctime)s [%(levelname)s] %(name)s:%(funcName)s:%(lineno)d - %(message)s'
logging.basicConfig(
    format=LOGGING_FORMAT,
    stream=sys.stdout,
    level=logging.INFO,
)

structlog.configure(
    processors=[
        structlog.processors.KeyValueRenderer(key_order=[
            "event",
            "request_id",
        ], ),
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
)

if __name__ != '__main__':
    GUNICORN_LOGGER = logging.getLogger('gunicorn.error')
    logging.root.setLevel(GUNICORN_LOGGER.level)
