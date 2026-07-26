def test_create_and_get_category(client, auth_headers):
    response = client.post("/categories", json={"category_name": "Snacks"}, headers=auth_headers)
    assert response.status_code == 201
    category_id = response.json()["id"]

    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["category_name"] == "Snacks"


def test_get_category_not_found_returns_404(client):
    response = client.get("/categories/999")
    assert response.status_code == 404


def test_list_categories_returns_created_entries(client, auth_headers):
    client.post("/categories", json={"category_name": "Snacks"}, headers=auth_headers)
    client.post("/categories", json={"category_name": "Beverages"}, headers=auth_headers)

    response = client.get("/categories")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_category(client, auth_headers):
    create = client.post("/categories", json={"category_name": "Snacks"}, headers=auth_headers)
    category_id = create.json()["id"]

    response = client.patch(
        f"/categories/{category_id}", json={"category_name": "Chips"}, headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["category_name"] == "Chips"


def test_update_category_not_found_returns_404(client, auth_headers):
    response = client.patch("/categories/999", json={"category_name": "Chips"}, headers=auth_headers)
    assert response.status_code == 404


def test_delete_category(client, auth_headers):
    create = client.post("/categories", json={"category_name": "Snacks"}, headers=auth_headers)
    category_id = create.json()["id"]

    response = client.delete(f"/categories/{category_id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 404


def test_delete_category_not_found_returns_404(client, auth_headers):
    response = client.delete("/categories/999", headers=auth_headers)
    assert response.status_code == 404


def test_create_category_rejects_unedited_swagger_example(client, auth_headers):
    response = client.post(
        "/categories",
        json={"category_name": "string", "parent_category": "string"},
        headers=auth_headers,
    )

    assert response.status_code == 422
    assert client.get("/categories").json() == []
