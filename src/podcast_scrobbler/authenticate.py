import pylast
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    lastfm_api_key: str
    lastfm_api_secret: str
    lastfm_session_key: str | None = None
    lastfm_username: str | None = None

    class Config:
        env_file = ".env"

    def has_session(self) -> bool:
        return self.lastfm_session_key and self.lastfm_username


def get_authenticated_lastfm_network() -> pylast.LastFMNetwork:
    settings = Settings()
    if not settings.has_session():
        import time
        import webbrowser

        network = pylast.LastFMNetwork(
            api_key=settings.lastfm_api_key, api_secret=settings.lastfm_api_secret
        )
        skg = pylast.SessionKeyGenerator(network)
        url = skg.get_web_auth_url()

        print(f"Please authorize this application to access your account at {url}\n")
        webbrowser.open(url)

        while not settings.lastfm_session_key:
            try:
                settings.lastfm_session_key, settings.lastfm_username = (
                    skg.get_web_auth_session_key_username(url)
                )
            except pylast.WSError:
                time.sleep(1)

        with open(".env", "a") as f:
            f.write(
                f"LASTFM_SESSION_KEY={settings.lastfm_session_key}\n"
                f"LASTFM_USERNAME={settings.lastfm_username}"
            )

    return pylast.LastFMNetwork(
        api_key=settings.lastfm_api_key,
        api_secret=settings.lastfm_api_secret,
        session_key=settings.lastfm_session_key,
        username=settings.lastfm_username,
    )
