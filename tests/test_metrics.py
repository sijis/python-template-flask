def test_metrics_status(client):
    """Metrics endpoint status code."""
    assert client.get('/metrics').status_code == 200


def test_metrics_response(client):
    """Metrics endpoint response."""
    assert 'process_virtual_memory_bytes' in client.get('/metrics').get_data(as_text=True)
