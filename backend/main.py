"""FastAPI application entry point."""

from fastapi import FastAPI

from api.checklist import router as checklist_router


app = FastAPI()
app.include_router(checklist_router)
