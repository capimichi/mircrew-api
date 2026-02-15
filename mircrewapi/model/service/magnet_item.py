from pydantic import BaseModel


class MagnetItem(BaseModel):
    title: str
    url: str
