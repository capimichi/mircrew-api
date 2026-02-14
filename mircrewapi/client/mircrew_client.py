from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from mircrewapi.manager.cache_manager import CacheManager
from mircrewapi.model.client.search_result import SearchResult


@dataclass(frozen=True)
class _LoginTokens:
    creation_time: str
    form_token: str


class MircrewClient:
    """Client for Mircrew interactions."""

    _BASE_URL = "https://mircrew-releases.org"
    _INDEX_URL = f"{_BASE_URL}/index.php"
    _LOGIN_URL = f"{_BASE_URL}/ucp.php?mode=login"
    _SEARCH_URL = f"{_BASE_URL}/search.php"
    _COOKIE_TTL = timedelta(hours=12)
    _QUALITY_KEYWORDS = (
        "2160p",
        "1080p",
        "720p",
        "480p",
        "4k",
        "x265",
        "x264",
    )

    def __init__(self, username: str, password: str, cache_manager: CacheManager | None = None):
        self.username = username
        self.password = password
        self._cache_manager = cache_manager
        self._cookie: str | None = None
        self._cookie_time: datetime | None = None
        self._restore_cached_cookie()

    def search(self, query: str) -> list[SearchResult]:
        self._ensure_login()

        response = requests.get(
            self._SEARCH_URL,
            params={"keywords": query, "sf": "titleonly", "sr": "topics"},
            headers=self._default_headers(referer=self._INDEX_URL),
            timeout=30,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results: list[SearchResult] = []
        for row in soup.select("li.row"):
            if not self._has_quality_keyword(row.get_text(" ", strip=True)):
                continue
            link = row.select_one("a.row-item-link")
            if not link or not link.get("href"):
                continue
            post_url = urljoin(self._BASE_URL, link["href"])
            results.extend(self._extract_magnets(post_url))
        return results

    def _ensure_login(self) -> None:
        if self._cookie and self._cookie_time:
            if datetime.utcnow() - self._cookie_time < self._COOKIE_TTL:
                return
        if not self.username or not self.password:
            raise ValueError("Missing MIRCREW_USERNAME or MIRCREW_PASSWORD")

        index_response = requests.get(self._INDEX_URL, timeout=30)
        index_response.raise_for_status()
        tokens = self._parse_login_tokens(index_response.text)

        login_payload = {
            "username": self.username,
            "password": self.password,
            "autologin": "on",
            "login": "Login",
            "redirect": "./index.php?",
            "creation_time": tokens.creation_time,
            "form_token": tokens.form_token,
        }

        login_response = requests.post(
            self._LOGIN_URL,
            data=login_payload,
            headers=self._default_headers(referer=f"{self._INDEX_URL}?"),
            timeout=30,
        )
        login_response.raise_for_status()

        self._cookie = self._merge_set_cookies(login_response)
        self._cookie_time = datetime.utcnow()
        self._cache_cookie()

    def _extract_magnets(self, post_url: str) -> list[SearchResult]:
        response = requests.get(
            post_url,
            headers=self._default_headers(referer=self._INDEX_URL),
            timeout=30,
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if self._has_like_link(soup):
            like_url = self._extract_like_url(soup)
            if like_url:
                requests.get(
                    like_url,
                    headers=self._default_headers(referer=post_url),
                    timeout=30,
                )
                response = requests.get(
                    post_url,
                    headers=self._default_headers(referer=post_url),
                    timeout=30,
                )
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

        title = self._extract_title(soup)
        results: list[SearchResult] = []
        for dd in soup.select("dd"):
            if "magnet" not in dd.get_text(" ", strip=True).lower():
                continue
            link = dd.find("a", href=True)
            if not link:
                continue
            href = link["href"]
            if href.startswith("magnet:"):
                results.append(SearchResult(title=title, url=href))
        return results

    def _default_headers(self, referer: str | None = None) -> dict:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        if referer:
            headers["referer"] = referer
        if self._cookie:
            headers["Cookie"] = self._cookie
        return headers

    def _parse_login_tokens(self, html: str) -> _LoginTokens:
        soup = BeautifulSoup(html, "html.parser")
        creation = soup.find("input", {"name": "creation_time"})
        form = soup.find("input", {"name": "form_token"})
        if not creation or not form:
            raise ValueError("Login tokens not found on index page")
        return _LoginTokens(creation_time=creation["value"], form_token=form["value"])

    def _merge_set_cookies(self, response: requests.Response) -> str:
        set_cookies: Iterable[str] = ()
        if hasattr(response.raw, "headers") and hasattr(response.raw.headers, "get_all"):
            set_cookies = response.raw.headers.get_all("Set-Cookie") or ()
        elif "Set-Cookie" in response.headers:
            set_cookies = [response.headers["Set-Cookie"]]

        parsed: list[str] = []
        for cookie in set_cookies:
            value = cookie.split(";", 1)[0].strip()
            if value:
                parsed.append(value)
        return "; ".join(parsed)

    def _restore_cached_cookie(self) -> None:
        if not self._cache_manager:
            return
        item = self._cache_manager.get("mircrew_cookie")
        if not item:
            return
        self._cookie = item.value
        self._cookie_time = item.created_at

    def _cache_cookie(self) -> None:
        if not self._cache_manager or not self._cookie:
            return
        self._cache_manager.set("mircrew_cookie", self._cookie, self._COOKIE_TTL)


    def _has_quality_keyword(self, text: str) -> bool:
        lowered = text.lower()
        return any(keyword in lowered for keyword in self._QUALITY_KEYWORDS)

    def _has_like_link(self, soup: BeautifulSoup) -> bool:
        return self._extract_like_url(soup) is not None

    def _extract_like_url(self, soup: BeautifulSoup) -> str | None:
        post = soup.select_one(".post")
        if not post:
            return None
        for link in post.find_all("a", href=True):
            if link.find("i", class_="fa-thumbs-o-up"):
                return urljoin(self._BASE_URL, link["href"])
        return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        title_el = soup.select_one("p")
        if title_el:
            return title_el.get_text(" ", strip=True)
        return "Mircrew search result"
