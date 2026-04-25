from __future__ import annotations

import hashlib
import json
from typing import Any

import redis

from utils.config import settings


class CacheService:
    def __init__(self) -> None:
        self.client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

    @staticmethod
    def _key(prefix: str, payload: dict[str, Any]) -> str:
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        return f"cliniq:{prefix}:{digest}"

    def get_json(self, prefix: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        try:
            raw = self.client.get(self._key(prefix, payload))
            return json.loads(raw) if raw else None
        except Exception:
            return None

    def set_json(self, prefix: str, payload: dict[str, Any], value: dict[str, Any], ttl_seconds: int = 900) -> None:
        try:
            self.client.setex(self._key(prefix, payload), ttl_seconds, json.dumps(value))
        except Exception:
            return
