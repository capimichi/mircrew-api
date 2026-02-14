from datetime import datetime, timedelta

from mircrewapi.manager.cache_manager import CacheManager


def test_cache_manager_set_get(tmp_path, monkeypatch):
    fixed_now = datetime(2024, 1, 1, 12, 0, 0)

    class FixedDateTime(datetime):
        @classmethod
        def utcnow(cls):
            return fixed_now

    import mircrewapi.manager.cache_manager as cache_module

    monkeypatch.setattr(cache_module, "datetime", FixedDateTime)

    manager = CacheManager(cache_dir=str(tmp_path))
    item = manager.set("token", "value", ttl=timedelta(hours=1))

    assert item.key == "token"
    assert item.value == "value"

    cached = manager.get("token")
    assert cached is not None
    assert cached.value == "value"


def test_cache_manager_expired(tmp_path, monkeypatch):
    start = datetime(2024, 1, 1, 12, 0, 0)

    class FixedDateTime(datetime):
        @classmethod
        def utcnow(cls):
            return start

    import mircrewapi.manager.cache_manager as cache_module

    monkeypatch.setattr(cache_module, "datetime", FixedDateTime)

    manager = CacheManager(cache_dir=str(tmp_path))
    manager.set("token", "value", ttl=timedelta(minutes=1))

    class LaterDateTime(datetime):
        @classmethod
        def utcnow(cls):
            return start + timedelta(minutes=2)

    monkeypatch.setattr(cache_module, "datetime", LaterDateTime)

    assert manager.get("token") is None
