from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
import sys
import requests
from bson.objectid import ObjectId

sys.path.append("./util")
from util.etc import *

router = APIRouter(prefix="/polls")


@router.post("/create")
async def createPoll(username: str, token: str, postID: str, polloptions: str):
    if verify(username, token):
        userID = requests.get(f"https://api.wasteof.money/users/{username}").json()[
            "id"
        ]
        post = requests.get(f"https://api.wasteof.money/posts/{postID}")
        if post.status_code == 200 and post["poster"]["id"] == userID:
            options = polloptions.split(",")
            votes = {option: [] for option in options}
            poll = pollscoll.insert_one(
                {
                    "postID": postID,
                    "user": userID,
                    "options": options,
                    "votes": votes,
                }
            )

            return {"ok": "poll created", "_id": str(poll.inserted_id)}
        else:
            if not post["poster"]["id"] == userID:
                return JSONResponse(
                    {"error": "poll with post ID already created"}, status_code=409
                )
            else:
                return JSONResponse({"error": "post not found"}, status_code=404)
    else:
        return JSONResponse({"error": "not authorized"}, status_code=401)


@router.get("/get/{pollID}")
async def getPoll(pollID: str):
    poll = pollscoll.find_one({"_id": ObjectId(pollID)})

    if poll is not None:
        poll["_id"] = str(poll["_id"])
        return poll
    else:
        return JSONResponse({"error": "poll not found"}, status_code=404)


@router.get("/get/post/{postID}")
async def getPoll(postID: str):
    poll = pollscoll.find_one({"postID": postID})

    if poll is not None:
        poll["_id"] = str(poll["_id"])
        return poll
    else:
        return JSONResponse({"error": "poll not found"}, status_code=404)


@router.put("/vote/{pollID}")
async def vote(token: str, username: str, pollOption: str, pollID: str):
    if verify(username, token):
        poll = pollscoll.find_one({"_id": ObjectId(pollID)})
        if poll:
            userID = requests.get(f"https://api.wasteof.money/users/{username}").json()[
                "id"
            ]
            if (
                pollOption in poll["options"]
                and userID not in poll["votes"][pollOption]
            ):
                pollscoll.update_one(
                    {"_id": ObjectId(pollID)},
                    {"$push": {f"votes.{pollOption}": userID}},
                )

                return {"ok": "voted"}
            else:
                if userID in poll["votes"][pollOption]:
                    return JSONResponse({"error": "already voted"}, status_code=409)
                else:
                    return JSONResponse({"error": "option not found"}, status_code=404)
        else:
            return JSONResponse({"error": "poll not found"}, status_code=404)
