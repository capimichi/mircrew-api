from pydantic import BaseModel, Field

from mircrewapi.model.controller.magnet_item import MagnetItem


class MagnetsResponse(BaseModel):
    post_id: str = Field(..., description="Post id")
    post_url: str = Field(..., description="Post url")
    results: list[MagnetItem] = Field(default_factory=list)
