import os
import subprocess
import tempfile
from datetime import datetime, timedelta
from enum import Enum

from .authenticate import get_authenticated_lastfm_network
from .podcast import get_podcast_episode
from .types import Track


def open_editor() -> str:
    EDITOR = os.environ.get("EDITOR") or "editor"  # TODO
    INITIAL = "# artist - title (- album)\n"
    with tempfile.NamedTemporaryFile(suffix=".tmp", mode="w", delete=False) as tf:
        path = tf.name
        tf.write(INITIAL)
    subprocess.run([EDITOR, tf.name])
    with open(path, "r") as f:
        content = f.read()
    os.unlink(path)
    return content


def parse_line(s: str, t: datetime) -> Track:
    SEP = " - "
    match s.split(SEP):
        case _ as artist, _ as title:
            album = None
        case _ as artist, *titles, _ as album:
            title = SEP.join(titles)
        case _:
            raise ValueError(f"Invalid line {s}")
    return Track(artist=artist, title=title, timestamp=t, album=album)


def parse_txt(
    text: str, start_time: datetime | None = None, dt: timedelta = timedelta(minutes=5)
) -> list[Track]:
    # TODO: ideally, get each track's length
    # Probably want to separate parsing from time logic
    lines = [s for s in text.strip().splitlines() if not s.startswith("#")]
    if start_time is None:
        start_time = datetime.now() - len(lines) * dt
    return [parse_line(s, start_time + i * dt) for (i, s) in enumerate(lines)]


def scrobble_tracks(tracks: list[Track]):
    get_authenticated_lastfm_network().scrobble_many([t.to_kwargs() for t in tracks])


class InputMode(Enum):
    EDITOR = "editor"
    PODCAST = "podcast"


def scrobble(mode: InputMode = InputMode.EDITOR):  # TODO: options to read files etc
    match mode:
        case InputMode.EDITOR:
            text = open_editor()
            tracks = parse_txt(text)
        case InputMode.PODCAST:
            podcast, episode = get_podcast_episode()
            tracks = podcast.parse_episode(episode)

    print("Tracklist:")
    for i, t in enumerate(tracks):
        s = f"{i + 1:>2} | {t.timestamp.isoformat()} | {t.artist} - {t.title}"
        if t.album:
            s += f" - {t.album}"
        print(s)
    if input("Proceed with scrobble? (y/N): ").lower() == "y":
        scrobble_tracks(tracks)
        print("Scrobbled!")
    else:
        print("Not scrobbling")
