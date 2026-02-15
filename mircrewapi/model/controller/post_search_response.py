from pydantic import BaseModel, Field

from mircrewapi.model.controller.post_item import PostItem


class PostSearchResponse(BaseModel):
    query: str = Field(..., description="Search query")
    results: list[PostItem] = Field(default_factory=list)
