import typer
from .authenticate import (
    get_authenticated_lastfm_network,
)  # TODO: relative import in package

app = typer.Typer()


@app.command()
def test_authentication():
    network = get_authenticated_lastfm_network()
    user = network.get_authenticated_user()
    print(f"Authenticated: {user}")
    top_artists = user.get_top_artists(limit=18)
    print("Your top artists:")
    for k, artist in enumerate(top_artists):
        print(f"{k + 1:>2}. {artist.item.name}: {artist.weight} scrobbles")


if __name__ == "__main__":
    app()
