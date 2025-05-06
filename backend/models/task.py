"""ORM model for tasks."""

from typing import Sequence
from sqlmodel import SQLModel, Field

from . import AuditMixin, Pagination


class Fields(SQLModel):
    title: str | None = Field(default=None, max_length=31)
    description: str | None = Field(default=None, max_length=255)
    checklist_id: int | None = Field(default=None, foreign_key="checklist.id")


class Task(AuditMixin, Fields, table=True):
    pass


class PaginatedTasks(SQLModel):
    pagination: Pagination
    tasks: Sequence[Task] = Field(default_factory=list)
