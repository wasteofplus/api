from fastapi import APIRouter, Header
import sys
import requests
from bson.objectid import ObjectId

sys.path.append("./util")
from util.etc import *

router = APIRouter(prefix="/polls")


@router.post("/create")
async def createPoll(username: str, token: str, postID: str, polloptions: str):
    if verify(username, token):
        if requests.get(f"https://api.wasteof.money/posts/{postID}").status_code == 200:
            userID = requests.get(f"https://api.wasteof.money/users/{username}").json()[
                "id"
            ]
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
            return {"error": "post not found"}
    else:
        return {"error": "not authorized"}


@router.get("/get/{pollID}")
async def getPoll(pollID: str):
    poll = pollscoll.find_one({"_id": ObjectId(pollID)})

    if poll is not None:
        poll["_id"] = str(poll["_id"])
        return poll
    else:
        return {"error": "poll not found"}


@router.get("/get/post/{postID}")
async def getPoll(postID: str):
    poll = pollscoll.find_one({"postID": postID})

    if poll is not None:
        poll["_id"] = str(poll["_id"])
        return poll
    else:
        return {"error": "poll not found"}


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
                    return {"error": "already voted"}
                else:
                    return {"error": "option not found"}
        else:
            return {"error": "poll not found"}
