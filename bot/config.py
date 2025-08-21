from pydantic import BaseModel
import os

class Config(BaseModel):
    api_id: int = int(os.getenv("API_ID", 0))
    api_hash: str = os.getenv("API_HASH", "")
    bot_token: str = os.getenv("BOT_TOKEN", "")
    assistant_session: str = os.getenv("ASSISTANT_SESSION", "")
    yt_cookies: str | None = os.getenv("YT_COOKIES") or None
    sudo_user_ids: list[int] = [int(x) for x in os.getenv("SUDO_USER_IDS", "").split(",") if x.strip().isdigit()]
    log_chat_id: int | None = int(os.getenv("LOG_CHAT_ID", 0)) or None
    spotify_client_id: str | None = os.getenv("SPOTIFY_CLIENT_ID") or None
    spotify_client_secret: str | None = os.getenv("SPOTIFY_CLIENT_SECRET") or None

CFG = Config()
