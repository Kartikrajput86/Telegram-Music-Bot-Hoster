import asyncio
import os
from pathlib import Path
from contextlib import suppress
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types.input_stream import AudioPiped, VideoPiped
from pytgcalls.types.input_stream.quality import HighQualityVideo, HighQualityAudio
import yt_dlp
from .queue import MusicQueue, QueueItem
from .metadata import yt_search_or_info
from .config import CFG
from .utils import logger

class VoicePlayer:
    def __init__(self, assistant_client: Client, config):
        self.assistant = assistant_client
        self.tgcalls = PyTgCalls(self.assistant)
        self.q = MusicQueue()
        self.cfg = config

    async def start(self):
        @self.tgcalls.on_stream_end()
        async def _(u: Update):
            if isinstance(u, StreamAudioEnded):
                chat_id = u.chat_id
                await self._play_next(chat_id)
        await self.tgcalls.start()

    async def enqueue(self, chat_id: int, requested_by: int, query: str, is_video: bool) -> QueueItem:
        info = yt_search_or_info(query)
        item = QueueItem(chat_id=chat_id, requested_by=requested_by, query=query, is_video=is_video, info=info)
        self.q.get(chat_id).append(item)
        if len(self.q.get(chat_id)) == 1:
            await self._start_playback(item)
        return item

    async def _start_playback(self, item: QueueItem):
        ydl_opts = {
            "format": "bestvideo+bestaudio/best" if item.is_video else "bestaudio/best",
            "quiet": True,
            "nocheckcertificate": True,
            "geo_bypass": True,
            "noplaylist": True,
            "outtmpl": str(Path("downloads")/"%(id)s.%(ext)s"),
        }
        if self.cfg.yt_cookies:
            ydl_opts["cookiefile"] = self.cfg.yt_cookies

        os.makedirs("downloads", exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(item.info["webpage_url"], download=True)
            filepath = ydl.prepare_filename(info)
            item.filepath = filepath

        if item.is_video:
            await self.tgcalls.join_group_call(
                item.chat_id,
                VideoPiped(item.filepath, HighQualityVideo(), HighQualityAudio()),
                stream_type=0,
            )
        else:
            await self.tgcalls.join_group_call(
                item.chat_id,
                AudioPiped(item.filepath, HighQualityAudio()),
                stream_type=0,
            )

    async def _play_next(self, chat_id: int):
        q = self.q.get(chat_id)
        if not q:
            with suppress(Exception):
                await self.tgcalls.leave_group_call(chat_id)
            return
        current = q[0]
        if self.q.is_looping(chat_id):
            await self._start_playback(current)
            return
        q.popleft()
        if q:
            await self._start_playback(q[0])
        else:
            with suppress(Exception):
                await self.tgcalls.leave_group_call(chat_id)

    async def skip(self, chat_id: int):
        await self._play_next(chat_id)

    async def stop(self, chat_id: int):
        self.q.get(chat_id).clear()
        with suppress(Exception):
            await self.tgcalls.leave_group_call(chat_id)

    async def pause(self, chat_id: int):
        await self.tgcalls.pause_stream(chat_id)

    async def resume(self, chat_id: int):
        await self.tgcalls.resume_stream(chat_id)

    async def shuffle(self, chat_id: int):
        q = self.q.get(chat_id)
        if len(q) > 1:
            first = q.popleft()
            import random
            random.shuffle(q)
            q.appendleft(first)

    def toggle_loop(self, chat_id: int) -> bool:
        return self.q.toggle_loop(chat_id)
