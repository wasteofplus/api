from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests

load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

client = MongoClient(CONNECTION_STRING)
db = client["wasteofplus"]
pollscoll = db["polls"]
print("connect to db")


def verify(username: str, token: str):
    session = requests.get(
        "https://api.wasteof.money/session", headers={"Authorization": token}
    ).json()

    if "user" in session and session["user"]["name"] == username:
        return True
    else:
        return False
