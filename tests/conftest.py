import json

import pytest

from python_template_flask.app import APP


@pytest.fixture
def app():
    """Flask application."""
    return APP


@pytest.fixture
def events(shared_datadir):
    def _events(name):
        contents = (shared_datadir / name).read_text()
        return json.loads(contents)

    return _events
