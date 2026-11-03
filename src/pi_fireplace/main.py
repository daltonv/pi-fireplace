"""FastAPI app assembly. Keep playback logic out of this module."""

from fastapi import FastAPI

from pi_fireplace.api.routes import health, playback

app = FastAPI(title="Pi Fireplace", version="0.1.0")
app.include_router(health.router, prefix="/api/v1")
app.include_router(playback.router, prefix="/api/v1/playback")
