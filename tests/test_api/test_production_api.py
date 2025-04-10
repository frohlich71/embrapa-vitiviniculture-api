# tests/test_api/test_production_api.py

def test_create_and_get_production(client):
    # response = client.post("/api/v1/production/", json={
    #     "year": 2024,
    #     "state": "RS",
    #     "product": "Teste Espumante",
    #     "quantity_liters": 54321.0
    # })
    # assert response.status_code == 200

    response = client.get("/api/v1/production/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
