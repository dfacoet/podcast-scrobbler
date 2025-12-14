from enum import Enum

import typer
from pylast import Album, Artist, TopItem, Track

from . import get_authenticated_lastfm_network


class TopType(Enum):
    ARTISTS = "artists"
    ALBUMS = "albums"
    TRACKS = "tracks"


# TODO: better formatting, align number of scrobbles


def format_top_item(i: TopItem) -> str:
    base: str
    match i.item:
        case Artist(name=name):
            base = name
        case Album(artist=artist, title=title) | Track(artist=artist, title=title):
            base = f"{artist} - {title}"
    return f"{base}: {i.weight} scrobbles"


def top(top_type: TopType, n: int = typer.Argument(20)):
    network = get_authenticated_lastfm_network()
    user = network.get_authenticated_user()
    match top_type:
        case TopType.ARTISTS:
            method = user.get_top_artists
        case TopType.ALBUMS:
            method = user.get_top_albums
        case TopType.TRACKS:
            method = user.get_top_tracks
    top = method(limit=n)
    print(f"Your top {top_type.value}:")
    for k, x in enumerate(top):
        print(f"{k + 1:>2}. {format_top_item(x)}")
