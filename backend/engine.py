"""SQLModel engine for the checklist app."""

from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from models import Checklist, Task


DB_URL = "sqlite:///./checklists.sqlite"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Method to get a session for the database.

    Yields:
        Generator[Session, None, None]: A session for the database.
    """

    with Session(engine) as session:
        yield session


DatabaseSession = Annotated[Session, Depends(get_session)]
