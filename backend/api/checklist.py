"""API for checklist management."""

import math
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlmodel import select

from db.engine import DatabaseSession, get_session
from models import NotFoundError, Pagination
from models.checklist import Checklist, PaginatedChecklists, Fields


router = APIRouter(
    prefix="/checklists",
    tags=["Checklists"],
    dependencies=[Depends(get_session)],
)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
async def post_checklist(
    session: DatabaseSession,
    fields: Fields = Body(description="Fields used to create the checklist"),
) -> Checklist:
    """Create a new checklist."""
    checklist = Checklist(**fields.model_dump())

    session.add(checklist)
    session.commit()
    session.refresh(checklist)

    return checklist


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def get_checklists(
    session: DatabaseSession,
    page: int = Query(default=1, description="Page to return"),
    rows: int = Query(default=10, description="Rows per page", ge=1, le=100),
) -> PaginatedChecklists:
    """Get checklists as per the pagination."""
    max_pages = math.ceil(len(session.exec(select(Checklist)).all()) / rows)

    skip = (page - 1) * rows
    checklists = session.exec(select(Checklist).offset(skip).limit(rows)).all()

    return PaginatedChecklists(
        pagination=Pagination(
            page=page,
            rows=rows,
            max_pages=max_pages,
        ),
        checklists=checklists,
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
async def patch_checklist(
    session: DatabaseSession,
    cid: int = Query(description="ID of the checklist to be updated."),
    fields: Fields = Body(description="Fields to be updated"),
) -> Checklist:
    """Idempotently update the selected checklist with the given fields."""
    if not (checklist := session.get(Checklist, cid)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Checklist with id={cid} not found",
        )

    if fields.title is not None:
        checklist.title = fields.title

    if fields.description is not None:
        checklist.description = fields.description

    session.commit()
    session.refresh(checklist)

    return checklist


@router.delete(path="/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_checklist(
    session: DatabaseSession,
    cid: int = Query(description="ID of the checklist to be deleted."),
) -> None:
    """Deletes the selected checklist."""
    if checklist := session.get(Checklist, cid):
        session.delete(checklist)
        session.commit()
