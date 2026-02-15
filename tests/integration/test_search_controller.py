import asyncio

from mircrewapi.client.mircrew_client import MircrewClient
from mircrewapi.controller.search_controller import SearchController
from mircrewapi.mapper.controller.magnet_mapper import MagnetMapper
from mircrewapi.mapper.controller.post_mapper import PostMapper
from mircrewapi.mapper.service.magnet_mapper import MagnetMapper as ServiceMagnetMapper
from mircrewapi.mapper.service.post_mapper import PostMapper as ServicePostMapper
from mircrewapi.model.client.post_result import PostResult
from mircrewapi.model.client.search_result import SearchResult
from mircrewapi.service.search_service import SearchService


class FakeMircrewClient(MircrewClient):
    def __init__(self):
        super().__init__(username="user", password="pass")

    def search_posts(self, query: str):
        return [PostResult(id="456", title="Title 1080p", url="https://example.com/viewtopic.php?t=456")]

    def get_magnets(self, post_id: str):
        return [SearchResult(title="Magnet", url="magnet:?xt=urn:btih:456")]


def test_search_controller_posts_response():
    service = SearchService(FakeMircrewClient(), ServicePostMapper(), ServiceMagnetMapper())
    controller = SearchController(service, PostMapper(), MagnetMapper())

    response = asyncio.run(controller.search_posts("query"))

    assert response.query == "query"
    assert len(response.results) == 1
    assert response.results[0].title == "Title 1080p"
    assert response.results[0].id == "456"


def test_search_controller_magnets_response():
    service = SearchService(FakeMircrewClient(), ServicePostMapper(), ServiceMagnetMapper())
    controller = SearchController(service, PostMapper(), MagnetMapper())

    response = asyncio.run(controller.get_magnets("456"))

    assert response.post_id == "456"
    assert response.post_url.endswith("t=456")
    assert len(response.results) == 1
    assert response.results[0].url.startswith("magnet:")
