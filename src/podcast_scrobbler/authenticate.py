import pylast
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError

REQUIRED_FOR_AUTH = {
    "lastfm_api_key",
    "lastfm_api_secret",
}


# ty does not know that Settings models can be instantiated without
# required fields, so we'll have some # type: ignore[missing-argument]
# Is there a better way?
class APISettings(BaseSettings):
    lastfm_api_key: str
    lastfm_api_secret: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


class AuthenticatedSettings(APISettings):
    lastfm_session_key: str
    lastfm_username: str


def authenticate():
    try:
        settings = APISettings()  # type: ignore[missing-argument]
    except ValidationError as e:
        raise RuntimeError("Missing API key or secret") from e

    import time
    import webbrowser

    network = pylast.LastFMNetwork(
        api_key=settings.lastfm_api_key, api_secret=settings.lastfm_api_secret
    )
    skg = pylast.SessionKeyGenerator(network)
    url = skg.get_web_auth_url()

    print(f"Please authorize this application to access your account at {url}\n")
    webbrowser.open(url)

    key, username = None, None
    while not (key and username):
        try:
            key, username = skg.get_web_auth_session_key_username(url)
        except pylast.WSError:
            time.sleep(1)

    with open(".env", "a") as f:
        f.write(f"\nLASTFM_SESSION_KEY={key}\nLASTFM_USERNAME={username}\n")
    print("Autheticated succesfully - username and key stored to .env")


def get_authenticated_lastfm_network() -> pylast.LastFMNetwork:
    try:
        settings = AuthenticatedSettings()  # type: ignore[missing-argument]
    except ValidationError:
        authenticate()
        settings = AuthenticatedSettings()  # type: ignore[missing-argument]

    return pylast.LastFMNetwork(
        api_key=settings.lastfm_api_key,
        api_secret=settings.lastfm_api_secret,
        session_key=settings.lastfm_session_key,
        username=settings.lastfm_username,
    )
