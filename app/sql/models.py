from typing import List
from sqlalchemy import JSON, Column, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from uuid import uuid4, UUID

from .database import Base


class Image(Base):
    __tablename__ = "images"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    artwork_id: Mapped[int] = mapped_column()

    path: Mapped[str] = mapped_column()
    processed: Mapped[List["ProcessedImage"]] = relationship(
        "ProcessedImage", back_populates="source")


class ProcessedImage(Base):
    __tablename__ = "processed_images"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    path: Mapped[str] = mapped_column()
    source: Mapped["Image"] = relationship("Image", back_populates="processed")
    source_id: Mapped[UUID] = mapped_column(ForeignKey("images.id"))
    filter_type: Mapped[str] = mapped_column()
    settings = Column(JSON)
