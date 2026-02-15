from mircrewapi.model.client.search_result import SearchResult
from mircrewapi.model.service.magnet_item import MagnetItem


class MagnetMapper:
    """Map client magnet results into domain models."""

    def to_domain(self, items: list[SearchResult]) -> list[MagnetItem]:
        return [MagnetItem(title=item.title, url=item.url) for item in items]
