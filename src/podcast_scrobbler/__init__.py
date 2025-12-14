import typer

from .authenticate import get_authenticated_lastfm_network
from .podcast import podcast
from .scrobble import scrobble
from .top import top

app = typer.Typer()


@app.command(help="Authenticate and print the username")
def user():
    network = get_authenticated_lastfm_network()
    user = network.get_authenticated_user()
    print(f"Authenticated: {user}")


app.command(help="Get information about known podcasts")(podcast)
app.command(help="Scrobble a tracklist (opens a text editor)")(scrobble)
app.command(help="Get your top artists, tracks and albums")(top)


if __name__ == "__main__":
    app()
