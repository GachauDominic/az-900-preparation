"""Tiny in-memory sliding-window rate limiter (per process)."""
import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, per_minute: int, window: float = 60.0):
        self.per_minute = per_minute
        self.window = window
        self._hits: dict[str, deque] = defaultdict(deque)

    def allow(self, key: str, now: float | None = None) -> bool:
        if self.per_minute <= 0:
            return True
        now = time.monotonic() if now is None else now
        hits = self._hits[key]
        while hits and now - hits[0] > self.window:
            hits.popleft()
        if len(hits) >= self.per_minute:
            return False
        hits.append(now)
        return True
