# Market Sentiment Analyzer - Category B Project

## Project Overview
This project implements a comprehensive market sentiment analysis system that combines:
- **Data Ingestion**: Yahoo Finance (Gold prices), Reuters RSS feeds, Reddit posts
- **Sentiment Analysis**: VADER (NLTK) for 3-class sentiment classification
- **Deep Learning**: LSTM, GRU, and RNN models for time-series forecasting
- **Frontend**: Streamlit dashboard for interactive market insights

## Project Components

### 1. **Data Scrapers**

#### Yahoo Finance (`yfinance.py`)
Fetches hourly gold (XAU/USD) price data for the last 60 days.

**Usage:**
```python
from yfinance import fetch_gold_price_data

gold_data = fetch_gold_price_data()
print(gold_data.head())
```

**Output**: DataFrame with OHLC data saved to `market_prices.csv`

---

#### Reuters News (`news.py`)
Scrapes financial headlines from Reuters RSS feeds (Business, Markets, Technology).

**Usage:**
```python
from news import fetch_reuters_financial_news

headlines = fetch_reuters_financial_news()
for headline in headlines:
    print(f"Title: {headline['title']}")
    print(f"Published: {headline['published']}")
```

**Returns**: List of dictionaries with title, date, link, and summary

---

#### Reddit Posts (`reddit.py`)
Extracts top 100 posts from r/wallstreetbets and r/finance.

**Setup:**
1. Create a Reddit app: https://www.reddit.com/prefs/apps
2. Update credentials in reddit.py:
```python
client_id = 'YOUR_ID'
client_secret = 'YOUR_SECRET'
user_agent = 'FinanceScraper'
```

**Usage:**
```python
from reddit import fetch_reddit_posts, save_reddit_posts_to_csv

posts = fetch_reddit_posts(client_id, client_secret, user_agent)
save_reddit_posts_to_csv(posts)
```

**Output**: `reddit_posts.csv` with posts from both subreddits

---

### 2. **Sentiment Analysis** (`sentiment.py`)

Uses NLTK VADER for 3-class sentiment classification:
- **Positive**: Compound score > 0.05 (Label: 1)
- **Negative**: Compound score < -0.05 (Label: -1)
- **Neutral**: -0.05 ≤ Compound score ≤ 0.05 (Label: 0)

**Usage:**
```python
from sentiment import analyze_sentiment, get_sentiment_label_text

result = analyze_sentiment("The stock market reached all-time highs!")
print(f"Sentiment: {get_sentiment_label_text(result['sentiment'])}")
print(f"Score: {result['compound_score']:.3f}")
```

**Returns**: Dictionary with sentiment label, compound score, and component scores

---

### 3. **Deep Learning Models** (`models.py`)

Implements three sequential models for time-series classification:

#### LSTM Model
```python
from models import build_lstm

model = build_lstm(input_shape=(30, 4))  # 30 time steps, 4 features
model.summary()
```
- LSTM layer: 50 units
- Dropout: 0.2
- Output: 3-class softmax

#### GRU Model
```python
from models import build_gru

model = build_gru(input_shape=(30, 4))
```
- GRU layer: 50 units
- Dropout: 0.2
- Output: 3-class softmax

#### RNN Model
```python
from models import build_rnn

model = build_rnn(input_shape=(30, 4))
```
- SimpleRNN layer: 50 units
- Dropout: 0.2
- Output: 3-class softmax

**Compare All Models:**
```python
from models import get_all_models

input_shape = (30, 4)
models = get_all_models(input_shape)

for name, model in models.items():
    print(f"\n{name} Model:")
    print(f"Parameters: {model.count_params():,}")
```

---

### 4. **Streamlit Dashboard** (`app.py`)

Interactive web application for sentiment analysis and market insights.
**Features:**
- **Sentiment Analysis Tab**: Real-time text sentiment analysis
- **Market Insights Tab**: Live market metrics and sentiment distribution
- **About Tab**: Project information and statistics

**Run the app:**
```bash
streamlit run app.py
```
Open browser at `http://localhost:8501`

---
## Installation & Setup

### 1. Create Virtual Environment
```bash
python -m venv .venv-1
.venv-1\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python sentiment.py          # Test VADER sentiment analysis
python models.py             # Build and test models
python yfinance.py           # Fetch market data
python news.py               # Scrape Reuters headlines
```

---

## Requirements

All dependencies are listed in `requirements.txt`:

- **yfinance** (0.2.32): Yahoo Finance data
- **feedparser** (6.0.10): RSS feed parsing
- **praw** (7.7.0): Reddit API
- **nltk** (3.8.1): VADER sentiment analysis
- **tensorflow** (2.14.0): Deep learning models
- **streamlit** (1.28.1): Web dashboard
- **pandas** (2.1.3): Data manipulation
- **numpy** (1.26.2): Numerical computing

---

## Project Architecture

```
ANN Project/
├── yfinance.py          # Yahoo Finance scraper
├── news.py              # Reuters RSS scraper
├── reddit.py            # Reddit posts scraper
├── sentiment.py         # VADER sentiment analysis
├── models.py            # LSTM, GRU, RNN models
├── app.py               # Streamlit dashboard
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## Workflow

### Data Collection Pipeline
```
Yahoo Finance Data → Sentiment Analysis
     ↓
Reddit Posts → Sentiment Scoring
     ↓
Reuters Headlines → VADER Classification
```

### Model Training Pipeline
```
Combined Sentiment + Market Data
     ↓
Prepare sequences (30 time steps)
     ↓
Train LSTM/GRU/RNN models
     ↓
Evaluate on test set
     ↓
Deploy in Streamlit dashboard
```

---

## Learning Objectives Met

### Data Ingestion (Category B)
- Yahoo Finance: Hourly gold prices 
- Reuters RSS: Financial headlines 
- Reddit PRAW: Social sentiment 

### Sentiment Labeling
- VADER sentiment analysis 
- 3-class classification 
- Compound score thresholds 

### Sequential Models (Minimum 3)
- LSTM model 
- GRU model 
- RNN model 

### Frontend
- Streamlit dashboard 
- Real-time sentiment analysis 
- Market insights visualization 

---

## Troubleshooting

### Issue: ImportError for NLTK VADER
**Solution**: The sentiment.py script automatically downloads required data.

### Issue: Reddit API Authentication Failed
**Solution**: 
1. Ensure credentials are correct
2. Verify your Reddit app is registered at reddit.com/prefs/apps
3. Use correct user_agent format

### Issue: TensorFlow GPU/CPU Warnings
**Solution**: Normal behavior. Models will run on CPU by default if GPU not available.

---

## Example Usage

### Complete Workflow
```python
# Step 1: Fetch data
from yfinance import fetch_gold_price_data
from news import fetch_reuters_financial_news
from sentiment import analyze_sentiment
from models import get_all_models
import numpy as np

# Get market data
gold_data = fetch_gold_price_data()

# Get news
headlines = fetch_reuters_financial_news()

# Analyze sentiment
for headline in headlines[:5]:
    result = analyze_sentiment(headline['title'])
    print(f"{headline['title']}: {result['sentiment']}")

# Build models
models = get_all_models((30, 4))

# Prepare dummy data
X_data = np.random.randn(1000, 30, 4)
y_data = np.random.randint(0, 3, 1000)

# Train LSTM
lstm_model = models['LSTM']
lstm_model.fit(X_data, y_data, epochs=5, batch_size=32)

print("Project complete!")
```

---

## References

- **VADER**: https://github.com/cjhutto/vaderSentiment
- **yfinance**: https://github.com/ranaroussi/yfinance
- **TensorFlow/Keras**: https://www.tensorflow.org/
- **Streamlit**: https://streamlit.io/
- **PRAW**: https://praw.readthedocs.io/