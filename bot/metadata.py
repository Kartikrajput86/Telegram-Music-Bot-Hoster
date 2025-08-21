from __future__ import annotations
import yt_dlp
from typing import Optional
from .config import CFG

_YDL_OPTS_BASE = {
    "quiet": True,
    "nocheckcertificate": True,
    "geo_bypass": True,
    "noplaylist": True,
    "skip_download": True,
}

if CFG.yt_cookies:
    _YDL_OPTS_BASE["cookiefile"] = CFG.yt_cookies

def yt_search_or_info(query: str) -> dict:
    opts = _YDL_OPTS_BASE.copy()
    with yt_dlp.YoutubeDL(opts) as ydl:
        if query.startswith("http"):
            info = ydl.extract_info(query, download=False)
        else:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if "entries" in info:
                info = info["entries"][0]
    return info

def best_thumbnail(info: dict) -> Optional[str]:
    thumbs = info.get("thumbnails") or []
    if thumbs:
        thumbs = sorted(thumbs, key=lambda t: t.get("height", 0), reverse=True)
        return thumbs[0].get("url")
    return info.get("thumbnail")
