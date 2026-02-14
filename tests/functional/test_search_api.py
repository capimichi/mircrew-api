import os

import pytest
from fastapi.testclient import TestClient

from mircrewapi import api


def _has_credentials() -> bool:
    return bool(os.getenv("MIRCREW_USERNAME") and os.getenv("MIRCREW_PASSWORD"))


def _has_results(payload: dict) -> bool:
    return bool(payload.get("results"))


@pytest.mark.functional
@pytest.mark.network
def test_search_api_real():
    if not _has_credentials():
        pytest.skip("Missing MIRCREW credentials for functional test")

    client = TestClient(api.app)
    response = client.get("/search", params={"q": "stranger"})

    assert response.status_code == 200
    payload = response.json()
    assert "query" in payload
    assert "results" in payload
    assert payload["query"] == "stranger"

    if not _has_results(payload):
        pytest.skip("No results returned for query 'stranger' (site may have changed)")

    for item in payload["results"]:
        assert "title" in item
        assert "url" in item
        assert item["url"].startswith("magnet:")
