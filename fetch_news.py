import feedparser
from datetime import datetime

# Create a function using feedparser to scrape headlines from Reuters financial RSS feeds, extract the publication date and title, and return a list of dictionaries.
def fetch_reuters_financial_news():
    """
    Scrape headlines from Reuters financial RSS feeds.
    
    Returns:
        list: List of dictionaries containing headline, publication date, and link
    """
    reuters_feeds = [
        "http://feeds.reuters.com/reuters/businessNews",
        "http://feeds.reuters.com/reuters/marketsNews",
        "http://feeds.reuters.com/reuters/technologyNews"
    ]
    
    headlines = []
    
    for feed_url in reuters_feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                headline_dict = {
                    'title': entry.get('title', 'N/A'),
                    'published': entry.get('published', 'N/A'),
                    'link': entry.get('link', 'N/A'),
                    'summary': entry.get('summary', 'N/A')[:200] if entry.get('summary') else 'N/A'
                }
                headlines.append(headline_dict)
        except Exception as e:
            print(f"Error fetching from {feed_url}: {e}")
            continue
    
    return headlines

if __name__ == "__main__":
    # Example usage
    news_data = fetch_reuters_financial_news()
    print(f"Fetched {len(news_data)} headlines")
    for headline in news_data[:5]:
        print(f"Headline: {headline['title']}")
        print(f"Published: {headline['published']}")
        print(f"Link: {headline['link']}")
        print("-" * 80)