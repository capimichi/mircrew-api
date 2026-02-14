from injector import inject

from mircrewapi.client.mircrew_client import MircrewClient
from mircrewapi.mapper.service.search_mapper import SearchMapper
from mircrewapi.model.service.search_item import SearchItem


class SearchService:
    """Service layer for search operations."""

    @inject
    def __init__(self, mircrew_client: MircrewClient, search_mapper: SearchMapper):
        self.mircrew_client = mircrew_client
        self.search_mapper = search_mapper

    def search(self, query: str) -> list[SearchItem]:
        items = self.mircrew_client.search(query)
        return self.search_mapper.to_domain(items)
