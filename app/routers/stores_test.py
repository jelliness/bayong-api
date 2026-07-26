def _store_payload(**overrides):
    defaults = dict(
        store_name="MegaMart",
        branch="Downtown",
        city="Metro City",
        province="Central",
        region="Region I",
        store_type="supermarket",
        has_membership=False,
    )
    defaults.update(overrides)
    return defaults


def test_create_and_get_store(client, auth_headers):
    response = client.post("/stores", json=_store_payload(), headers=auth_headers)
    assert response.status_code == 201
    store_id = response.json()["id"]

    response = client.get(f"/stores/{store_id}")
    assert response.status_code == 200
    assert response.json()["store_name"] == "MegaMart"


def test_get_store_not_found_returns_404(client):
    response = client.get("/stores/999")
    assert response.status_code == 404


def test_list_stores(client, auth_headers):
    client.post("/stores", json=_store_payload(store_name="MegaMart"), headers=auth_headers)
    client.post("/stores", json=_store_payload(store_name="ValueStore"), headers=auth_headers)

    response = client.get("/stores")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_store(client, auth_headers):
    create = client.post("/stores", json=_store_payload(), headers=auth_headers)
    store_id = create.json()["id"]

    response = client.patch(
        f"/stores/{store_id}", json={"store_name": "MegaMart Plus"}, headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["store_name"] == "MegaMart Plus"


def test_delete_store(client, auth_headers):
    create = client.post("/stores", json=_store_payload(), headers=auth_headers)
    store_id = create.json()["id"]

    response = client.delete(f"/stores/{store_id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/stores/{store_id}")
    assert response.status_code == 404
