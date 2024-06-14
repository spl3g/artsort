from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.sql.models import Base
from sqlalchemy_utils import database_exists, create_database, drop_database
from app.dependencies import get_db
import os


POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')


SQLALCHEMY_DATABASE_URL = \
    f"postgresql://127.0.0.1:{POSTGRES_PORT}/test?user={POSTGRES_USER}&password={POSTGRES_PASSWORD}"  # noqa: E501

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)


if database_exists(engine.url):
    drop_database(engine.url)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_artworks():
    response = client.get("/api/v1/artworks")
    assert response.status_code == 200


def test_get_artwork():
    response = client.get("/api/v1/artworks/151424")
    assert response.status_code == 200
    assert response.json()['id'] == 151424


def test_post_kuwahara():
    response = client.post(
        "/api/v1/process/kuwahara",
        json={
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "artwork_id": 0,
            "window": 7,
        }
    )
    assert response.status_code == 200
    assert response \
        .json()['path'] \
        .startswith(
            '/images/processed/kuwahara_3fa85f64-5717-4562-b3fc-2c963f66afa6'
        )


def test_post_pixsort():
    response = client.post(
        "/api/v1/process/pixsort",
        json={
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "artwork_id": 0,
            "threashold_from": 0.25,
            "threashold_to": 0.75,
            "inverse_threashold": True,
        }
    )
    assert response.status_code == 200
    assert response \
        .json()['path'] \
        .startswith(
            '/images/processed/pixsort_3fa85f64-5717-4562-b3fc-2c963f66afa6'
        )
