from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from .routes import api
from .routes import front

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="static")
app.include_router(api.router)
app.include_router(front.router)
