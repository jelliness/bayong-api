def test_root_returns_service_name_and_status(client):
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["name"] == "Bayong Grocery Price Comparison API"


def test_health_check_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
