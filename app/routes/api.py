from typing import Annotated
from uuid import UUID
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.sql.schemas import Image, ProcessedImage
from ..dependencies import httpx_client, get_db
from ..sql import crud, schemas
from httpx import AsyncClient
from datetime import datetime
from random import randint
import subprocess

BASE_URL = "https://api.artic.edu/api/v1"
router = APIRouter(prefix="/api/v1")
httpx_client_wrapper = Annotated[AsyncClient, Depends(httpx_client)]
db_session = Annotated[Session, Depends(get_db)]


class Kuwahara(BaseModel):
    id: UUID
    artwork_id: int
    window: int = 7


class PixSort(BaseModel):
    id: UUID
    artwork_id: int
    threashold_from: float = 0.25
    threashold_to: float = 0.75
    inverse_threashold: bool = False


@router.get("/artworks")
async def read_artworks(async_client: httpx_client_wrapper, db: db_session):
    params = {"fields": "id,title,image_id,artist_title",
              "page": randint(1, 10), "limit": 12}
    r = await async_client.get(f"{BASE_URL}/artworks/search", params=params)
    r = r.json()
    for artwork in r["data"]:
        image = crud.get_image(db, UUID(artwork["image_id"]))
        if image:
            iurl = image.path
        else:
            iurl = f"{r['config']['iiif_url']}/{artwork['image_id']}/full/843,/0/default.jpg"  # noqa: E501

        artwork["image_url"] = iurl
    return r["data"]


@router.get("/artworks/{artwork_id}")
async def read_artwork(
        artwork_id: int,
        async_client: httpx_client_wrapper,
        db: db_session,
):
    params = {
        "fileds": "id,title,image_id,description,artist_title,date_start,date_end"  # noqa: E501
    }
    r = await \
        async_client.get(f"{BASE_URL}/artworks/{artwork_id}", params=params)
    r = r.json()
    image = crud.get_image(db, UUID(r["data"]["image_id"]))
    if image:
        iurl = image.path
    else:
        iurl = f"{r['config']['iiif_url']}/{r['data']['image_id']}/full/843,/0/default.jpg"  # noqa: E501
    r["data"]["image_url"] = iurl
    return r["data"]


@router.post("/process/kuwahara")
async def kuwahara(
        body: Kuwahara,
        async_client: httpx_client_wrapper,
        db: db_session
):
    image = crud.get_image(db, body.id)
    settings = {
        'window': body.window
    }
    filename = f"images/{body.id}.jpg"
    if image:
        iurl = image.path
        processed_image = crud.get_processed_image_pro(
            db, body.id, "kuwahara", settings)
        if processed_image:
            return {'path': processed_image.path}
    else:
        iurl = f"https://www.artic.edu/iiif/2/{body.id}/full/843,/0/default.jpg"  # noqa: E501
        r = await async_client.get(iurl)
        open(filename, 'wb').write(r.content)
        image = Image(id=body.id, artwork_id=body.artwork_id,
                      path="/" + filename, processed=[])
        crud.create_image(db, image)

    output = f"images/processed/kuwahara_{body.id}_{datetime.now()}.png"
    subprocess.run([
        "./clis/kuwahara",
        f"{filename}",
        output,
        f"{body.window}"
    ])

    processed_image = ProcessedImage(
        path="/" + output,
        source_id=body.id,
        filter_type="kuwahara",
        settings=settings,
    )
    crud.create_processed_image(db, processed_image)
    return {'path': '/' + output}


@router.post("/process/pixsort")
async def pixsort(
        body: PixSort,
        async_client: httpx_client_wrapper,
        db: db_session,
):
    image = crud.get_image(db, body.id)
    settings = {
        "threshold_from": body.threashold_from,
        "threshold_to": body.threashold_to,
        "inverse_threshold": body.inverse_threashold,
    }
    filename = f"images/{body.id}.jpg"
    if image:
        iurl = image.path
        processed_image = crud.get_processed_image_pro(
            db, body.id, "pixsort", settings)
        if processed_image:
            return {'path': processed_image.path}
    else:
        iurl = f"https://www.artic.edu/iiif/2/{body.id}/full/843,/0/default.jpg"  # noqa: E501
        r = await async_client.get(iurl)
        open(filename, 'wb').write(r.content)
        image = Image(
            id=body.id,
            artwork_id=body.artwork_id,
            path="/" + filename,
            processed=[]
        )
        crud.create_image(db, image)

    output = f"images/processed/pixsort_{body.id}_{datetime.now()}.png"
    subprocess.run([
        "./clis/pixsort",
        f"{filename}",
        output,
        f"{body.threashold_from}",
        f"{body.threashold_to}",
        f"{body.inverse_threashold}",
    ])

    processed_image = ProcessedImage(
        path="/" + output,
        source_id=body.id,
        filter_type="pixsort",
        settings=settings,
    )
    crud.create_processed_image(db, processed_image)
    return {'path': '/' + output}


@router.get('/process', response_model=list[schemas.ProcessedImage])
async def get_processed(db: db_session):
    return crud.get_processed_images(db)


@router.get(
    '/process/{filter_type}',
    response_model=list[schemas.ProcessedImage],
)
async def get_processed_by(filter_type: str, db: db_session):
    return crud.get_processed_images_by_filter(db, filter_type)
