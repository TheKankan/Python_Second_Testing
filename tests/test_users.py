# 1. Test nominal : création réussie
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
    assert "password" not in data  # Vérifie que le MDP n'est PAS exposé


# 2. Test d'erreur : email déjà pris
def test_create_user_duplicate_email(client):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "secretpassword",
    }

    # Premier appel -> Succès
    client.post("/users", json=payload)

    # Deuxième appel avec le même email -> Doit échouer en 400
    payload_duplicate = {
        "name": "Bob",
        "email": "alice@example.com",  # Même email !
        "password": "anotherpassword",
    }
    response = client.post("/users", json=payload_duplicate)

    assert response.status_code == 400
    assert (
        response.json()["detail"] == "Un utilisateur avec cet email existe déjà."
    )


# 3. Test de validation Pydantic : format d'email invalide
def test_create_user_invalid_email(client):
    payload = {
        "name": "Charlie",
        "email": "charlie-pas-un-email",  # Email invalide
        "password": "secretpassword",
    }
    response = client.post("/users", json=payload)

    # Pydantic bloque la requête automatiquement avec un code 422
    assert response.status_code == 422