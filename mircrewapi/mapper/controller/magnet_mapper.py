from mircrewapi.model.controller.magnet_item import MagnetItem as ControllerMagnetItem
from mircrewapi.model.controller.magnets_response import MagnetsResponse
from mircrewapi.model.service.magnet_item import MagnetItem


class MagnetMapper:
    """Map domain magnets into controller responses."""

    def to_response(
        self,
        post_id: str,
        post_url: str,
        items: list[MagnetItem],
    ) -> MagnetsResponse:
        controller_items = [
            ControllerMagnetItem(title=item.title, url=item.url) for item in items
        ]
        return MagnetsResponse(post_id=post_id, post_url=post_url, results=controller_items)
