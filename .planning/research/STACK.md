# Stack Research

**Domain:** FastAPI scraping API for phpBB forum (MirCrew)
**Researched:** January 24, 2026
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| FastAPI | 0.128.0 | API framework | Modern, async-capable, high-performance Python API framework with built-in validation via Pydantic. |
| Pydantic | 2.12.5 | Data models/validation | FastAPI standard for request/response models and validation. |
| Uvicorn | 0.40.0 | ASGI server | Lightweight, standard server for FastAPI deployments. |
| httpx | 0.28.1 | HTTP client | Async + sync HTTP client suitable for authenticated scraping and cookie handling. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| beautifulsoup4 | 4.14.3 | HTML parsing | Extracting elements from MirCrew HTML pages. |
| lxml | 6.0.2 | HTML parser backend | Faster/more robust parsing backend for BeautifulSoup. |
| injector | 0.24.0 | Dependency Injection | Container-based DI for client/config/logger. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| pytest | Testing | Unit tests for mappers/client parsing. |
| ruff | Linting/format | Fast linting and style consistency. |

## Installation

```bash
# Core
pip install fastapi pydantic uvicorn httpx

# Supporting
pip install beautifulsoup4 lxml injector

# Dev dependencies
pip install pytest ruff
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Uvicorn | Hypercorn / Daphne | When specific ASGI features or integrations are needed. |
| httpx | requests | When only synchronous HTTP is needed. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| BeautifulSoup 3 | Deprecated/obsolete | beautifulsoup4 |

## Stack Patterns by Variant

**If scraping becomes heavy/slow:**
- Use httpx AsyncClient with connection pooling
- Because it reduces per-request overhead and reuses connections

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| FastAPI 0.128.0 | Pydantic 2.12.5 | FastAPI uses Pydantic v2 models. |
| Uvicorn 0.40.0 | Python 3.10+ | Uvicorn requires modern Python runtime. |

## Sources

- https://pypi.org/project/fastapi/ — version and project metadata
- https://pypi.org/project/pydantic/ — version and project metadata
- https://pypi.org/project/uvicorn/ — version and ASGI server alternatives
- https://pypi.org/project/httpx/ — version and HTTP client capabilities
- https://pypi.org/project/beautifulsoup4/ — version and parsing scope
- https://pypi.org/project/lxml/ — version and parser backend
- https://pypi.org/project/injector/ — version and DI library
- https://pypi.org/project/beautifulsoup/ — deprecation of BeautifulSoup 3

---
*Stack research for: FastAPI scraping API for phpBB forum (MirCrew)*
*Researched: January 24, 2026*
