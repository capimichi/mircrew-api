from mircrewapi.model.client.post_result import PostResult
from mircrewapi.model.service.post_item import PostItem


class PostMapper:
    """Map client post results into domain models."""

    def to_domain(self, items: list[PostResult]) -> list[PostItem]:
        return [PostItem(id=item.id, title=item.title, url=item.url) for item in items]
