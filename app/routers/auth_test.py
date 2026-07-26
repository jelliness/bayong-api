from conftest import ADMIN_PASSWORD, ADMIN_USERNAME


def test_login_succeeds_with_correct_credentials(client, admin_user):
    response = client.post("/auth/login", data={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD})

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_fails_with_wrong_password(client, admin_user):
    response = client.post("/auth/login", data={"username": ADMIN_USERNAME, "password": "wrong-password"})

    assert response.status_code == 401


def test_login_fails_with_unknown_username(client):
    response = client.post("/auth/login", data={"username": "nobody", "password": "whatever"})

    assert response.status_code == 401


def test_write_endpoint_rejects_request_without_token(client):
    response = client.post("/categories", json={"category_name": "Snacks"})

    assert response.status_code == 401


def test_write_endpoint_rejects_garbage_token(client):
    response = client.post(
        "/categories",
        json={"category_name": "Snacks"},
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401


def test_write_endpoint_succeeds_with_valid_admin_token(client, auth_headers):
    response = client.post("/categories", json={"category_name": "Snacks"}, headers=auth_headers)

    assert response.status_code == 201


def test_read_endpoint_does_not_require_a_token(client):
    response = client.get("/categories")

    assert response.status_code == 200
