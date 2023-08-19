from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
import sys
from cachetools import TTLCache

sys.path.append("./util")
from util.etc import *

router = APIRouter(prefix="/reactions")

allowedEmojis = [
    "red-heart",
    "smiling-face",
    "star",
    "thumbs-up",
    "thumbs-down",
    "partying-face",
    "sobbing",
    "eyes",
    "laughing",
    "thinking",
    "heart-eyes",
]


@router.post(
    "/react"
)  # this endpoint is pretty slow (taking a few second,) and if possible should be improved eventually
async def react(username: str, token: str, postID: str, emoji: str):
    global idCache
    if verify(username, token):
        post = requests.get(f"https://api.wasteof.money/posts/{postID}")
        if post.status_code == 200 and emoji in allowedEmojis:
            dbpost = reactionscoll.find_one({"postID": postID})
            if username in idCache:
                userID = idCache[username]
            else:
                userID = requests.get(
                    f"https://api.wasteof.money/users/{username}"
                ).json()["id"]
                idCache[username] = userID
            if dbpost:
                if userID in dbpost["reactions"]:
                    reactionscoll.update_one(
                        {"postID": postID},
                        {"$pull": {f"reactions.{emoji}": userID}},
                    )
                    return {"ok": "removed reaction"}
                else:
                    reactionscoll.update_one(
                        {"postID": postID},
                        {"$push": {f"reactions.{emoji}": userID}},
                    )
                    return {"ok": "added reaction"}
            else:
                reactionscoll.insert_one(
                    {"postID": postID, "reactions": {emoji: [userID]}}
                )
                return {"ok": "added reaction"}
        else:
            if not emoji in allowedEmojis:
                return JSONResponse({"error": "reaction not allowed"}, status_code=400)
            else:
                return JSONResponse({"error": "post not found"}, status_code=404)
    else:
        return JSONResponse({"error": "not authorized"}, status_code=401)


@router.get("/get/{postID}")
def getReactions(postID: str):
    post = reactionscoll.find_one({"postID": postID})
    if post:
        post["_id"] = str(post["_id"])
        return post
    else:
        return JSONResponse(
            {"error": "post not found, couldn't get reactions"}, status_code=404
        )
