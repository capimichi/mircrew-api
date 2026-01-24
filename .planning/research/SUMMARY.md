# Project Research Summary

**Project:** MirCrew API
**Domain:** FastAPI scraping API for phpBB forum (MirCrew)
**Researched:** January 24, 2026
**Confidence:** MEDIUM

## Executive Summary

Questo progetto e' una API FastAPI che fa scraping HTML autenticato su MirCrew per cercare titoli e restituire magnet. La soluzione standard usa FastAPI + Pydantic per modelli/validazione, httpx per le chiamate HTTP con cookie, e un parser HTML (BeautifulSoup + lxml). Il client deve gestire una login a token (hidden inputs) e persistere i cookie per evitare login frequenti.

I rischi principali sono la fragilita' dei selettori HTML e la gestione corretta del flusso "thumbs-up" necessario a rendere visibili i magnet. La mitigazione richiede mappers dedicati, test su HTML di esempio e logging mirato.

## Key Findings

### Recommended Stack

FastAPI + Pydantic + Uvicorn come base API, con httpx per HTTP scraping autenticato. Parsing HTML con BeautifulSoup usando lxml come parser, e Injector per DI.

**Core technologies:**
- FastAPI: API framework — moderno e compatibile con Pydantic
- Pydantic: modelli e validazione — standard FastAPI
- Uvicorn: ASGI server — default per FastAPI
- httpx: HTTP client — supporta cookie + sync/async

### Expected Features

**Must have (table stakes):**
- Login con token hidden + cookie persistence
- Search by title e parsing risultati
- Estrazione magnet con flusso thumbs-up

**Should have (competitive):**
- Filtri per qualita' (1080p/720p)
- Logging + error handling

**Defer (v2+):**
- Altri endpoint o indicizzazione estesa

### Architecture Approach

Architettura a layer (controller → service → client) con mappers e modelli separati per livello, contenitore DI con Injector e client dedicato al flusso di login/search/scraping.

**Major components:**
1. Controllers — HTTP layer + mapping response
2. Services — orchestrazione del flusso di ricerca
3. MirCrewClient — login, cookie, scraping HTML

### Critical Pitfalls

1. **Token login mancanti/stale** — sempre fetch della pagina iniziale prima del POST
2. **Cookie non persistiti** — unificare cookie + TTL 24h
3. **Selector HTML fragili** — mappers isolati + test
4. **Thumbs-up flow ignorato** — magnet non visibili senza navigazione

## Implications for Roadmap

### Phase 1: Foundation + Login
**Rationale:** l'accesso autenticato e' prerequisito per tutto.
**Delivers:** client MirCrew con login token + cookie cache.
**Addresses:** login + cookie handling.
**Avoids:** token/cookie pitfalls.

### Phase 2: Search + Parsing
**Rationale:** parsing e scraping stabilizzano la value chain.
**Delivers:** search workflow, parsing lista e magnet extraction.
**Uses:** httpx + BeautifulSoup/lxml.
**Implements:** client mapper + service mapper.

### Phase 3: API + Mappers + Errors
**Rationale:** esporre API stabile e formattata.
**Delivers:** controller thin, response models, error mapping.

### Phase Ordering Rationale

- Login deve esistere prima della ricerca.
- Parsing + magnet extraction richiede flusso completo nel client.
- API layer va per ultimo per stabilizzare il dominio.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2:** parsing HTML selettori, robustezza al cambiamento.

Phases with standard patterns (skip research-phase):
- **Phase 1:** login + cookie cache sono pattern noti.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Versioni verificate su PyPI |
| Features | MEDIUM | Basate su requisiti progetto |
| Architecture | MEDIUM | Derivata da vincoli architetturali |
| Pitfalls | MEDIUM | Esperienza su scraping HTML |

**Overall confidence:** MEDIUM

### Gaps to Address

- HTML selectors specifici vanno validati contro il sito reale.
- Definizione finale dei codici errore per casi di login/search.

## Sources

### Primary (HIGH confidence)
- https://pypi.org/project/fastapi/ — version and project metadata
- https://pypi.org/project/pydantic/ — version and project metadata
- https://pypi.org/project/uvicorn/ — version and ASGI server alternatives
- https://pypi.org/project/httpx/ — version and HTTP client capabilities
- https://pypi.org/project/beautifulsoup4/ — version and parsing scope
- https://pypi.org/project/lxml/ — version and parser backend
- https://pypi.org/project/injector/ — version and DI library
- https://pypi.org/project/beautifulsoup/ — deprecation of BeautifulSoup 3

---
*Research completed: January 24, 2026*
*Ready for roadmap: yes*
