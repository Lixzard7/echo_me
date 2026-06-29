from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.websocket.audio_socket import router as websocket_router
from app.inference.service import voice_service
from app.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await voice_service.initialize()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.include_router(health_router)
app.include_router(websocket_router)