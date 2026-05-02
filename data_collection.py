"""
Real-time data collection pipeline for market prediction
Collects: Stock prices, Financial news, Reddit posts
"""

import os
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import yfinance as yf
import feedparser
import requests
from pathlib import Path

# Try to import PRAW for Reddit data
try:
    import praw
    PRAW_AVAILABLE = True
except ImportError:
    PRAW_AVAILABLE = False
    print("Warning: PRAW not available. Reddit data collection will be skipped.")


class DataCollector:
    """Main pipeline for collecting financial market data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.collection_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # ===================== PRICE DATA =====================
    def fetch_stock_prices(self, tickers: List[str] = None, period: str = "30d") -> pd.DataFrame:
        """
        Fetch OHLC price data from Yahoo Finance
        
        Args:
            tickers: List of stock tickers (default: Gold, S&P 500)
            period: Time period (default: 30 days)
        
        Returns:
            Combined DataFrame with all price data
        """
        if tickers is None:
            tickers = ["GC=F", "^GSPC"]  # Gold futures and S&P 500
        
        all_prices = {}
        
        print(f"\n📈 Fetching price data for: {tickers}")
        
        for ticker in tickers:
            try:
                print(f"  Downloading {ticker}...")
                data = yf.Ticker(ticker).history(period=period)
                
                if data is not None and len(data) > 0:
                    data['Ticker'] = ticker
                    data['Timestamp'] = data.index
                    all_prices[ticker] = data.reset_index(drop=True)
                    print(f"  ✓ Got {len(data)} records for {ticker}")
                else:
                    print(f"  ✗ No data for {ticker}")
            except Exception as e:
                print(f"  ✗ Error fetching {ticker}: {e}")
        
        # Combine all price data
        if all_prices:
            combined_df = pd.concat(all_prices.values(), ignore_index=True)
            combined_df = combined_df.sort_values('Timestamp').reset_index(drop=True)
            return combined_df
        else:
            print("✗ No price data collected")
            return pd.DataFrame()
    
    # ===================== NEWS DATA =====================
    def fetch_financial_news(self, feed_urls: List[str] = None) -> pd.DataFrame:
        """
        Fetch financial news from RSS feeds
        
        Args:
            feed_urls: List of RSS feed URLs (default: Reuters feeds)
        
        Returns:
            DataFrame with news headlines and metadata
        """
        if feed_urls is None:
            feed_urls = [
                "http://feeds.reuters.com/reuters/businessNews",
                "http://feeds.reuters.com/reuters/marketsNews",
                "http://feeds.reuters.com/reuters/technologyNews"
            ]
        
        headlines = []
        print(f"\n📰 Fetching financial news from {len(feed_urls)} feeds")
        
        for feed_url in feed_urls:
            try:
                print(f"  Parsing {feed_url.split('/')[-1]}...")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:20]:  # Limit to 20 per feed
                    try:
                        headline_dict = {
                            'title': entry.get('title', 'N/A'),
                            'published': entry.get('published', datetime.now().isoformat()),
                            'link': entry.get('link', 'N/A'),
                            'summary': entry.get('summary', 'N/A')[:300],
                            'source': 'Reuters',
                            'timestamp': datetime.now().isoformat()
                        }
                        headlines.append(headline_dict)
                    except Exception as e:
                        print(f"    Error processing entry: {e}")
                        continue
                
                print(f"  ✓ Got {len([h for h in headlines if h['source'] == 'Reuters'])} headlines from Reuters")
            except Exception as e:
                print(f"  ✗ Error fetching from {feed_url}: {e}")
        
        if headlines:
            news_df = pd.DataFrame(headlines)
            news_df['published'] = pd.to_datetime(news_df['published'], errors='coerce')
            return news_df
        else:
            print("✗ No news data collected")
            return pd.DataFrame()
    
    # ===================== REDDIT DATA =====================
    def fetch_reddit_posts(self, client_id: str = None, client_secret: str = None, 
                          user_agent: str = None, subreddits: List[str] = None) -> pd.DataFrame:
        """
        Fetch Reddit posts using PRAW
        
        Args:
            client_id: Reddit API client ID
            client_secret: Reddit API client secret
            user_agent: Reddit API user agent
            subreddits: List of subreddits to scrape
        
        Returns:
            DataFrame with Reddit posts
        """
        if not PRAW_AVAILABLE:
            print("\n⚠️ PRAW not available. Skipping Reddit data collection.")
            print("   Install with: pip install praw")
            return pd.DataFrame()
        
        # Try to get credentials from environment
        if client_id is None:
            client_id = os.getenv('REDDIT_CLIENT_ID')
        if client_secret is None:
            client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        if user_agent is None:
            user_agent = os.getenv('REDDIT_USER_AGENT', 'FinanceMarketPrediction/1.0')
        
        if not client_id or not client_secret or client_id == "your_client_id_here":
            print("\n⚠️ Reddit credentials not configured. Skipping Reddit data.")
            print("   Setup: Copy .env.example to .env and add your credentials")
            print("   Get credentials: https://www.reddit.com/prefs/apps")
            return pd.DataFrame()
        
        posts = []
        if subreddits is None:
            subreddits = ['wallstreetbets', 'finance', 'stocks']
        
        print(f"\n🔴 Fetching Reddit posts from: {subreddits}")
        
        try:
            reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            
            for subreddit_name in subreddits:
                try:
                    print(f"  Scraping r/{subreddit_name}...")
                    subreddit = reddit.subreddit(subreddit_name)
                    
                    for submission in subreddit.hot(limit=50):
                        post_data = {
                            'title': submission.title,
                            'body': submission.selftext[:500] if submission.selftext else '',
                            'timestamp': datetime.fromtimestamp(submission.created_utc).isoformat(),
                            'score': submission.score,
                            'num_comments': submission.num_comments,
                            'subreddit': subreddit_name,
                            'url': submission.url
                        }
                        posts.append(post_data)
                    
                    print(f"  ✓ Got {len([p for p in posts if p['subreddit'] == subreddit_name])} posts from r/{subreddit_name}")
                except Exception as e:
                    print(f"  ✗ Error fetching r/{subreddit_name}: {e}")
        
        except Exception as e:
            print(f"✗ Reddit authentication failed: {e}")
            return pd.DataFrame()
        
        if posts:
            reddit_df = pd.DataFrame(posts)
            return reddit_df
        else:
            print("✗ No Reddit posts collected")
            return pd.DataFrame()
    
    # ===================== DATA AGGREGATION =====================
    def collect_all_data(self, include_reddit: bool = True) -> Dict[str, pd.DataFrame]:
        """
        Collect data from all sources
        
        Args:
            include_reddit: Whether to include Reddit data
        
        Returns:
            Dictionary with DataFrames for each data source
        """
        print("\n" + "="*60)
        print("🚀 STARTING DATA COLLECTION PIPELINE")
        print("="*60)
        
        data_sources = {}
        
        # Collect price data
        prices_df = self.fetch_stock_prices()
        if not prices_df.empty:
            data_sources['prices'] = prices_df
            self._save_data(prices_df, 'prices')
        
        # Collect news data
        news_df = self.fetch_financial_news()
        if not news_df.empty:
            data_sources['news'] = news_df
            self._save_data(news_df, 'news')
        
        # Collect Reddit data (optional)
        if include_reddit:
            reddit_df = self.fetch_reddit_posts()
            if not reddit_df.empty:
                data_sources['reddit'] = reddit_df
                self._save_data(reddit_df, 'reddit')
        
        print("\n" + "="*60)
        print("✅ DATA COLLECTION COMPLETE")
        print("="*60)
        print(f"\nData Summary:")
        for source, df in data_sources.items():
            print(f"  {source:12} : {len(df):5} records")
        
        return data_sources
    
    def _save_data(self, df: pd.DataFrame, source_name: str) -> None:
        """Save DataFrame to CSV"""
        filename = self.data_dir / f"{source_name}_{self.collection_timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"  📁 Saved to: {filename}")
    
    def save_combined_data(self, data_sources: Dict[str, pd.DataFrame]) -> None:
        """Save metadata about collected data"""
        metadata = {
            'collection_timestamp': self.collection_timestamp,
            'sources': {
                source: {
                    'records': len(df),
                    'columns': list(df.columns)
                }
                for source, df in data_sources.items()
            }
        }
        
        metadata_file = self.data_dir / f"metadata_{self.collection_timestamp}.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n📄 Metadata saved to: {metadata_file}")


def main():
    """Run the complete data collection pipeline"""
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    collector = DataCollector(data_dir="data")
    
    # Collect data from all sources
    data_sources = collector.collect_all_data(include_reddit=True)
    
    # Save metadata
    collector.save_combined_data(data_sources)
    
    # Display sample data
    print("\n" + "="*60)
    print("📊 SAMPLE DATA")
    print("="*60)
    
    if 'prices' in data_sources:
        print("\n💰 Price Data Sample:")
        print(data_sources['prices'].head())
    
    if 'news' in data_sources:
        print("\n📰 News Data Sample:")
        print(data_sources['news'][['title', 'published', 'source']].head())
    
    if 'reddit' in data_sources:
        print("\n🔴 Reddit Data Sample:")
        print(data_sources['reddit'][['title', 'score', 'subreddit']].head())


if __name__ == "__main__":
    main()
