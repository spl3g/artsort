from uuid import UUID
from fastapi.testclient import TestClient
from app.main import app
from app.sql.models import ProcessedImage, Image
from .test_artwork import TestingSessionLocal

client = TestClient(app)

with TestingSessionLocal() as db:
    pimage = ProcessedImage(**{
        "path": "/images/processed/pixsort_3fa85f64-5717-4562-b3fc-2c963f66afa6_2024-06-13 23:35:32.457201.png",  # noqa: E501
        "source_id": UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        "filter_type": "pixsort",
        "settings": {
            "threshold_from": 0.25,
            "threshold_to": 0.75,
            "inverse_threshold": True
        }
    })
    image = Image(**{
        "id": UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        "path": "/images/3fa85f64-5717-4562-b3fc-2c963f66afa6.png",
        "artwork_id": 1562,
    })
    db.add(image)
    db.add(pimage)
    db.commit()
    db.refresh(image)
    db.refresh(pimage)


def test_processed():
    json = {
        "path": "/images/processed/pixsort_3fa85f64-5717-4562-b3fc-2c963f66afa6_2024-06-13 23:35:32.457201.png",  # noqa: E501
        "source_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "filter_type": "pixsort",
        "settings": {
            "threshold_from": 0.25,
            "threshold_to": 0.75,
            "inverse_threshold": True
        }
    }

    response = client.get("/api/v1/process")
    assert json in response.json()


def test_processed_filter():
    json = {
        "path": "/images/processed/pixsort_3fa85f64-5717-4562-b3fc-2c963f66afa6_2024-06-13 23:35:32.457201.png",  # noqa: E501
        "source_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "filter_type": "pixsort",
        "settings": {
            "threshold_from": 0.25,
            "threshold_to": 0.75,
            "inverse_threshold": True
        }
    }

    response = client.get("/api/v1/process/pixsort")
    assert json in response.json()
