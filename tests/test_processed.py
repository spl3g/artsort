from uuid import UUID
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.sql.models import ProcessedImage
from app.sql.models import Base
from app.dependencies import get_db
from sqlalchemy.pool import StaticPool


client = TestClient(app)
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # noqa: E501

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
with TestingSessionLocal() as db:
    image = ProcessedImage(**{
                "path": "/images/processed/pixsort_3fa85f64-5717-4562-b3fc-2c963f66afa6_2024-06-13 23:35:32.457201.png",  # noqa: E501
                "source_id": UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
                "filter_type": "pixsort",
                "settings": {
                    "threshold_from": 0.25,
                    "threshold_to": 0.75,
                    "inverse_threshold": True
                }
            })
    db.add(image)
    db.commit()
    db.refresh(image)

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
app.dependency_overrides = {}
