# tests/test_api/test_production_api.py


def test_get_production(client):
    response = client.get("/api/v1/production/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
