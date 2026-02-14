from mircrewapi.model.client.search_result import SearchResult as ClientSearchResult
from mircrewapi.model.service.search_item import SearchItem


class SearchMapper:
    """Map client search results into domain models."""

    def to_domain(self, items: list[ClientSearchResult]) -> list[SearchItem]:
        return [SearchItem(title=item.title, url=item.url) for item in items]
