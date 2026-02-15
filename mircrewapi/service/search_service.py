from injector import inject

from mircrewapi.client.mircrew_client import MircrewClient
from mircrewapi.mapper.service.magnet_mapper import MagnetMapper
from mircrewapi.mapper.service.post_mapper import PostMapper
from mircrewapi.model.service.magnet_item import MagnetItem
from mircrewapi.model.service.post_item import PostItem


class SearchService:
    """Service layer for search operations."""

    @inject
    def __init__(
        self,
        mircrew_client: MircrewClient,
        post_mapper: PostMapper,
        magnet_mapper: MagnetMapper,
    ):
        self.mircrew_client = mircrew_client
        self.post_mapper = post_mapper
        self.magnet_mapper = magnet_mapper

    def search_posts(self, query: str) -> list[PostItem]:
        items = self.mircrew_client.search_posts(query)
        return self.post_mapper.to_domain(items)

    def get_magnets(self, post_id: str) -> list[MagnetItem]:
        items = self.mircrew_client.get_magnets(post_id)
        return self.magnet_mapper.to_domain(items)
