# Requirements

## v1 Requirements

### Authentication & Session
- [ ] **AUTH-01**: System authenticates automatically by fetching login page tokens (`creation_time`, `form_token`) and submitting login POST with `autologin=on`.
- [ ] **AUTH-02**: System reads MirCrew credentials from env via container config and injects them into the MirCrewClient constructor.
- [ ] **AUTH-03**: System reuses authenticated cookies for up to 24 hours before re-login.
- [ ] **AUTH-04**: System re-authenticates automatically when cookie cache is expired or invalid.

### Search & Result List
- [ ] **SEARCH-01**: User can call `GET /api/search` with query params `q`, `page`, `per_page`.
- [ ] **SEARCH-02**: System performs title-only search on MirCrew and loads the first page of results.
- [ ] **SEARCH-03**: System filters result rows to those containing quality keywords (e.g., 1080p, 720p) before extracting `a.row-item-link`.

### Post Navigation & Magnet Extraction
- [ ] **MAGNET-01**: System navigates each result link and finds the first `.post` containing a thumbs-up action link (`i.fa-thumbs-o-up`).
- [ ] **MAGNET-02**: System follows the thumbs-up link (if present) to unlock magnet visibility.
- [ ] **MAGNET-03**: System reloads the original post and extracts magnet URLs from `dd a[href*="magnet"]`.
- [ ] **MAGNET-04**: System returns results with `title` from the first `p` inside `dd` (trimmed) and `url` as the magnet link.

### Observability & Errors
- [ ] **OBS-01**: System logs failures via DI-injected logger.
- [ ] **OBS-02**: Controller maps known failures to appropriate HTTP status codes.

## v2 Requirements (Deferred)

(None yet)

## Out of Scope

- Real pagination on MirCrew — only first page is used in v1.
- Additional endpoints beyond `GET /api/search` — later phases.
- Non-title search modes (`sf` other than `titleonly`).

## Traceability

| Requirement ID | Roadmap Phase |
|----------------|---------------|
| AUTH-01 | TBD |
| AUTH-02 | TBD |
| AUTH-03 | TBD |
| AUTH-04 | TBD |
| SEARCH-01 | TBD |
| SEARCH-02 | TBD |
| SEARCH-03 | TBD |
| MAGNET-01 | TBD |
| MAGNET-02 | TBD |
| MAGNET-03 | TBD |
| MAGNET-04 | TBD |
| OBS-01 | TBD |
| OBS-02 | TBD |
