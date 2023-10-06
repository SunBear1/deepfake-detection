import logging

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from endpoints.events import router as events_router
from endpoints.healthcheck import router as healthcheck_router
from endpoints.elevenLabsApi import router as elevenLabs_API

URL_PREFIX = "/api/v1"

app = FastAPI(
    title="Dokumentacja REST API",
    version="1.0.0",
    description="Dokumentacja REST API dla generatora deep-fakeów audio"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

api_router = APIRouter()

app.include_router(events_router, prefix=URL_PREFIX, tags=["Endpoints for event grid operations"])
app.include_router(healthcheck_router, prefix=URL_PREFIX, tags=["Endpoints for healthcheck operations"])
app.include_router(elevenLabs_API, prefix=URL_PREFIX, tags=["Endpoints for 11Labs operations"])
app.include_router(api_router)

logger = logging.getLogger("generator")

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
