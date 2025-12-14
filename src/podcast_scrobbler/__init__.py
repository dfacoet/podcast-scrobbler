import typer

from .authenticate import get_authenticated_lastfm_network
from .podcast import podcast
from .scrobble import scrobble
from .top import top

app = typer.Typer()


@app.command()
def user():
    network = get_authenticated_lastfm_network()
    user = network.get_authenticated_user()
    print(f"Authenticated: {user}")


app.command()(podcast)
app.command()(scrobble)
app.command()(top)


if __name__ == "__main__":
    app()
