from pydantic import BaseModel


class PostResult(BaseModel):
    id: str
    title: str
    url: str
