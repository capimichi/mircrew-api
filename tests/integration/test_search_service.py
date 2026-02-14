from mircrewapi.client.mircrew_client import MircrewClient
from mircrewapi.mapper.service.search_mapper import SearchMapper
from mircrewapi.model.client.search_result import SearchResult
from mircrewapi.service.search_service import SearchService


class FakeMircrewClient(MircrewClient):
    def __init__(self):
        super().__init__(username="user", password="pass")

    def search(self, query: str):
        return [SearchResult(title="Title", url="magnet:?xt=urn:btih:123")]


def test_search_service_maps_to_domain():
    service = SearchService(FakeMircrewClient(), SearchMapper())
    items = service.search("query")

    assert len(items) == 1
    assert items[0].title == "Title"
    assert items[0].url.startswith("magnet:")
