import praw
import csv
from datetime import datetime

# Use PRAW to scrape the top 100 posts from 'r/wallstreetbets' and 'r/finance', extracting the post title, timestamp, and score into a CSV.
def fetch_reddit_posts(client_id, client_secret, user_agent):
    """
    Scrape top 100 posts from r/wallstreetbets and r/finance.
    
    Args:
        client_id: Reddit API client ID
        client_secret: Reddit API client secret
        user_agent: Reddit API user agent
        
    Returns:
        list: List of posts with title, timestamp, and score
    """
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    
    posts = []
    subreddits = ['wallstreetbets', 'finance']
    
    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            for submission in subreddit.hot(limit=100):
                post_data = {
                    'title': submission.title,
                    'timestamp': datetime.fromtimestamp(submission.created_utc),
                    'score': submission.score,
                    'subreddit': subreddit_name,
                    'url': submission.url
                }
                posts.append(post_data)
            print(f"Fetched {len([p for p in posts if p['subreddit'] == subreddit_name])} posts from r/{subreddit_name}")
        except Exception as e:
            print(f"Error fetching from r/{subreddit_name}: {e}")
            continue
    
    return posts

def save_reddit_posts_to_csv(posts, filename='reddit_posts.csv'):
    """
    Save scraped Reddit posts to a CSV file.
    
    Args:
        posts: List of post dictionaries
        filename: Output CSV filename
    """
    if not posts:
        print("No posts to save")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'timestamp', 'score', 'subreddit', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for post in posts:
                writer.writerow(post)
        
        print(f"Successfully saved {len(posts)} posts to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    # Replace with your Reddit API credentials
    client_id = 'YOUR_ID'
    client_secret = 'YOUR_SECRET'
    user_agent = 'FinanceScraper'
    
    if client_id != 'YOUR_ID':  # Only run if credentials are set
        posts = fetch_reddit_posts(client_id, client_secret, user_agent)
        save_reddit_posts_to_csv(posts)
    else:
        print("Please update Reddit API credentials before running")