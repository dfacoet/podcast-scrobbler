import urllib.request
from abc import ABC, abstractmethod
from datetime import datetime
from functools import cached_property
from typing import Any

import podcastparser

# TODO: podcastparser uses dictionaries
# should validate output and use pydantic models(?)


class Podcast(ABC):
    @property
    @abstractmethod
    def URL(self): ...

    @abstractmethod
    def print_episode(self, episode: dict[str, Any]): ...

    def get(self, max_episodes: int = 0) -> dict[str, Any]:
        url = self.URL
        return podcastparser.parse(url, urllib.request.urlopen(url), max_episodes)

    def get_episodes(self, max_episodes: int = 0) -> list[dict[str, Any]]:
        episodes = self.get(max_episodes)["episodes"]
        if max_episodes:
            assert len(episodes) <= max_episodes
        return episodes


class Battiti(Podcast):
    @cached_property
    def URL(self):
        return "https://giuliomagnifico.github.io/raiplay-feed/feed_battiti.xml"

    def print_episode(self, episode):
        print(f"Title: {episode['title']}")
        print(f"Published: {datetime.fromtimestamp(episode['published']).isoformat()}")
        print(f"Description:\n{episode['description']}")


KNOWN_PODCASTS: dict[str, Podcast] = {"Battiti": Battiti()}


def podcast():
    print("Podcasts available:")
    for t in sorted(KNOWN_PODCASTS):
        print(t)
    while True:
        title = input("Pick a podcast: ")
        try:
            podcast = KNOWN_PODCASTS[title]
            break
        except KeyError:
            print("Unknown podcast title")
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
    print("Selected episode:")
    podcast.print_episode(episode)
