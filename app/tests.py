from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_get_artworks():
    response = client.get("/api/v1/artworks")
    assert response.status_code == 200


def test_get_artwork():
    response = client.get("/api/v1/artworks/151424")
    assert response.status_code == 200


def test_post_kuwahara():
    response = client.post(
        "/api/v1/process/kuwahara",
        json='''{
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "artwork_id": 0,
            "window": 7
        }''')
    assert response.status_code == 422


def test_post_pixsort():
    response = client.post(
        "/api/v1/process/pixsort",
        json='''
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "artwork_id": 0,
                "threashold_from": 0.25,
                "threashold_to": 0.75,
                "inverse_threashold": false
        }
        ''')
    assert response.status_code == 422
