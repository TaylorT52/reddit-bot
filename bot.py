import praw, json, time, random
from pathlib import Path

accounts = json.load(open("accounts.json"))
account = random.choice(accounts)

reddit_client = praw.Reddit(
    client_id=account["client_id"],
    client_secret=account["client_secret"],
    username=account["username"],
    password=account["password"],
    user_agent=account["user_agent"]
)

keywords = [line.strip().lower() for line in open("keywords.txt")]
responded_to = set(json.load(open("responded.json")))

subreddits = ["DataEngineering", "MarketingTechnology"]

def generate_reply(post):
    return f"Interesting post about {', '.join([k for k in keywords if k in post.title.lower()])}!"

print("Bot running...")
for post in reddit.subreddit("+".join(subreddits)).stream.submissions(skip_existing=True):

    title_lower = post.title.lower()
    matched_keywords = [k for k in keywords if k in title_lower]
    comment = generate_reply(post)

    if matched_keywords:
        print(f"Match found: {post.title}")
        try:
            responded_to.add(post.id)
            json.dump(list(responded_to), open("responded.json", "w"))
            log_flagged_post(post, matched_keywords, response=comment) 
            time.sleep(30) 
        except Exception as e:
            print(f"Error: {e}")
            log_flagged_post(post, matched_keywords, response=comment) 
            time.sleep(60)