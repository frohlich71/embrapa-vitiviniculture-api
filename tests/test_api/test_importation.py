def test_get_importation(client):
    response = client.get("/api/v1/importation/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
