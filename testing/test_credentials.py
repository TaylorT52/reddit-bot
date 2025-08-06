import praw
import json

def test_reddit_credentials():
    """Test if Reddit credentials are working"""
    try:
        # Load credentials
        with open("accounts.json", "r") as f:
            accounts = json.load(f)
        
        account = accounts[0]
        
        print("Testing Reddit credentials...")
        print(f"Username: {account['username']}")
        print(f"Client ID: {account['client_id'][:10]}...")  # Only show first 10 chars for security
        
        # Initialize Reddit client
        reddit = praw.Reddit(
            client_id=account["client_id"],
            client_secret=account["client_secret"],
            username=account["username"],
            password=account["password"],
            user_agent=account["user_agent"]
        )
        
        # Test authentication
        print("Testing authentication...")
        user = reddit.user.me()
        print(f"✅ Successfully authenticated as: {user.name}")
        
        # Test subreddit access
        print("Testing subreddit access...")
        subreddit = reddit.subreddit("DataEngineering")
        print(f"✅ Successfully accessed r/DataEngineering")
        
        # Test getting recent posts
        print("Testing post retrieval...")
        posts = list(subreddit.new(limit=1))
        if posts:
            print(f"✅ Successfully retrieved post: {posts[0].title[:50]}...")
        
        print("\n🎉 All tests passed! Your credentials are working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nPlease check your credentials in accounts.json")
        return False

if __name__ == "__main__":
    test_reddit_credentials() 