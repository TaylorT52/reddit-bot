import praw, json, time, random
from pathlib import Path

accounts = json.load(open("accounts.json"))
account = random.choice(accounts)
