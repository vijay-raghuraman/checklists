"""Common models for the application."""

from pydantic import BaseModel
from sqlmodel import Field


class AuditMixin(BaseModel):
    id: int = Field(index=True, primary_key=True)


class Pagination(BaseModel):
    page: int = Field(ge=1, default=1)
    rows: int = Field(ge=1, le=100, default=10)
    max_pages: int = Field(ge=0)


class NotFoundError(BaseModel):
    detail: str
