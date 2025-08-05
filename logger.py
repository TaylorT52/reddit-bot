# logger.py

import json
from datetime import datetime
from pathlib import Path

# Set the file name where logs are stored
FLAGGED_FILE = "logs/flagged.json"

# Make sure the file exists
Path(FLAGGED_FILE).touch(exist_ok=True)

def log_flagged_post(post, matched_keywords, response):
    entry = {
        "timestamp_utc": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "post_id": post.id,
        "subreddit": post.subreddit.display_name,
        "title": post.title,
        "url": f"https://reddit.com{post.permalink}",
        "matched_keywords": matched_keywords,
        "response": response
    }

    # Append to JSON file as newline-delimited entry
    with open(FLAGGED_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
