from fastapi import APIRouter
from injector import inject

from mircrewapi.mapper.controller.magnet_mapper import MagnetMapper
from mircrewapi.mapper.controller.post_mapper import PostMapper
from mircrewapi.model.controller.magnets_response import MagnetsResponse
from mircrewapi.model.controller.post_search_response import PostSearchResponse
from mircrewapi.service.search_service import SearchService


class SearchController:
    """Expose search endpoints."""

    @inject
    def __init__(
        self,
        search_service: SearchService,
        post_mapper: PostMapper,
        magnet_mapper: MagnetMapper,
    ):
        self.search_service = search_service
        self.post_mapper = post_mapper
        self.magnet_mapper = magnet_mapper
        self.router = APIRouter(tags=["Search"])
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(
            "/search",
            self.search_posts,
            methods=["GET"],
            summary="Search Mircrew posts",
            response_model=PostSearchResponse,
        )
        self.router.add_api_route(
            "/post/{post_id}/magnets",
            self.get_magnets,
            methods=["GET"],
            summary="Get magnets for a post",
            response_model=MagnetsResponse,
        )

    async def search_posts(self, q: str) -> PostSearchResponse:
        items = self.search_service.search_posts(q)
        return self.post_mapper.to_response(query=q, items=items)

    async def get_magnets(self, post_id: str) -> MagnetsResponse:
        items = self.search_service.get_magnets(post_id)
        post_url = self.search_service.mircrew_client.build_post_url(post_id)
        return self.magnet_mapper.to_response(post_id=post_id, post_url=post_url, items=items)
