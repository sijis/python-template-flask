from flask import url_for

ENDPOINT = 'check'


def test_health_status(client):
    """Health endpoint status code."""
    assert client.get(url_for(ENDPOINT)).status_code == 200


def test_health_response(client):
    """Health endpoint response."""
    response = client.get(url_for(ENDPOINT))
    assert response.json['status'] == 'success'
