# Pitfalls Research

**Domain:** FastAPI scraping API for phpBB forum (MirCrew)
**Researched:** January 24, 2026
**Confidence:** MEDIUM

## Critical Pitfalls

### Pitfall 1: Login tokens missing or stale

**What goes wrong:** Login POST fails because `creation_time`/`form_token` not collected fresh.
**Why it happens:** Tokens are page-specific and expire; caching or skipping the GET.
**How to avoid:** Always GET the index/login page, parse hidden inputs, then POST immediately.
**Warning signs:** Repeated login failures or missing cookies.
**Phase to address:** Phase 1 (client login flow)

---

### Pitfall 2: Cookies not persisted or mixed

**What goes wrong:** Search returns partial content or magnets missing.
**Why it happens:** Cookies from login response are not aggregated correctly or expire.
**How to avoid:** Store full cookie jar string + timestamp; refresh after 24h.
**Warning signs:** Search works intermittently; magnet links missing.
**Phase to address:** Phase 1-2

---

### Pitfall 3: HTML selectors break

**What goes wrong:** Parsing fails after site HTML changes (class names, structure).
**Why it happens:** Hard-coded CSS selectors without fallback.
**How to avoid:** Centralize selectors in client mapper + add minimal defensive checks.
**Warning signs:** Empty result sets or missing magnets after site changes.
**Phase to address:** Phase 2 (parsing/mappers)

---

### Pitfall 4: Missing thumbs-up navigation

**What goes wrong:** Magnet links not visible on post page.
**Why it happens:** Required thumbs-up link was not visited to unlock magnets.
**How to avoid:** Always check `.post` for `a` containing `i.fa-thumbs-o-up`, navigate if present.
**Warning signs:** No magnet hrefs found in `dd` elements.
**Phase to address:** Phase 2

---

### Pitfall 5: Relative URLs mishandled

**What goes wrong:** Navigations fail for `./` or relative links.
**Why it happens:** Missing URL normalization.
**How to avoid:** Normalize hrefs to absolute URLs before requests.
**Warning signs:** 404/redirect loops in client logs.
**Phase to address:** Phase 2

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Parsing in controller | Faster initial build | Unmaintainable coupling | Never |
| Reusing models across layers | Less code | Tight coupling, refactor pain | Never |
| No test coverage for mappers | Faster build | Breaks silently on HTML change | Only in spike |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| MirCrew login | Skip hidden token fetch | Always fetch `creation_time`/`form_token` |
| MirCrew search | Assume magnets visible | Visit thumbs-up link, then reload |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Re-login on every request | Slow API | Cache cookies for 24h | Immediately noticeable |
| Fetching full pages twice unnecessarily | Latency spikes | Only reload when thumbs-up flow needed | At moderate usage |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Logging credentials | Credential leakage | Mask secrets in logs |
| Storing creds in code | Hard-coded secrets | Use env vars + DI config |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Silent empty results | Confusing responses | Return clear empty array + status 200 |
| Generic 500 errors | Hard to debug | Map known failures to 4xx/5xx with logs |

## "Looks Done But Isn't" Checklist

- [ ] **Login:** Cookies stored and reused across requests
- [ ] **Search:** Quality filter applied before selecting links
- [ ] **Magnets:** Thumbs-up navigation executed when present
- [ ] **Parsing:** Relative URLs normalized to absolute

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Token parsing fails | LOW | Re-fetch login page, update selectors |
| Selectors break | MEDIUM | Update mapper selectors, add tests |
| Cookie mismatch | LOW | Force re-login and refresh cookies |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Login tokens missing | Phase 1 | Login returns cookies consistently |
| Cookie persistence | Phase 1-2 | Search returns magnets after reuse |
| Selector breakage | Phase 2 | Parsing tests pass with fixture HTML |
| Thumbs-up flow missing | Phase 2 | Magnets visible after flow |

## Sources

- Internal domain knowledge from project constraints

---
*Pitfalls research for: FastAPI scraping API for phpBB forum (MirCrew)*
*Researched: January 24, 2026*
