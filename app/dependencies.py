import httpx
from .sql.database import SessionLocal


async def httpx_client():
    try:
        httpx_client_wrapper = httpx.AsyncClient()
        yield httpx_client_wrapper
    finally:
        await httpx_client_wrapper.aclose()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
