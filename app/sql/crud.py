from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import String
import json

from . import models, schemas


def create_image(db: Session, image: schemas.Image):
    db_image = models.Image(**dict(image))
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def create_processed_image(
        db: Session,
        processed_image: schemas.ProcessedImage,
):
    db_image = models.ProcessedImage(**dict(processed_image))
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_image(db: Session, image_id: UUID):
    return db.query(models.Image) \
             .filter(models.Image.id == image_id).first()


def get_processed_image(db: Session, image_id: UUID):
    return db.query(models.ProcessedImage) \
             .filter(models.ProcessedImage.id == image_id).first()


def get_processed_image_by_source(db: Session, image_id: UUID):
    return db.query(models.ProcessedImage) \
             .filter(models.ProcessedImage.source_id == image_id).all()


def get_processed_image_pro(
        db: Session,
        image_id: UUID,
        filter_type: str,
        settings: dict,
):
    return db.query(models.ProcessedImage) \
             .filter(models.ProcessedImage.source_id == image_id.hex) \
             .filter(models.ProcessedImage.filter_type == filter_type) \
             .filter(models.ProcessedImage.settings.cast(String)
                     == json.dumps(settings)) \
             .first()
