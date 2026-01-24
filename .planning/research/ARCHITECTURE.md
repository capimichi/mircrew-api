# Architecture Research

**Domain:** FastAPI scraping API for phpBB forum (MirCrew)
**Researched:** January 24, 2026
**Confidence:** MEDIUM

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                            │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │ Controllers  │  │ Controller Mappers│  │ Response Models│ │
│  └──────┬───────┘  └──────────┬───────┘  └────────┬───────┘ │
│         │                    │                   │         │
├─────────┴────────────────────┴───────────────────┴─────────┤
│                       Service Layer                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐   ┌────────────────┐   ┌──────────────────┐   │
│  │ Services │   │ Service Mappers│   │ Service Models   │   │
│  └────┬─────┘   └───────┬────────┘   └────────┬─────────┘   │
│       │                 │                    │             │
├───────┴─────────────────┴────────────────────┴─────────────┤
│                        Client Layer                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌────────────────┐  ┌────────────────┐  │
│  │ MirCrewClient│  │ Client Mappers │  │ Client Models  │  │
│  └──────────────┘  └────────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Controllers | HTTP layer, validation, error mapping | FastAPI routers/endpoints |
| Services | Orchestration, business flow | Pure Python services |
| Clients | HTTP scraping + login + cookies | httpx + HTML parsing |
| Mappers | Data transformations across layers | Dedicated mapper classes |
| Models | Pydantic models per layer | models/controller, models/service, models/client |
| Container | DI wiring + configuration | Injector container |

## Recommended Project Structure

```
mircrewapi/
├── api/                         # FastAPI app + routers
│   └── search_controller.py     # GET /api/search
├── clients/
│   └── mircrew/
│       └── mircrew_client.py    # login/search/scrape
├── services/
│   └── search_service.py
├── models/
│   ├── controller/
│   │   └── search_response.py
│   ├── service/
│   │   └── search_result.py
│   └── client/
│       └── mircrew/
│           └── search_page.py
├── mappers/
│   ├── controller/
│   │   └── search_response_mapper.py
│   ├── service/
│   │   └── search_result_mapper.py
│   └── client/
│       └── mircrew/
│           └── search_page_mapper.py
├── container/
│   └── default_container.py     # Injector wiring
└── config/
    └── mircrew_config.py        # env loading
```

### Structure Rationale

- **models/**: strict separation by layer to avoid leakage across boundaries.
- **mappers/**: clear transformations from HTML -> client models -> service models -> controller response.

## Architectural Patterns

### Pattern 1: Thin Controller

**What:** Controller only validates, invokes service, maps response.
**When to use:** Always, to keep HTTP concerns separated.
**Trade-offs:** Slightly more boilerplate, but clean responsibilities.

**Example:**
```python
# controller calls service and maps result
```

### Pattern 2: Client Session Cache

**What:** Client maintains cookie string + timestamp for 24h reuse.
**When to use:** Scraping with login tokens and cookie auth.
**Trade-offs:** Must handle expiration and invalid cookies.

### Pattern 3: Mapper-First Parsing

**What:** Client returns raw HTML parsed into client models, then mapped.
**When to use:** Scraping with complex HTML.
**Trade-offs:** Extra types and mapping code, but stability and testability.

## Data Flow

### Request Flow

```
Client request
    ↓
SearchController → SearchService → MirCrewClient
    ↓                    ↓              ↓
ResponseMapper  ← ServiceMapper  ← ClientMapper
```

### Key Data Flows

1. **Login flow:** GET login page → parse hidden tokens → POST login → store cookies.
2. **Search flow:** GET search page → parse rows → visit thumbs-up link → reload post → extract magnets.

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-1k users | Monolith API is fine |
| 1k-100k users | Add caching + rate limiting |
| 100k+ users | Separate scraper workers + queue |

## Anti-Patterns

### Anti-Pattern 1: Parsing in Controller

**What people do:** HTML parsing and scraping inside controller.
**Why it's wrong:** Couples HTTP layer with scraping logic.
**Do this instead:** Keep parsing in client + mapper layers.

### Anti-Pattern 2: Shared Models Across Layers

**What people do:** Reuse controller models in service/client.
**Why it's wrong:** Leaks concerns and makes refactors risky.
**Do this instead:** Dedicated models per layer + explicit mappers.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| MirCrew | HTTP scraping + cookies | Hidden form tokens + cookies required |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Controller ↔ Service | direct call | API DTO mapping |
| Service ↔ Client | direct call | Client returns client models |

## Sources

- Internal architecture conventions from project constraints

---
*Architecture research for: FastAPI scraping API for phpBB forum (MirCrew)*
*Researched: January 24, 2026*
