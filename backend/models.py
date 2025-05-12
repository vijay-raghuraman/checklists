"""Common models for the application."""

from typing import Sequence
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class AuditMixin(BaseModel):
    id: int = Field(index=True, primary_key=True)


class Pagination(BaseModel):
    page: int = Field(ge=1, default=1)
    rows: int = Field(ge=1, le=100, default=10)
    max_pages: int = Field(ge=0)


class NotFoundError(BaseModel):
    detail: str


class Fields(SQLModel):
    title: str | None = Field(default=None, max_length=31)
    description: str | None = Field(default=None, max_length=255)


class Checklist(AuditMixin, Fields, table=True):
    pass


class PaginatedChecklists(BaseModel):
    pagination: Pagination
    checklists: Sequence[Checklist] = Field(default_factory=list)


class TaskFields(Fields):
    checklist_id: int = Field(foreign_key="checklist.id")


class Task(AuditMixin, TaskFields, table=True):
    pass


class PaginatedTasks(SQLModel):
    pagination: Pagination
    tasks: Sequence[Task] = Field(default_factory=list)
