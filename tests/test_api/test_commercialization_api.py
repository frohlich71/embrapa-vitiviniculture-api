# tests/test_api/test_comercialization_api.py


def test_get_commercialization(client):
    response = client.get("/api/v1/commercialization/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
