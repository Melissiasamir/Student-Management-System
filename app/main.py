"""
Application entrypoint.

Creates the FastAPI app, wires up database table creation, registers
routers, and adds a couple of application-wide conveniences (root
redirect, health check).
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.config import settings
from app.database import Base, engine
from app.routers import students


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup (idempotent for SQLite)."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
)

app.include_router(students.router)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Redirect the root path to the interactive Swagger docs."""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Health"], summary="Health check")
def health_check() -> dict[str, str]:
    """Simple liveness endpoint for monitoring/uptime checks."""
    return {"status": "ok"}
