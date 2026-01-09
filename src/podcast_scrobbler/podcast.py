import re
import urllib.request
from abc import ABC, abstractmethod
from datetime import datetime
from functools import cached_property
from typing import Any

import podcastparser

from .types import Track

# TODO: podcastparser uses dictionaries
# should validate output and use pydantic models(?)
type Episode = dict[str, Any]


class Podcast(ABC):
    @property
    @abstractmethod
    def URL(self): ...

    @abstractmethod
    def print_episode(self, episode: Episode): ...

    @abstractmethod
    def parse_episode(
        self, episode: Episode, t: datetime | None = None
    ) -> list[Track]: ...

    def get(self, max_episodes: int = 0) -> dict[str, Any]:
        url = self.URL
        return podcastparser.parse(url, urllib.request.urlopen(url), max_episodes)

    def get_episodes(self, max_episodes: int = 0) -> list[Episode]:
        episodes = self.get(max_episodes)["episodes"]
        if max_episodes:
            assert len(episodes) <= max_episodes
        return episodes


class Battiti(Podcast):
    @cached_property
    def URL(self):
        return "https://giuliomagnifico.github.io/raiplay-feed/feed_battiti.xml"

    def print_episode(self, episode: Episode):
        print(f"Title: {episode['title']}")
        print(f"Published: {datetime.fromtimestamp(episode['published']).isoformat()}")
        print(f"Description:\n{episode['description']}")

    def parse_line(self, s: str, t: datetime) -> Track | None:
        s = s.strip()
        artist_title = s.split(",", 1)
        if len(artist_title) < 2:
            print(f"Skipped parsing: {s}")
            return None
        artist = artist_title[0].strip().title()
        title = artist_title[1].split(", da", 1)[0].strip().title()
        album_match = re.search(r'da\s+"(.*?)"', s)
        album = album_match.group(1).title() if album_match else None

        return Track(artist=artist, title=title, timestamp=t, album=album)

    def parse_episode(self, episode: Episode, t: datetime | None = None) -> list[Track]:
        t = t or datetime.now()
        lines = [ss for s in episode["description"].split("//") if (ss := s.strip())]
        return [track for s in lines if (track := self.parse_line(s, t)) is not None]


KNOWN_PODCASTS: dict[str, Podcast] = {"Battiti": Battiti()}


def get_podcast_episode() -> tuple[Podcast, Episode]:
    print("Podcasts available:")
    podcast_titles = sorted(KNOWN_PODCASTS)
    for i, t in enumerate(podcast_titles):
        print(f"{i:>3}. {t}")
    while True:
        podcast_text = input("Pick a podcast: ")
        try:
            id = int(podcast_text)
        except ValueError:
            title = podcast_text
        else:
            try:
                title = podcast_titles[id]
            except IndexError:
                print(f"Invalid index {id}")
                continue
        try:
            podcast = KNOWN_PODCASTS[title]
            break
        except KeyError:
            print("Unknown podcast title {podcast}")
            continue
    episodes = podcast.get_episodes()
    print("Episodes: ")
    for i, ep in enumerate(episodes):
        print(f"{i:>3}. {ep['title']}")
    while True:
        k = input("Pick an episode number ")
        try:
            episode = episodes[int(k)]
            break
        except ValueError:
            print(f"{k} is not a number")
        except KeyError:
            print(f"Only {len(episodes)} available")
    return podcast, episode


def podcast():
    podcast, episode = get_podcast_episode()
    print("Selected episode:")
    podcast.print_episode(episode)
