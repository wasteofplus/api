from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
from cachetools import TTLCache

load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

client = MongoClient(CONNECTION_STRING)
print("connect to db")
db = client["wasteofplus"]
pollscoll = db["polls"]
reactionscoll = db["reactions"]
idCache = TTLCache(maxsize=1000, ttl=300)


def verify(username: str, token: str):
    session = requests.get(
        "https://api.wasteof.money/session", headers={"Authorization": token}
    ).json()

    if "user" in session and session["user"]["name"] == username:
        return True
    else:
        return False
