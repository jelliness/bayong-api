def _product_payload(**overrides):
    defaults = dict(
        category="Beverages",
        subcategory="Soft Drinks",
        product_name="Cola",
        brand="Acme",
        package_type="bottle",
        size_value="1.5",
        size_unit="L",
        standard_unit="L",
        standard_quantity="1.5",
        tags={},
        last_verified="2026-01-01",
    )
    defaults.update(overrides)
    return defaults


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


def _setup_product_and_store(client, auth_headers):
    product_id = client.post("/products", json=_product_payload(), headers=auth_headers).json()["id"]
    store_id = client.post("/stores", json=_store_payload(), headers=auth_headers).json()["id"]
    return product_id, store_id


def test_create_and_get_price(client, auth_headers):
    product_id, store_id = _setup_product_and_store(client, auth_headers)

    response = client.post(
        "/prices",
        json=dict(
            product_id=product_id,
            store_id=store_id,
            price="50.00",
            date_collected="2026-01-01",
            price_source="manual",
        ),
        headers=auth_headers,
    )
    assert response.status_code == 201
    price_id = response.json()["id"]

    response = client.get(f"/prices/{price_id}")
    assert response.status_code == 200
    assert response.json()["price"] == "50.00"


def test_get_price_not_found_returns_404(client):
    response = client.get("/prices/999")
    assert response.status_code == 404


def test_update_price_logs_history(client, auth_headers):
    product_id, store_id = _setup_product_and_store(client, auth_headers)
    create = client.post(
        "/prices",
        json=dict(
            product_id=product_id,
            store_id=store_id,
            price="50.00",
            date_collected="2026-01-01",
            price_source="manual",
        ),
        headers=auth_headers,
    )
    price_id = create.json()["id"]

    response = client.patch(f"/prices/{price_id}", json={"price": "45.00"}, headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["price"] == "45.00"

    history = client.get(f"/products/{product_id}/prices")
    assert history.status_code == 200


def test_delete_price(client, auth_headers):
    product_id, store_id = _setup_product_and_store(client, auth_headers)
    create = client.post(
        "/prices",
        json=dict(
            product_id=product_id,
            store_id=store_id,
            price="50.00",
            date_collected="2026-01-01",
            price_source="manual",
        ),
        headers=auth_headers,
    )
    price_id = create.json()["id"]

    response = client.delete(f"/prices/{price_id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/prices/{price_id}")
    assert response.status_code == 404
