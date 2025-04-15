def test_get_processing(client):
    response = client.get("/api/v1/processing/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
