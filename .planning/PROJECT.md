# MirCrew API

## What This Is

Una API in FastAPI per navigare MirCrew e fare ricerche sui titoli, esponendo un endpoint `GET /api/search` che restituisce magnet link. L'API usa un'architettura a layer (controller → service → client) con mapping esplicito tra modelli e scraping HTML sul sito MirCrew.

## Core Value

Permettere la ricerca su MirCrew e restituire magnet validi in modo affidabile.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] `GET /api/search` accetta `q`, `page`, `per_page` e restituisce una response Pydantic dedicata (es. `SearchResponse`).
- [ ] Login via scraping: recupero `creation_time` e `form_token` da `https://mircrew-releases.org/index.php`, poi POST a `ucp.php?mode=login` con `autologin=on`.
- [ ] Cookie handling: unificare i cookie di response e riutilizzarli fino a 24h (poi re-login).
- [ ] Search HTML: chiamata a `search.php?keywords={q}&sf=titleonly&sr=topics` (prima pagina).
- [ ] Parsing lista: prendere `li.row` che contengono keyword qualità (es. 1080p/720p), poi `a.row-item-link` e normalizzare href (es. `./`).
- [ ] Navigazione post: entra nel post, trova dentro il primo `.post` un `a` che contiene `i.fa-thumbs-o-up`; se presente, navigarlo per abilitare la visione dei magnet.
- [ ] Ricaricare il post originale e cercare `dd` con `a[href*="magnet"]`; creare result `{ title, url }` usando il primo `p` dentro `dd` come titolo (trim).
- [ ] Layering: controller thin, service per orchestrazione, client per HTTP/scraping; mappers per conversioni.
- [ ] Struttura modelli e mapper:
  - `models/controller`, `models/service`, `models/client/...` (Pydantic)
  - `mappers/controller`, `mappers/service`, `mappers/client`
- [ ] Config e DI: container con Injector, credenziali (user/pass) da env passate al MirCrewClient.
- [ ] Error handling: try/catch in controller con codici HTTP appropriati e logging tramite logger DI.

### Out of Scope

- Paginazione reale su MirCrew — per ora solo prima pagina.
- Altri endpoint oltre `GET /api/search` — fase successiva.
- Ricerca non basata su titolo (`sf=titleonly`) — non prevista in v1.

## Context

- Repo contiene un `python-boilerplate` come riferimento per struttura namespace; il namespace desiderato e' `mircrewapi`.
- Scraping HTML sul sito MirCrew con sessione autenticata; la login richiede campi hidden e gestione cookie.
- L'architettura richiede separazione netta tra controller/service/client e mapping dedicato tra modelli.

## Constraints

- **Tech stack**: FastAPI + Pydantic — richiesto per endpoint e modelli.
- **DI**: Injector con container dedicato — richiesto per configurazione e dipendenze (client, logger).
- **Scraping**: HTML parsing del sito MirCrew — nessuna API ufficiale disponibile.
- **Namespace**: `mircrewapi` — uniformare struttura progetto.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| FastAPI come framework API | Richiesto dal progetto | — Pending |
| Pydantic per tutti i modelli | Standard FastAPI e validazione forte | — Pending |
| Architettura a layer controller → service → client | Separazione responsabilita' e testabilita' | — Pending |
| Controller thin + mapper verso response | Controller deve solo orchestrare e mappare | — Pending |
| Injector per DI e container config | Richiesto; facilita env/config | — Pending |
| Scraping HTML MirCrew con login/cookie | Unico modo per ottenere risultati | — Pending |
| Cookie riutilizzati fino a 24h | Evita login frequenti | — Pending |

---
*Last updated: January 24, 2026 after initialization*
