"""FastAPI application entry point."""

from fastapi import FastAPI

from api.checklist import router as checklist_router
from api.task import router as task_router
from db.engine import create_db_and_tables


create_db_and_tables()

app = FastAPI()
app.include_router(checklist_router)
app.include_router(task_router)
