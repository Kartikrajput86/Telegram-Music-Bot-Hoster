from collections import deque
from dataclasses import dataclass

@dataclass
class QueueItem:
    chat_id: int
    requested_by: int
    query: str
    is_video: bool
    info: dict | None = None
    filepath: str | None = None

class MusicQueue:
    def __init__(self):
        self.queues: dict[int, deque[QueueItem]] = {}
        self.loop_flags: dict[int, bool] = {}

    def get(self, chat_id: int) -> deque[QueueItem]:
        return self.queues.setdefault(chat_id, deque())

    def toggle_loop(self, chat_id: int) -> bool:
        val = not self.loop_flags.get(chat_id, False)
        self.loop_flags[chat_id] = val
        return val

    def is_looping(self, chat_id: int) -> bool:
        return self.loop_flags.get(chat_id, False)
