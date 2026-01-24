# Feature Research

**Domain:** FastAPI scraping API for phpBB forum (MirCrew)
**Researched:** January 24, 2026
**Confidence:** MEDIUM

## Feature Landscape

### Table Stakes (Users Expect These)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Authenticated session login | Required to access full content and magnets | MEDIUM | Hidden token extraction + login POST + cookie reuse. |
| Search by title | Core use case | MEDIUM | Query params: q, page, per_page (API-level). |
| HTML parsing for results | Required for scraping | MEDIUM | Parse rows and extract links/titles/magnets. |
| Error handling & status codes | API reliability | LOW | Map common failures to HTTP errors. |
| Logging | Debug scraping/login failures | LOW | Log in controller/service/client. |

### Differentiators (Competitive Advantage)

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Quality filtering (1080p/720p) | Better results relevance | LOW | Filter `li.row` containing quality keywords. |
| Magnet availability check | Avoid dead results | MEDIUM | Navigate thumbs-up flow to unlock magnets. |
| Cookie reuse window | Fewer logins / stability | LOW | Cache cookies for 24h. |

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Aggressive scraping / parallel crawling | Faster results | Triggers anti-bot, instability | Respectful sequential fetching |
| Full-site indexing | "Search everything" | Large scope, slow, high risk | On-demand search by keyword |

## Feature Dependencies

```
Search results
    └──requires──> Authenticated session
                       └──requires──> Login tokens (creation_time, form_token)

Magnet extraction
    └──requires──> Visit thumbs-up link
                       └──requires──> Post detail navigation
```

### Dependency Notes

- **Search requires authenticated session:** magnets are only visible when logged in.
- **Magnet extraction requires thumbs-up navigation:** required to unlock magnet visibility.

## MVP Definition

### Launch With (v1)

- [ ] Authenticated login flow (tokens + POST + cookie reuse)
- [ ] GET /api/search (q, page, per_page) returning SearchResponse
- [ ] HTML parsing for results and magnet extraction
- [ ] Error handling + logging

### Add After Validation (v1.x)

- [ ] Result caching (optional) — if performance becomes a bottleneck
- [ ] Result ranking tweaks — if quality filter not sufficient

### Future Consideration (v2+)

- [ ] Additional endpoints (details, seasons, etc.) — after core search is stable

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Login flow | HIGH | MEDIUM | P1 |
| Search endpoint | HIGH | MEDIUM | P1 |
| Magnet extraction | HIGH | MEDIUM | P1 |
| Logging + error codes | MEDIUM | LOW | P1 |
| Quality filter | MEDIUM | LOW | P2 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

## Competitor Feature Analysis

| Feature | Competitor A | Competitor B | Our Approach |
|---------|--------------|--------------|--------------|
| Search + magnet extraction | N/A (site-specific) | N/A | Focused MirCrew scraping workflow |

## Sources

- Internal domain knowledge from project constraints

---
*Feature research for: FastAPI scraping API for phpBB forum (MirCrew)*
*Researched: January 24, 2026*
