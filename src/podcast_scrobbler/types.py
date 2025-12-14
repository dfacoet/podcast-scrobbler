from datetime import datetime
from typing import Any

from pydantic import BaseModel


# Arguments of pylast's Network.scrobble
class ScrobbleArgs(BaseModel):
    artist: str
    title: str
    timestamp: int
    album: str | None = None
    album_artist: str | None = None
    track_number: int | None = None
    duration: int | None = None
    stream_id: str | None = None
    context: str | None = None
    mbid: str | None = None
    chosen_by_user: bool | None = None


class Track(BaseModel):
    artist: str
    title: str
    timestamp: datetime
    album: str | None = None

    def to_kwargs(self) -> dict[str, Any]:
        return ScrobbleArgs.model_validate(
            self.model_dump()
            | {"timestamp": int(self.timestamp.timestamp())}  # TODO: use serializer?
        ).model_dump()
