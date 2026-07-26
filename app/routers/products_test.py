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


def test_create_and_get_product(client, auth_headers):
    response = client.post("/products", json=_product_payload(), headers=auth_headers)
    assert response.status_code == 201
    product_id = response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["product_name"] == "Cola"


def test_get_product_not_found_returns_404(client):
    response = client.get("/products/999")
    assert response.status_code == 404


def test_update_product(client, auth_headers):
    create = client.post("/products", json=_product_payload(), headers=auth_headers)
    product_id = create.json()["id"]

    response = client.patch(
        f"/products/{product_id}", json={"product_name": "Cola Zero"}, headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["product_name"] == "Cola Zero"


def test_delete_product(client, auth_headers):
    create = client.post("/products", json=_product_payload(), headers=auth_headers)
    product_id = create.json()["id"]

    response = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404


def test_list_products_filters_by_category_and_brand(client, auth_headers):
    client.post(
        "/products",
        json=_product_payload(category="Beverages", brand="Acme", product_name="Cola"),
        headers=auth_headers,
    )
    client.post(
        "/products",
        json=_product_payload(category="Snacks", brand="Other", product_name="Chips"),
        headers=auth_headers,
    )

    response = client.get("/products", params={"category": "Beverages", "brand": "Acme"})

    assert response.status_code == 200
    names = [p["product_name"] for p in response.json()]
    assert names == ["Cola"]


def test_list_products_filters_by_tag_query_param(client, auth_headers):
    client.post(
        "/products",
        json=_product_payload(product_name="Vegan Cola", tags={"vegan": True}),
        headers=auth_headers,
    )
    client.post(
        "/products",
        json=_product_payload(product_name="Regular Cola", tags={"vegan": False}),
        headers=auth_headers,
    )

    response = client.get("/products", params={"vegan": "true"})

    assert response.status_code == 200
    names = [p["product_name"] for p in response.json()]
    assert names == ["Vegan Cola"]


def test_get_product_prices_sorted_cheapest_first(client, auth_headers):
    product_id = client.post("/products", json=_product_payload(), headers=auth_headers).json()["id"]
    store_a_id = client.post(
        "/stores", json=_store_payload(store_name="MegaMart"), headers=auth_headers
    ).json()["id"]
    store_b_id = client.post(
        "/stores", json=_store_payload(store_name="ValueStore"), headers=auth_headers
    ).json()["id"]

    client.post(
        "/prices",
        json=dict(
            product_id=product_id,
            store_id=store_a_id,
            price="60.00",
            date_collected="2026-01-01",
            price_source="manual",
        ),
        headers=auth_headers,
    )
    client.post(
        "/prices",
        json=dict(
            product_id=product_id,
            store_id=store_b_id,
            price="45.00",
            date_collected="2026-01-01",
            price_source="manual",
        ),
        headers=auth_headers,
    )

    response = client.get(f"/products/{product_id}/prices")

    assert response.status_code == 200
    prices = [p["price"] for p in response.json()]
    assert prices == ["45.00", "60.00"]


def test_get_product_prices_not_found_for_missing_product(client):
    response = client.get("/products/999/prices")
    assert response.status_code == 404


def test_get_cheapest_price_returns_price_and_store(client, auth_headers):
    product_id = client.post("/products", json=_product_payload(), headers=auth_headers).json()["id"]
    store_id = client.post(
        "/stores", json=_store_payload(store_name="MegaMart"), headers=auth_headers
    ).json()["id"]

    client.post(
        "/prices",
        json=dict(
            product_id=product_id,
            store_id=store_id,
            price="60.00",
            date_collected="2026-01-01",
            price_source="manual",
        ),
        headers=auth_headers,
    )

    response = client.get(f"/products/{product_id}/cheapest")

    assert response.status_code == 200
    body = response.json()
    assert body["price"]["price"] == "60.00"
    assert body["store"]["store_name"] == "MegaMart"


def test_get_cheapest_price_not_found_when_no_prices(client, auth_headers):
    product_id = client.post("/products", json=_product_payload(), headers=auth_headers).json()["id"]

    response = client.get(f"/products/{product_id}/cheapest")

    assert response.status_code == 404
