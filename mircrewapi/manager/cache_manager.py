from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from mircrewapi.model.service.cache_item import CacheItem


class CacheManager:
    """Simple filesystem cache with TTL persistence."""

    def __init__(self, cache_dir: str):
        self._cache_dir = Path(cache_dir)
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str) -> Optional[CacheItem]:
        path = self._path_for(key)
        if not path.exists():
            return None
        try:
            item = CacheItem.model_validate_json(path.read_text())
        except Exception:
            return None
        if datetime.utcnow() >= item.expires_at:
            self.delete(key)
            return None
        return item

    def set(self, key: str, value: str, ttl: timedelta) -> CacheItem:
        now = datetime.utcnow()
        item = CacheItem(
            key=key,
            value=value,
            created_at=now,
            expires_at=now + ttl,
        )
        path = self._path_for(key)
        path.write_text(item.model_dump_json())
        return item

    def delete(self, key: str) -> None:
        path = self._path_for(key)
        if path.exists():
            path.unlink()

    def _path_for(self, key: str) -> Path:
        safe_key = "".join(ch for ch in key if ch.isalnum() or ch in ("-", "_"))
        return self._cache_dir / f"{safe_key}.json"
