import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from database.models import Base
from database.session import engine
from utils.config import settings
from utils.logging import configure_logging

configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix=settings.api_prefix)


@app.on_event("startup")
async def startup() -> None:
    try:
        async def _init_db() -> None:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        await asyncio.wait_for(_init_db(), timeout=3)
    except Exception:
        # Allow boot without DB for local demos; endpoints handle persistence best-effort.
        pass

try:
    from prometheus_fastapi_instrumentator import Instrumentator

    Instrumentator().instrument(app).expose(app)
except ImportError:
    # Keep service bootable even when optional monitoring dependency is missing.
    pass
