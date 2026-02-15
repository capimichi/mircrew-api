from mircrewapi.client.mircrew_client import MircrewClient
from mircrewapi.mapper.service.magnet_mapper import MagnetMapper
from mircrewapi.mapper.service.post_mapper import PostMapper
from mircrewapi.model.client.post_result import PostResult
from mircrewapi.model.client.search_result import SearchResult
from mircrewapi.service.search_service import SearchService


class FakeMircrewClient(MircrewClient):
    def __init__(self):
        super().__init__(username="user", password="pass")

    def search_posts(self, query: str):
        return [PostResult(id="123", title="Title 1080p", url="https://example.com/viewtopic.php?t=123")]

    def get_magnets(self, post_id: str):
        return [SearchResult(title="Magnet", url="magnet:?xt=urn:btih:123")]


def test_search_service_maps_posts_to_domain():
    service = SearchService(FakeMircrewClient(), PostMapper(), MagnetMapper())
    items = service.search_posts("query")

    assert len(items) == 1
    assert items[0].title == "Title 1080p"
    assert items[0].url.startswith("https://")


def test_search_service_maps_magnets_to_domain():
    service = SearchService(FakeMircrewClient(), PostMapper(), MagnetMapper())
    items = service.get_magnets("123")

    assert len(items) == 1
    assert items[0].title == "Magnet"
    assert items[0].url.startswith("magnet:")
