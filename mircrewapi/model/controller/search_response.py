from pydantic import BaseModel, Field

from mircrewapi.model.controller.search_item import SearchItem


class SearchResponse(BaseModel):
    query: str = Field(..., description="Search query")
    results: list[SearchItem] = Field(default_factory=list)
