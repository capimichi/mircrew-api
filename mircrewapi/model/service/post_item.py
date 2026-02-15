from pydantic import BaseModel


class PostItem(BaseModel):
    id: str
    title: str
    url: str
