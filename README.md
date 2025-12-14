# podcast-scrobbler

The aim of this project is to provide a simple interface to scrobble songs from music-oriented podcast tracklists.

## Setup
Use [uv](https://docs.astral.sh/uv/getting-started/installation) and [just](https://just.systems/man/en/introduction.html).

Needs a [Last.fm API key](https://www.last.fm/api/authentication), stored in `.env`. See `.env.example`.

## Run
```bash
just run --help
```

```bash
uv run scrobble --help
```

## Develop
Format, lint and typecheck:

```bash
just check
```
