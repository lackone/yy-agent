from pydantic import BaseModel


class FileRes(BaseModel):
    original_name: str
    new_name: str
    size: int
    url: str
