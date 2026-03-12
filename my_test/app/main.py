from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import requests as requests_router, dispatcher, master
from app import seeds

app = FastAPI(title="Repair Requests")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(requests_router.router, prefix="/api/requests", tags=["requests"])
app.include_router(dispatcher.router, prefix="/api/dispatcher", tags=["dispatcher"])
app.include_router(master.router, prefix="/api/master", tags=["master"])

@app.on_event("startup")
def startup():
    seeds.seed_data()