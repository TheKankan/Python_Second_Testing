# Fichier de test pour les routes liées aux utilisateurs

# test creating user successfully
def test_create_user_success(client):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "secretpassword",
    }
    response = client.post("/users", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data
    assert "password" not in data


# test creating user with duplicate email
def test_create_user_duplicate_email(client):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "secretpassword",
    }

    client.post("/users", json=payload)

    payload_duplicate = {
        "name": "Bob",
        "email": "alice@example.com",  # same mail
        "password": "anotherpassword",
    }
    response = client.post("/users", json=payload_duplicate)

    assert response.status_code == 400
    assert response.json()["detail"] == "This email is already registered."


# test creating user with invalid email
def test_create_user_invalid_email(client):
    payload = {
        "name": "Charlie",
        "email": "charlie_not_email", # Invalid email format
        "password": "secretpassword",
    }
    response = client.post("/users", json=payload)

    assert response.status_code == 422

# test creating user with duplicate username
def test_create_user_duplicate_username(client):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "secretpassword",
    }

    client.post("/users", json=payload)

    payload_duplicate = {
        "name": "Alice", # same username
        "email": "bob@example.com",
        "password": "anotherpassword",
    }
    response = client.post("/users", json=payload_duplicate)

    assert response.status_code == 400
    assert response.json()["detail"] == "This username is already taken."


    # TODO : add more tests (getting users, getting user by id, trying to register with invalid password or username, etc.)
    # TODO : also add security for password & username (disable some special characters, etc.)