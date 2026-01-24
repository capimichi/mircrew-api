# Roadmap

## Overview

**Project:** MirCrew API
**Goal:** Deliver an authenticated scraping API that returns MirCrew magnet links via `GET /api/search`.

**Phases:** 8
**All v1 requirements mapped:** Yes

---

## Phase 1 — Credentials Injection (DI)
**Goal:** Provide MirCrew credentials to the client via container config.
**Requirements:** AUTH-02

**Success Criteria:**
1. Container reads username/password from env configuration.
2. MirCrewClient receives credentials via constructor injection.
3. No credentials are hard-coded in codebase.

---

## Phase 2 — Login Token Flow
**Goal:** Implement the token-based login request sequence.
**Requirements:** AUTH-01

**Success Criteria:**
1. Client fetches `creation_time` and `form_token` from login/index page.
2. Client submits login POST with `autologin=on` and tokens.
3. Login response includes session cookies captured by the client.

---

## Phase 3 — Cookie Cache & Re-Auth
**Goal:** Reuse cookies for 24h and re-login when expired or invalid.
**Requirements:** AUTH-03, AUTH-04

**Success Criteria:**
1. Client stores cookies with timestamp after login.
2. Client skips login if cookies are still valid (<24h).
3. Client forces login when cookie cache is expired or invalid.

---

## Phase 4 — Search List & Filtering
**Goal:** Perform MirCrew title-only search and select result links.
**Requirements:** SEARCH-02, SEARCH-03

**Success Criteria:**
1. Client calls `search.php?keywords={q}&sf=titleonly&sr=topics`.
2. Results page is parsed for `li.row` containing quality keywords (1080p/720p/etc.).
3. Client extracts normalized `a.row-item-link` URLs.

---

## Phase 5 — Post Navigation & Unlock
**Goal:** Navigate result pages and trigger thumbs-up unlock when present.
**Requirements:** MAGNET-01, MAGNET-02

**Success Criteria:**
1. Client opens each post URL and locates first `.post` block.
2. Client finds `a` containing `i.fa-thumbs-o-up` when present.
3. Client navigates the thumbs-up link to unlock magnets.

---

## Phase 6 — Magnet Extraction
**Goal:** Reload post and extract magnet results.
**Requirements:** MAGNET-03, MAGNET-04

**Success Criteria:**
1. Client reloads the original post after thumbs-up navigation.
2. Client extracts all `dd a[href*="magnet"]` links.
3. Each result includes `title` from the first `p` in `dd` (trimmed) and `url` as magnet.

---

## Phase 7 — API Endpoint & Response Mapping
**Goal:** Expose `GET /api/search` with controller models and mappings.
**Requirements:** SEARCH-01

**Success Criteria:**
1. Controller accepts `q`, `page`, `per_page` query params.
2. Service orchestrates client calls and returns service models.
3. Controller maps service models to controller response model.

---

## Phase 8 — Logging & Error Mapping
**Goal:** Provide operational logging and appropriate HTTP errors.
**Requirements:** OBS-01, OBS-02

**Success Criteria:**
1. Logger is injected and used for client/service/controller failures.
2. Controller returns appropriate HTTP status codes for known failures.
3. Errors are logged with enough context to debug scraping/login issues.

---

## Requirement Coverage

All v1 requirements are mapped to exactly one phase.
