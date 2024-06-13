from typing import Union
from pydantic import BaseModel
from uuid import UUID


class ProcessedImage(BaseModel):
    path: str
    source_id: UUID
    filter_type: str
    settings: dict

    class Config:
        from_attributes = True


class ImageBase(BaseModel):
    id: UUID
    artwork_id: int


class Image(ImageBase):
    path: str
    processed: Union[list[ProcessedImage], None]

    class Config:
        from_attributes = True
