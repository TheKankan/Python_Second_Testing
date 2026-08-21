# Fichier de test pour les routes liées aux utilisateurs

# test creation utilisateur
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


# test creation d'utilisateur avec email déjà pris
def test_create_user_duplicate_email(client):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "secretpassword",
    }

    client.post("/users", json=payload)

    payload_duplicate = {
        "name": "Bob",
        "email": "alice@example.com",  # Même email !
        "password": "anotherpassword",
    }
    response = client.post("/users", json=payload_duplicate)

    assert response.status_code == 400
    assert response.json()["detail"] == "Un utilisateur avec cet email existe déjà."


# test creation utilisateur avec email déjà pris
def test_create_user_invalid_email(client):
    payload = {
        "name": "Charlie",
        "email": "charlie-pas-un-email",
        "password": "secretpassword",
    }
    response = client.post("/users", json=payload)

    assert response.status_code == 422
