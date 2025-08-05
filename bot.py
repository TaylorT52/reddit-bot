import praw
import json
import time
import random
import logging
from datetime import datetime, timedelta
from pathlib import Path
from logger import log_flagged_post
from generate_reply import generate_reply

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RedditBot:
    def __init__(self):
        self.accounts = json.load(open("accounts.json"))
        self.account = random.choice(self.accounts)
        self.KEYWORDS = [line.strip().lower() for line in open("keywords.txt")]
        self.SUBREDDITS = ["dataengineering", "martech", "marketingautomation", "marketing", "digitalmarketing", "dataisbeautiful", "marketingops", "CRM"]
        self.start_time = datetime.now()
        self.posts_processed = 0
        self.matches_found = 0
        self.errors = 0
        
        # Initialize Reddit client
        self.reddit_client = praw.Reddit(
            client_id=self.account["client_id"],
            client_secret=self.account["client_secret"],
            username=self.account["username"],
            password=self.account["password"],
            user_agent=self.account["user_agent"]
        )
        
        logger.info(f"Bot initialized with account: {self.account['username']}")
        logger.info(f"Monitoring subreddits: {', '.join(self.SUBREDDITS)}")
        logger.info(f"Loaded {len(self.KEYWORDS)} keywords")
    
    def should_comment(self, post):
        """Check if we should comment on this post"""
        # Don't comment if we've already responded (you can add this later)
        # if post.id in self.responded_to:
        #     return False
        
        # Don't comment on posts older than 24 hours
        post_age = datetime.now() - datetime.fromtimestamp(post.created_utc)
        if post_age > timedelta(hours=24):
            return False
        
        # Don't comment if post has too many comments (avoid spam)
        if post.num_comments > 50:
            return False
        
        return True
    
    def process_post(self, post):
        """ Process a single post """ 
        try:
            self.posts_processed += 1

            title_lower = post.title.lower()
            content_lower = getattr(post, 'selftext', '').lower()
            
            full_text = title_lower + " " + content_lower
            
            matched_keywords = [k for k in self.KEYWORDS if k in full_text]
            
            if matched_keywords:
                self.matches_found += 1
                logger.info(f"Match found: {post.title}")
                logger.info(f"Matched keywords: {matched_keywords}")
                
                # Check if we should comment
                if self.should_comment(post):
                    comment_text = generate_reply(post)
                    if comment_text and comment_text.strip():
                        try:
                            comment = post.reply(comment_text)
                            logger.info(f"Posted comment: {comment.id}")
                            time.sleep(random.uniform(60, 120))  # 1-2 minutes; varied response time prevents being marked spam
                        except Exception as e:
                            logger.error(f"Error posting comment: {e}")
                            self.errors += 1
                            time.sleep(300)  # Wait 5 minutes on error
                    else:
                        logger.info("No valid reply generated, skipping comment")
                
                # Log the interaction
                log_flagged_post(post, matched_keywords, response=comment_text if 'comment_text' in locals() else "")
            else: 
                logger.info("Post contained no keywords.")
            
            # Print status every 10 posts
            if self.posts_processed % 10 == 0:
                self.print_status()
                
        except Exception as e:
            logger.error(f"Error processing post: {e}")
            self.errors += 1
    
    def print_status(self):
        """Print current bot status"""
        runtime = datetime.now() - self.start_time
        logger.info(f"=== BOT STATUS ===")
        logger.info(f"Runtime: {runtime}")
        logger.info(f"Posts processed: {self.posts_processed}")
        logger.info(f"Matches found: {self.matches_found}")
        logger.info(f"Errors: {self.errors}")
        logger.info(f"==================")
    
    def run_continuously(self):
        logger.info("Starting Reddit bot in continuous mode...")
        
        while True:
            try:
                logger.info("Starting new stream...")
                
                # Test subreddit access first
                for subreddit_name in self.SUBREDDITS:
                    try:
                        subreddit = self.reddit_client.subreddit(subreddit_name)
                        # Try to get one post to test access
                        test_posts = list(subreddit.new(limit=1))
                        if test_posts:
                            logger.info(f"✅ Successfully accessed r/{subreddit_name}")
                        else:
                            logger.warning(f"⚠️ No posts found in r/{subreddit_name}")
                    except Exception as e:
                        logger.error(f"❌ Cannot access r/{subreddit_name}: {e}")
                        continue
                
                # Create stream with better configuration
                subreddit_stream = self.reddit_client.subreddit("+".join(self.SUBREDDITS)).stream.submissions(
                    skip_existing=True,
                    pause_after=10  # Pause after 10 None responses
                )
                
                logger.info("Stream created successfully, monitoring for new posts...")
                
                for post in subreddit_stream:
                    if post is None: 
                        logger.info("No new posts, continuing to monitor...")
                        continue
                    
                    self.process_post(post)
                    time.sleep(1)
                
            except Exception as e:
                logger.error(f"Stream error: {e}")
                self.errors += 1
                logger.info("Waiting 30 seconds before restarting...")
                time.sleep(30)
            
            # Print status every hour
            if (datetime.now() - self.start_time).seconds % 3600 < 60:
                self.print_status()

def main():
    try:
        bot = RedditBot()
        bot.run_continuously()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        bot.print_status()
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()