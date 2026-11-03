"""HTTP endpoints for controlling playback (your implementation)."""

from fastapi import APIRouter

router = APIRouter(tags=["playback"])

# TODO: define your playback API contracts and Pydantic request/response models.
# TODO: call the MPV service; don't put socket / subprocess code in route handlers.
# Ideas: GET /state, POST /play, POST /pause, PUT /volume, PUT /media.
