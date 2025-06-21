def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "healthy"


def test_create_consultation(client):
    data = {
        "name": "Test",
        "phone": "+996700000001",
        "service_type": "test",
        "message": "Hi",
    }
    resp = client.post("/api/consultations", json=data)
    assert resp.status_code == 201
    assert resp.get_json()["success"] is True


def test_rate_limit(client):
    for _ in range(2):
        client.get("/api/health")
    resp = client.get("/api/health")
    assert resp.status_code == 429
