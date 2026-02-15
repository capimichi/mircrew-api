from mircrewapi.model.controller.post_item import PostItem as ControllerPostItem
from mircrewapi.model.controller.post_search_response import PostSearchResponse
from mircrewapi.model.service.post_item import PostItem


class PostMapper:
    """Map domain posts into controller responses."""

    def to_response(self, query: str, items: list[PostItem]) -> PostSearchResponse:
        controller_items = [
            ControllerPostItem(id=item.id, title=item.title, url=item.url)
            for item in items
        ]
        return PostSearchResponse(query=query, results=controller_items)
