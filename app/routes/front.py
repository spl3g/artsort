from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..dependencies import get_db, httpx_client
from typing import Annotated
from httpx import AsyncClient
from . import api

httpx_client_wrapper = Annotated[AsyncClient, Depends(httpx_client)]
router = APIRouter(default_response_class=HTMLResponse)
templates = Jinja2Templates(directory="app/templates")
db_session = Annotated[Session, Depends(get_db)]


@router.get("/")
async def get_artworks(
        request: Request,
        async_client: httpx_client_wrapper,
        db: db_session,
):
    r = await api.read_artworks(async_client, db)
    return templates. \
        TemplateResponse("artworks.html", {"request": request, "artworks": r})


@router.get("/artwork/{artwork_id}")
async def get_artwork(
        request: Request,
        artwork_id: int,
        async_client: httpx_client_wrapper,
        db: db_session,
):
    r = await api.read_artwork(artwork_id, async_client, db)
    return templates. \
        TemplateResponse("artwork.html", {"request": request, "artwork": r})


@router.get("/pixsort/{artwork_id}")
async def get_pixsort(
        request: Request,
        artwork_id: int,
        async_client: httpx_client_wrapper,
        db: db_session,
):
    r = await api.read_artwork(artwork_id, async_client, db)
    return templates. \
        TemplateResponse("pixsort.html", {"request": request, "artwork": r})


@router.post("/pixsort")
async def post_pixsort(
        request: Request,
        body: api.PixSort,
        async_client: httpx_client_wrapper,
        db: db_session,
):
    r = await api.pixsort(body, async_client, db)
    r = r['path']
    return templates. \
        TemplateResponse("partial/image.html", {"request": request, "url": r})


@router.get("/kuwahara/{artwork_id}")
async def get_kuwahara(
        request: Request,
        artwork_id: int,
        async_client: httpx_client_wrapper,
        db: db_session,
):
    r = await api.read_artwork(artwork_id, async_client, db)
    return templates. \
        TemplateResponse("kuwahara.html", {"request": request, "artwork": r})


@router.post("/kuwahara")
async def post_kuwahara(
        request: Request,
        body: api.Kuwahara,
        async_client: httpx_client_wrapper,
        db: db_session,
):
    r = await api.kuwahara(body, async_client, db)
    r = r['path']
    return templates. \
        TemplateResponse("partial/image.html", {"request": request, "url": r})
