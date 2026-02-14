from mircrewapi.model.controller.search_item import SearchItem as ControllerSearchItem
from mircrewapi.model.controller.search_response import SearchResponse
from mircrewapi.model.service.search_item import SearchItem


class SearchMapper:
    """Map domain search items into controller responses."""

    def to_response(self, query: str, items: list[SearchItem]) -> SearchResponse:
        controller_items = [
            ControllerSearchItem(title=item.title, url=item.url)
            for item in items
        ]
        return SearchResponse(query=query, results=controller_items)
