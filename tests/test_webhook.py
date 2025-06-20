
def test_webhook_endpoint(client):
    data = {'event': 'test.event', 'payload': {'a': 1}}
    resp = client.post('/api/webhooks', json=data)
    assert resp.status_code == 201
    assert resp.get_json()['success'] is True
