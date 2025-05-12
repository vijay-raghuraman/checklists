"""FastAPI application entry point."""

from fastapi import FastAPI

from api import checklist_router, task_router
from engine import create_db_and_tables


create_db_and_tables()

app = FastAPI()
app.include_router(checklist_router)
app.include_router(task_router)
