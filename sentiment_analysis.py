"""
Sentiment Analysis Module
Analyzes sentiment of financial news and social media posts
"""

import pandas as pd
import numpy as np
from typing import List, Dict
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download required NLTK data
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)


class SentimentAnalyzer:
    """Sentiment analysis for financial texts using multiple methods"""
    
    def __init__(self, method: str = 'vader'):
        """
        Initialize sentiment analyzer
        
        Args:
            method: 'vader', 'textblob', or 'hybrid'
        """
        self.method = method
        self.sia = SentimentIntensityAnalyzer()
    
    def analyze_vader(self, text: str) -> Dict:
        """
        Analyze sentiment using VADER (Valence Aware Dictionary and sEntiment Reasoner)
        Best for social media and financial texts
        
        Returns:
            Dict with sentiment scores and label
        """
        scores = self.sia.polarity_scores(text)
        
        compound = scores['compound']
        if compound >= 0.05:
            label = 'Positive'
        elif compound <= -0.05:
            label = 'Negative'
        else:
            label = 'Neutral'
        
        return {
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'compound': compound,
            'label': label
        }
    
    def analyze_textblob(self, text: str) -> Dict:
        """
        Analyze sentiment using TextBlob
        
        Returns:
            Dict with polarity, subjectivity and label
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        if polarity > 0.1:
            label = 'Positive'
        elif polarity < -0.1:
            label = 'Negative'
        else:
            label = 'Neutral'
        
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'label': label
        }
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment using selected method
        
        Args:
            text: Text to analyze
        
        Returns:
            Sentiment analysis results
        """
        if not text or len(text) < 3:
            return {'label': 'Neutral', 'confidence': 0.0}
        
        if self.method == 'vader':
            return self.analyze_vader(text)
        elif self.method == 'textblob':
            return self.analyze_textblob(text)
        else:  # hybrid
            vader_result = self.analyze_vader(text)
            textblob_result = self.analyze_textblob(text)
            
            # Combine results
            labels = [vader_result['label'], textblob_result['label']]
            label = max(set(labels), key=labels.count)
            
            return {
                'label': label,
                'vader_confidence': abs(vader_result['compound']),
                'textblob_confidence': abs(textblob_result['polarity']),
                'methods': {'vader': vader_result, 'textblob': textblob_result}
            }
    
    def analyze_batch(self, texts: List[str]) -> pd.DataFrame:
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts: List of texts to analyze
        
        Returns:
            DataFrame with sentiment results
        """
        results = []
        
        for text in texts:
            sentiment = self.analyze(text)
            sentiment['text'] = text[:100]  # Store truncated text
            results.append(sentiment)
        
        return pd.DataFrame(results)
    
    @staticmethod
    def aggregate_sentiment(df: pd.DataFrame, label_col: str = 'label', 
                          time_col: str = None, period: str = 'D') -> pd.DataFrame:
        """
        Aggregate sentiment over time
        
        Args:
            df: DataFrame with sentiment labels
            label_col: Column containing sentiment labels
            time_col: Column with timestamps (for time aggregation)
            period: Time period for aggregation ('D', 'H', 'W', etc.)
        
        Returns:
            Aggregated sentiment scores
        """
        if time_col is None:
            # Overall aggregation
            sentiment_counts = df[label_col].value_counts()
            total = len(df)
            
            return pd.Series({
                'Positive': sentiment_counts.get('Positive', 0) / total,
                'Negative': sentiment_counts.get('Negative', 0) / total,
                'Neutral': sentiment_counts.get('Neutral', 0) / total,
                'Total_Samples': total
            })
        else:
            # Time-based aggregation
            df[time_col] = pd.to_datetime(df[time_col])
            df_grouped = df.groupby(pd.Grouper(key=time_col, freq=period))
            
            results = []
            for period_date, group in df_grouped:
                if len(group) == 0:
                    continue
                
                sentiment_counts = group[label_col].value_counts()
                total = len(group)
                
                results.append({
                    'Period': period_date,
                    'Positive_Ratio': sentiment_counts.get('Positive', 0) / total,
                    'Negative_Ratio': sentiment_counts.get('Negative', 0) / total,
                    'Neutral_Ratio': sentiment_counts.get('Neutral', 0) / total,
                    'Sample_Count': total
                })
            
            return pd.DataFrame(results)


def main():
    """Example usage"""
    
    analyzer = SentimentAnalyzer(method='vader')
    
    print("\n" + "="*60)
    print("SENTIMENT ANALYSIS EXAMPLES")
    print("="*60)
    
    # Test texts
    test_texts = [
        "Stock market hits record highs!",
        "Market crash expected, investors worried",
        "Trading volumes remain stable today",
        "Company earnings beat expectations significantly",
        "Economic downturn feared by analysts"
    ]
    
    print("\n🔍 Individual text analysis (VADER):")
    for text in test_texts:
        result = analyzer.analyze(text)
        print(f"\n  Text: {text}")
        print(f"  Sentiment: {result['label']}")
        print(f"  Compound Score: {result['compound']:.3f}")
    
    # Batch analysis
    print("\n\n📊 Batch analysis:")
    results_df = analyzer.analyze_batch(test_texts)
    print(results_df[['label']].value_counts())
    
    # Aggregation example
    print("\n\n📈 Aggregated sentiment:")
    agg_sentiment = analyzer.aggregate_sentiment(results_df, label_col='label')
    print(agg_sentiment)


if __name__ == "__main__":
    main()
