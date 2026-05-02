from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download required VADER lexicon
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

# Create a sentiment analysis function using NLTK VADER that takes a string and returns 1 for Positive (score > 0.05), -1 for Negative (score < -0.05), and 0 for Neutral.
def analyze_sentiment(text):
    """
    Analyze sentiment of text using VADER and return simple sentiment label.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Dictionary with sentiment label (1=Positive, -1=Negative, 0=Neutral) and compound score
    """
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    
    # Three-class sentiment classification
    if compound > 0.05:
        sentiment_label = 1  # Positive
    elif compound < -0.05:
        sentiment_label = -1  # Negative
    else:
        sentiment_label = 0  # Neutral
    
    return {
        'sentiment': sentiment_label,
        'compound_score': compound,
        'positive': scores['pos'],
        'negative': scores['neg'],
        'neutral': scores['neu']
    }

def get_sentiment_label_text(label):
    """
    Convert numeric sentiment label to text.
    
    Args:
        label (int): Sentiment label (1, -1, or 0)
        
    Returns:
        str: Sentiment label as text
    """
    label_map = {1: 'Positive', -1: 'Negative', 0: 'Neutral'}
    return label_map.get(label, 'Unknown')

if __name__ == "__main__":
    # Test cases
    test_texts = [
        "The market is soaring! Great news for investors!",
        "Stock prices are collapsing. Investors are panicking.",
        "The market closed with mixed signals today.",
        "I love this company, it's the best!",
        "This is terrible, I'm losing money."
    ]
    
    print("VADER Sentiment Analysis - 3-Class Classification")
    print("=" * 70)
    
    for text in test_texts:
        result = analyze_sentiment(text)
        label_text = get_sentiment_label_text(result['sentiment'])
        print(f"\nText: {text}")
        print(f"Sentiment: {label_text} (Label: {result['sentiment']})")
        print(f"Compound Score: {result['compound_score']:.3f}")
        print(f"Positive: {result['positive']:.3f}, Negative: {result['negative']:.3f}, Neutral: {result['neutral']:.3f}")
