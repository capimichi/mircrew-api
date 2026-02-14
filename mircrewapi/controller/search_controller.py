from fastapi import APIRouter
from injector import inject

from mircrewapi.mapper.controller.search_mapper import SearchMapper
from mircrewapi.model.controller.search_response import SearchResponse
from mircrewapi.service.search_service import SearchService


class SearchController:
    """Expose search endpoints."""

    @inject
    def __init__(self, search_service: SearchService, search_mapper: SearchMapper):
        self.search_service = search_service
        self.search_mapper = search_mapper
        self.router = APIRouter(prefix="/search", tags=["Search"])
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(
            "",
            self.search,
            methods=["GET"],
            summary="Search Mircrew",
            response_model=SearchResponse,
        )

    async def search(self, q: str) -> SearchResponse:
        items = self.search_service.search(q)
        return self.search_mapper.to_response(query=q, items=items)
