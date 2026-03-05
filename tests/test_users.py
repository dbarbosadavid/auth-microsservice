def test_create_user_success(client):
    response = client.post("/user/register", json={
        "name": "Test User",
        "email": "teste@teste.com",
        "password": "12345678"
    })

    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["name"] == "TEST USER"
    assert response.json()["email"] == "teste@teste.com"
    assert response.json()["roles"] == ["USER"]

def test_login_success(client):
    response = client.post("/token/auth", json={
        "email": "teste@teste.com",
        "password": "12345678"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure(client):
    response = client.post("/token/auth", json={
        "email": "teste@teste.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    assert "detail" in response.json()

def test_update_user_success(client, access_token):
    response = client.put("/user/update", 
                           json={
                                "name": "test user updated",
                                "password": "newpassword123"
                            }, 
                            headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["name"] == "TEST USER UPDATED"
    assert response.json()["email"] == "teste@teste.com"
    assert response.json()["roles"] == ["USER"]

def test_login_new_password_success(client):
    response = client.post("/token/auth", json={
        "email": "teste@teste.com",
        "password": "newpassword123"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_delete_user_success(client, new_access_token):
    response = client.delete("/user/delete", headers={"Authorization": f"Bearer {new_access_token}"})

    assert response.status_code == 204



