from contextlib import asynccontextmanager

from fastapi import FastAPI

from router.vps import router as vps_router
from router.telegram import router as telegram_router
from service.telegram import alert
import asyncio
import logging





@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(alert())
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(vps_router)
app.include_router(telegram_router)
