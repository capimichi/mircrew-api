from pathlib import Path

from mircrewapi.client.mircrew_client import MircrewClient


def test_is_logged_in_html_true():
    html = Path("tests/fixtures/index_logged_in.html").read_text()
    assert MircrewClient._is_logged_in_html(html) is True


def test_is_logged_in_html_false():
    html = Path("tests/fixtures/index_logged_out.html").read_text()
    assert MircrewClient._is_logged_in_html(html) is False
