from fastapi import APIRouter
from injector import inject

from mircrewapi.service.example_service import ExampleService


class ExampleController:
    """Expose a simple router that returns an example payload."""

    @inject
    def __init__(self, example_service: ExampleService):
        self.example_service = example_service
        self.router = APIRouter(prefix="/examples", tags=["Examples"])
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(
            "",
            self.get_example,
            methods=["GET"],
            summary="Return a sample payload",
        )

    async def get_example(self) -> dict:
        return self.example_service.get_example()
