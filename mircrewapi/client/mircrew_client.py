from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import logging
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from camoufox.async_api import AsyncCamoufox

from mircrewapi.manager.cache_manager import CacheManager
from mircrewapi.model.client.post_result import PostResult
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
    _STATE_FILENAME = "mircrew_state.json"

    def __init__(self, username: str, password: str, cache_manager: CacheManager | None = None):
        self.username = username
        self.password = password
        self._cache_manager = cache_manager
        self._session = requests.Session()
        self._cookie: str | None = None
        self._cookie_time: datetime | None = None
        self._restore_cached_cookie()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._session.cookies.set("cookieconsent_status", "dismiss")

    def search_posts(self, query: str) -> list[PostResult]:
        self._ensure_login()

        search_html = self._perform_browser_search(query)
        soup = BeautifulSoup(search_html, "html.parser")
        results: list[PostResult] = []
        for row in soup.select("li.row"):
            link = row.select_one("a.topictitle")
            if not link or not link.get("href"):
                continue
            post_url = urljoin(self._BASE_URL, link["href"])
            post_id = self._extract_post_id(post_url)
            if not post_id:
                continue
            title = link.get_text(" ", strip=True)
            if not self._has_quality_keyword(title):
                continue
            results.append(PostResult(id=post_id, title=title, url=post_url))
        return results

    def get_magnets(self, post_id: str) -> list[SearchResult]:
        self._ensure_login()
        post_url = self._build_post_url(post_id)
        return self._extract_magnets(None, post_url)

    def build_post_url(self, post_id: str) -> str:
        return self._build_post_url(post_id)

    def _ensure_login(self) -> None:
        if self._cookie and self._cookie_time:
            if datetime.utcnow() - self._cookie_time < self._COOKIE_TTL:
                if self._is_logged_in():
                    return
        if not self.username or not self.password:
            raise ValueError("Missing MIRCREW_USERNAME or MIRCREW_PASSWORD")

        if self._restore_browser_state():
            if self._is_logged_in():
                return

        if not self._perform_browser_login():
            self._logger.warning("Login failed during headless flow.")
            raise RuntimeError("Login failed")
        # Headless flow already validated login and stored cookies.
        return

    def _perform_browser_login(self) -> bool:
        self._logger.info("Starting headless login via Camoufox.")
        screenshot_dir = self._ensure_screenshot_dir()

        async def _login() -> dict:
            async with AsyncCamoufox(headless=True) as browser:
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto(self._LOGIN_URL, wait_until="domcontentloaded")
                await page.screenshot(path=str(screenshot_dir / "login_page.png"), full_page=True)
                try:
                    await page.wait_for_selector("form#login", timeout=10000)
                except Exception:
                    html = await page.content()
                    self._logger.warning("Login form not found. Page length=%s", len(html))
                    await page.screenshot(path=str(screenshot_dir / "login_form_missing.png"), full_page=True)
                    await context.close()
                    await browser.close()
                    return {}

                await page.fill("form#login input[name='username']", self.username)
                await page.fill("form#login input[name='password']", self.password)
                await page.check("form#login input[name='autologin']")
                await page.check("form#login input[name='viewonline']")
                await page.click("form#login input[type='submit']")
                await page.wait_for_load_state("networkidle")
                await page.screenshot(path=str(screenshot_dir / "after_submit.png"), full_page=True)

                error_text = None
                error_el = page.locator("div.error")
                if await error_el.count() > 0:
                    try:
                        error_text = await error_el.first.text_content()
                    except Exception:
                        error_text = None
                if error_text:
                    self._logger.warning("Login error text: %s", error_text.strip())

                await page.goto(self._INDEX_URL, wait_until="domcontentloaded")
                await page.screenshot(path=str(screenshot_dir / "index_after_login.png"), full_page=True)
                logout_el = page.locator('a[href^="./ucp.php?mode=logout&sid="]')
                logged_in = await logout_el.count() > 0
                self._logger.info("Headless login check: %s", logged_in)

                storage = await context.storage_state(path=str(self._state_path()))
                await context.close()
                await browser.close()
                return {"storage": storage, "logged_in": logged_in}

        result = _run_async(_login())
        if not result or not isinstance(result, dict):
            return False
        storage_state = result.get("storage")
        if not storage_state:
            return False
        self._save_storage_state(storage_state)
        self._apply_storage_state(storage_state)
        self._cookie = self._cookie_from_session()
        self._cookie_time = datetime.utcnow()
        self._cache_cookie()
        return bool(result.get("logged_in"))

    def _perform_browser_search(self, query: str) -> str:
        self._logger.info("Starting headless search via Camoufox.")
        screenshot_dir = self._ensure_screenshot_dir()

        async def _search() -> str:
            async with AsyncCamoufox(headless=True) as browser:
                context = await browser.new_context(storage_state=str(self._state_path()))
                page = await context.new_page()
                await page.goto(self._INDEX_URL, wait_until="domcontentloaded")
                await page.screenshot(path=str(screenshot_dir / "search_page.png"), full_page=True)

                try:
                    await page.wait_for_selector("#keywords", timeout=10000)
                    await page.fill("#keywords", query)
                    await page.click(".button-search")
                    await page.wait_for_load_state("networkidle")
                except Exception:
                    html = await page.content()
                    await page.screenshot(path=str(screenshot_dir / "search_failed.png"), full_page=True)
                    await context.close()
                    await browser.close()
                    return html

                await page.screenshot(path=str(screenshot_dir / "search_results.png"), full_page=True)
                html = await page.content()
                await context.close()
                await browser.close()
                return html

        return _run_async(_search())

    def _extract_magnets(self, title: str | None, post_url: str) -> list[SearchResult]:
        screenshot_dir = self._ensure_screenshot_dir()

        async def _extract() -> list[SearchResult]:
            async with AsyncCamoufox(headless=True) as browser:
                context = await browser.new_context(storage_state=str(self._state_path()))
                page = await context.new_page()
                await page.goto(post_url, wait_until="domcontentloaded")
                await page.screenshot(path=str(screenshot_dir / "post_page.png"), full_page=True)

                thank_selector = (
                    ".post a:has(i.fa-thumbs-o-up),"
                    " .post a:has(i.fa-thumbs-up),"
                    " .post a:has(i.icon-thumbs-up)"
                )
                thank_button = page.locator(thank_selector)
                if await thank_button.count() > 0:
                    try:
                        if await thank_button.first.is_visible():
                            await thank_button.first.click(timeout=1000)
                            await page.wait_for_load_state("networkidle")
                            await page.screenshot(
                                path=str(screenshot_dir / "post_after_thanks.png"),
                                full_page=True,
                            )
                            await page.goto(post_url, wait_until="domcontentloaded")
                            await page.wait_for_load_state("networkidle")
                    except Exception as exc:
                        self._logger.warning("Unable to click thanks button: %s", exc)

                results: list[SearchResult] = []
                boxes = page.locator(".hidebox.unhide dd")
                count = await boxes.count()
                for idx in range(count):
                    box = boxes.nth(idx)
                    magnet_el = box.locator('a[href^="magnet:"]')
                    if await magnet_el.count() == 0:
                        continue
                    href = await magnet_el.first.get_attribute("href")
                    if not href:
                        continue
                    title_el = box.locator("p").first
                    item_title = None
                    if await title_el.count() > 0:
                        item_title = (await title_el.text_content()) or ""
                    item_title = (item_title or "").strip() or title or "Magnet"
                    results.append(SearchResult(title=item_title, url=href))

                await context.close()
                await browser.close()
                return results

        return _run_async(_extract())

    def _default_headers(self, referer: str | None = None) -> dict:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        }
        if referer:
            headers["referer"] = referer
        return headers

    def _parse_login_tokens(self, html: str) -> _LoginTokens:
        soup = BeautifulSoup(html, "html.parser")
        creation = soup.find("input", {"name": "creation_time"})
        form = soup.find("input", {"name": "form_token"})
        if not creation or not form:
            raise ValueError("Login tokens not found on index page")
        return _LoginTokens(creation_time=creation["value"], form_token=form["value"])

    def _is_logged_in(self) -> bool:
        response = self._session.get(
            self._INDEX_URL,
            headers=self._default_headers(referer=self._INDEX_URL),
            timeout=30,
        )
        if response.status_code == 403:
            self._logger.warning("Login check blocked (403). Treating as not logged in.")
            return False
        response.raise_for_status()
        return self._is_logged_in_html(response.text)

    @staticmethod
    def _is_logged_in_html(html: str) -> bool:
        soup = BeautifulSoup(html, "html.parser")
        return soup.select_one('a[href*="ucp.php?mode=logout"]') is not None

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
        for chunk in self._cookie.split(";"):
            chunk = chunk.strip()
            if not chunk or "=" not in chunk:
                continue
            key, value = chunk.split("=", 1)
            self._session.cookies.set(key, value)

    def _cache_cookie(self) -> None:
        if not self._cache_manager or not self._cookie:
            return
        self._cache_manager.set("mircrew_cookie", self._cookie, self._COOKIE_TTL)

    def _cookie_from_session(self) -> str:
        cookies = []
        for cookie in self._session.cookies:
            cookies.append(f"{cookie.name}={cookie.value}")
        return "; ".join(cookies)

    def _cookie_names_from_session(self) -> list[str]:
        return [cookie.name for cookie in self._session.cookies]

    def _extract_thankyou_url(self, soup: BeautifulSoup) -> str | None:
        link = soup.select_one("ul.post-buttons li:nth-last-child(1) a")
        if not link or not link.get("href"):
            return None
        return urljoin(self._BASE_URL, link["href"])

    def _has_quality_keyword(self, text: str) -> bool:
        lowered = text.lower()
        return any(keyword in lowered for keyword in self._QUALITY_KEYWORDS)

    def _extract_post_id(self, post_url: str) -> str | None:
        try:
            parsed = urlparse(post_url)
        except ValueError:
            return None
        query = parse_qs(parsed.query)
        ids = query.get("t")
        if not ids:
            return None
        return ids[0]

    def _build_post_url(self, post_id: str) -> str:
        return f"{self._BASE_URL}/viewtopic.php?t={post_id}"

    def _state_path(self) -> Path:
        if not self._cache_manager:
            return Path(self._STATE_FILENAME)
        return Path(self._cache_manager._cache_dir) / self._STATE_FILENAME

    def _ensure_screenshot_dir(self) -> Path:
        if self._cache_manager:
            base_dir = Path(self._cache_manager._cache_dir)
        else:
            base_dir = Path("var")
        screenshot_dir = base_dir / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        return screenshot_dir

    def _save_storage_state(self, storage_state: dict) -> None:
        path = self._state_path()
        path.write_text(json.dumps(storage_state))

    def _restore_browser_state(self) -> bool:
        path = self._state_path()
        if not path.exists():
            return False
        try:
            storage_state = json.loads(path.read_text())
        except Exception:
            return False
        self._apply_storage_state(storage_state)
        return True

    def _apply_storage_state(self, storage_state: dict) -> None:
        cookies = storage_state.get("cookies", []) if isinstance(storage_state, dict) else []
        for cookie in cookies:
            name = cookie.get("name")
            value = cookie.get("value")
            domain = cookie.get("domain")
            if not name or value is None:
                continue
            self._session.cookies.set(name, value, domain=domain)


import asyncio
from concurrent.futures import ThreadPoolExecutor


def _run_async(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    with ThreadPoolExecutor(max_workers=1) as executor:
        return executor.submit(lambda: asyncio.run(coro)).result()
