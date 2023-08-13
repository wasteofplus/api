from fastapi import APIRouter
import requests
import sys

sys.path.append("./util")
from util.etc import *

router = APIRouter(prefix="/auth")


@router.get("/verify", include_in_schema=False)
async def verifysession(username: str, token: str):
    return verify(username, token)
