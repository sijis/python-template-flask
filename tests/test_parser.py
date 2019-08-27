import pytest
from flask import url_for

ENDPOINT = 'parser'


def test_parser_status_nodata(client):
    """Endpoint status code with no data."""
    assert client.post(url_for(ENDPOINT)).status_code == 422


def test_parser_status_nodata_empty(client):
    """Endpoint status code with empty data."""
    assert client.post(url_for(ENDPOINT), json={}).status_code == 422


@pytest.mark.parametrize('event', ['generic_event.json'])
def test_parser_plugin_mirror(client, events, event):
    """Endpoint default response with mirror plugin."""
    generic_event_data = events(event)
    response = client.post(url_for(ENDPOINT), json=generic_event_data)
    assert response.status_code == 200
    assert response.json['received'] == generic_event_data
