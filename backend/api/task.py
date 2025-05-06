"""API for task management."""

import math
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlmodel import select

from db.engine import DatabaseSession, get_session
from models import NotFoundError, Pagination
from models.task import Fields, PaginatedTasks, Task


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(get_session)],
)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
async def post_task(
    session: DatabaseSession,
    fields: Fields = Body(description="Fields used to create the task"),
) -> Task:
    """Create a new task."""
    task = Task(**fields.model_dump())

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def get_task(
    session: DatabaseSession,
    page: int = Query(default=1, description="Page to return"),
    rows: int = Query(default=10, description="Rows per page", ge=1, le=100),
) -> PaginatedTasks:
    """Get task as per the pagination."""
    max_pages = math.ceil(len(session.exec(select(Task)).all()) / rows)

    skip = (page - 1) * rows
    tasks = session.exec(select(Task).offset(skip).limit(rows)).all()

    return PaginatedTasks(
        pagination=Pagination(
            page=page,
            rows=rows,
            max_pages=max_pages,
        ),
        tasks=tasks,
    )


@router.patch(
    path="/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "model": NotFoundError,
        }
    },
)
async def patch_task(
    session: DatabaseSession,
    tid: int = Query(description="ID of the task to be updated."),
    fields: Fields = Body(description="Fields to be updated"),
) -> Task:
    """Idempotently update the selected task with the given fields."""
    if not (task := session.get(Task, tid)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id={tid} not found",
        )

    if fields.title is not None:
        task.title = fields.title

    if fields.description is not None:
        task.description = fields.description

    if fields.checklist_id is not None:
        task.checklist_id = fields.checklist_id

    session.commit()
    session.refresh(task)

    return task


@router.delete(path="/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    session: DatabaseSession,
    tid: int = Query(description="ID of the task to be deleted."),
) -> None:
    """Deletes the selected task."""
    if task := session.get(Task, tid):
        session.delete(task)
        session.commit()
