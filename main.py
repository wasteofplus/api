from fastapi import APIRouter, FastAPI

from routers import auth, polls

app = FastAPI()
router = app.router

app.include_router(auth.router)
app.include_router(polls.router)
