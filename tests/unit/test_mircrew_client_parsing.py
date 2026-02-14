from pathlib import Path

from mircrewapi.client.mircrew_client import MircrewClient


def test_parse_login_tokens():
    html = Path("tests/fixtures/index.html").read_text()
    client = MircrewClient(username="user", password="pass")
    tokens = client._parse_login_tokens(html)

    assert tokens.creation_time == "1769295919"
    assert tokens.form_token == "7886dd58bfce6c6b47c19e6a8c9ceb8c05dc923f"


def test_has_quality_keyword():
    client = MircrewClient(username="user", password="pass")
    assert client._has_quality_keyword("Some Movie 1080p") is True
    assert client._has_quality_keyword("Some Movie SD") is False


def test_merge_set_cookies():
    class DummyRawHeaders:
        def get_all(self, key):
            if key.lower() == "set-cookie":
                return [
                    "cookieconsent_status=dismiss; Path=/",
                    "phpbb3_12hgm_u=1; Path=/",
                ]
            return []

    class DummyRaw:
        headers = DummyRawHeaders()

    class DummyResponse:
        raw = DummyRaw()
        headers = {}

    client = MircrewClient(username="user", password="pass")
    cookie_header = client._merge_set_cookies(DummyResponse())

    assert "cookieconsent_status=dismiss" in cookie_header
    assert "phpbb3_12hgm_u=1" in cookie_header
