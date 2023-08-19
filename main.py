from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
import time

from routers import auth, polls, reactions

app = FastAPI()
router = app.router

app.include_router(auth.router)
app.include_router(polls.router)
app.include_router(reactions.router)

startTime = time.time()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(500)
async def error_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        {
            "error": "an unknown server error occured. please report this to @radi8 on wasteof.money or via email at me@radi8.dev"
        }
    )


@app.get("/")
def root():
    return {
        "ok": "ok",
        "version": "no version for now, pre v1", # will figure out later
        "uptime": time.time() - startTime,
        "docs": "/docs",
    }


@app.get("/gen500", include_in_schema=False)
async def gen500():
    raise HTTPException(status_code=500)
