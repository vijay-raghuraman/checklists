"""Definitions of the Checklist ORM model."""

from typing import Sequence
from pydantic import BaseModel
from sqlmodel import SQLModel, Field

from . import AuditMixin, Pagination


class Fields(SQLModel):
    title: str | None = Field(default=None, max_length=31)
    description: str | None = Field(default=None, max_length=255)


class Checklist(AuditMixin, Fields, table=True):
    pass


class PaginatedChecklists(BaseModel):
    pagination: Pagination
    checklists: Sequence[Checklist] = Field(default_factory=list)
