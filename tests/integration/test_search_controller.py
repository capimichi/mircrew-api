import asyncio

from mircrewapi.client.mircrew_client import MircrewClient
from mircrewapi.controller.search_controller import SearchController
from mircrewapi.mapper.controller.search_mapper import SearchMapper
from mircrewapi.mapper.service.search_mapper import SearchMapper as ServiceSearchMapper
from mircrewapi.model.client.search_result import SearchResult
from mircrewapi.service.search_service import SearchService


class FakeMircrewClient(MircrewClient):
    def __init__(self):
        super().__init__(username="user", password="pass")

    def search(self, query: str):
        return [SearchResult(title="Title", url="magnet:?xt=urn:btih:456")]


def test_search_controller_response():
    service = SearchService(FakeMircrewClient(), ServiceSearchMapper())
    controller = SearchController(service, SearchMapper())

    response = asyncio.run(controller.search("query"))

    assert response.query == "query"
    assert len(response.results) == 1
    assert response.results[0].title == "Title"
