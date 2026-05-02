# Real-Time Market Movement Prediction System - Data Collection Guide

## 📋 Overview

This project implements a real-time financial market prediction system using sequential deep learning models (RNN, LSTM, GRU) with sentiment analysis of financial news and social media data.

## 🎯 Quick Start

### 1. Setup Environment

```bash
# Create/activate virtual environment (already done)
.\.venv-1\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Collect Real-Time Data

```bash
python data_collection.py
```

This will:
- ✅ Download 30 days of historical price data (Gold futures & S&P 500)
- ✅ Scrape financial news from Reuters feeds
- ✅ (Optional) Fetch Reddit posts from finance communities
- 📁 Save all data to `data/` directory

### 3. Preprocess Data

```bash
python data_loader.py
```

This will:
- ✅ Load collected data
- ✅ Prepare target variables (price direction: up/down)
- ✅ Create sequences for RNN/LSTM/GRU models
- ✅ Split train/test data
- 📁 Save preprocessed data to `.npy` files

### 4. Run Sentiment Analysis

```bash
python sentiment_analysis.py
```

## 📊 Data Sources

### Price Data (✅ Working)
- **Source**: Yahoo Finance via `yfinance`
- **Assets**: Gold futures (GC=F), S&P 500 (^GSPC)
- **Period**: 30 days of daily data
- **Features**: Open, High, Low, Close, Volume

**Sample Data (prices_20260503_011933.csv):**
```
55 records collected
Date Range: 2026-03-20 to 2026-05-03
Features: Open, High, Low, Close, Volume, Dividends, Stock Splits, Ticker
```

### Financial News (⏳ Configure for Production)
- **Source**: Reuters RSS feeds
- **Categories**: Business, Markets, Technology
- **Fields**: Title, Published date, Summary, Link

To activate news collection, verify RSS feeds are accessible in your network.

### Social Media (🔐 Requires API Credentials)
- **Source**: Reddit via PRAW
- **Subreddits**: r/wallstreetbets, r/finance, r/stocks
- **Fields**: Title, Score, Comments, Timestamp

**Setup Reddit API:**
1. Go to https://www.reddit.com/prefs/apps
2. Create a new app (script)
3. Copy `.env.example` to `.env`
4. Fill in your credentials:
   ```
   REDDIT_CLIENT_ID=your_id_here
   REDDIT_CLIENT_SECRET=your_secret_here
   REDDIT_USER_AGENT=FinanceMarketPrediction/1.0
   ```

## 📈 Data Pipeline

```
┌─────────────────────┐
│  Real-time Sources  │
├─────────────────────┤
│ • Yahoo Finance     │
│ • Reuters RSS       │
│ • Reddit API        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Data Collection     │
│ (data_collection.py)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Data Loading        │
│ (data_loader.py)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Sentiment Analysis  │
│ (sentiment_analysis)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Time-Series Data    │
│ X, y arrays ready   │
│ for model training  │
└─────────────────────┘
```

## 📁 Data Directory Structure

```
data/
├── prices_20260503_011933.csv      # Price data (OHLC)
├── X_train.npy                      # Training sequences (40, 5, 5)
├── X_test.npy                       # Test sequences (10, 5, 5)
├── y_train.npy                      # Training targets (40,)
├── y_test.npy                       # Test targets (10,)
└── metadata_20260503_011933.json    # Collection metadata
```

## 🔍 Current Data Summary

| Source | Records | Status |
|--------|---------|--------|
| **Prices** | 55 | ✅ Active |
| **News** | 0* | ⏳ Setup needed |
| **Reddit** | 0* | 🔐 Credentials needed |

*Working on improving feed reliability

## 🎯 Prepared Training Data

### Features & Target Variable

- **Sequence Length**: 5 time steps
- **Features per Time Step**: 5 (Open, High, Low, Close, Volume)
- **Target**: Binary classification (1=price up, 0=price down)

### Split

- **Training Samples**: 40 sequences
- **Test Samples**: 10 sequences
- **Feature Normalization**: Z-score normalized
- **Train/Test Ratio**: 80/20 (temporal split)

### Class Distribution

```
✓ Positive class (price up): 32
✓ Negative class (price down): 23
```

## 🤖 Model Training (Next Steps)

The prepared data is ready for the following models:

1. **RNN (Recurrent Neural Network)**
2. **LSTM (Long Short-Term Memory)**
3. **GRU (Gated Recurrent Unit)**

Load training data in your model scripts:
```python
import numpy as np

X_train = np.load('data/X_train.npy')
X_test = np.load('data/X_test.npy')
y_train = np.load('data/y_train.npy')
y_test = np.load('data/y_test.npy')

# X shape: (samples, sequence_length, features)
# y: binary targets (0 or 1)
```

## 📊 Sentiment Analysis Features

### Analysis Methods Available

1. **VADER** (Valence Aware Dictionary and sEntiment Reasoner)
   - Best for social media & financial texts
   - Compound score: -1 (most negative) to +1 (most positive)

2. **TextBlob**
   - Polarity: -1 to +1
   - Subjectivity: 0 to 1

3. **Hybrid**
   - Combines VADER and TextBlob results

### Usage

```python
from sentiment_analysis import SentimentAnalyzer

analyzer = SentimentAnalyzer(method='vader')

# Single text
result = analyzer.analyze("Stock prices surge!")
print(result['label'])  # 'Positive', 'Negative', or 'Neutral'

# Batch analysis
results_df = analyzer.analyze_batch(texts_list)

# Time-series aggregation
agg = analyzer.aggregate_sentiment(results_df, time_col='timestamp')
```

## ⚙️ Configuration

### Modify Data Collection Targets

Edit `data_collection.py`:

```python
# Change tickers
tickers = ["AAPL", "MSFT", "GOOGL"]  # Add your symbols

# Change time period
period = "60d"  # 60 days of data

# Change subreddits
subreddits = ['investing', 'stocks', 'cryptocurrency']
```

### Environment Variables (.env)

```
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=YourApp/1.0
```

## 🐛 Troubleshooting

### Issue: "No data collected"

**Price Data:**
- Check internet connection
- Verify ticker symbols are valid
- Check Yahoo Finance availability

**News Data:**
- Reuters feeds may be restricted in some regions
- Try using alternative news APIs (NewsAPI, Finnhub)

**Reddit Data:**
- Verify credentials in `.env` file
- Check PRAW installation: `pip install praw`
- Ensure Reddit API credentials are correct

### Issue: ImportError with yfinance

**Solution**: Your project had a naming conflict. We've renamed:
- `yfinance.py` → `fetch_prices.py`
- `news.py` → `fetch_news.py`
- `reddit.py` → `fetch_reddit.py`

## 📚 Files Reference

| File | Purpose |
|------|---------|
| `data_collection.py` | Main pipeline to collect data from all sources |
| `data_loader.py` | Load, preprocess, and prepare time-series data |
| `sentiment_analysis.py` | Analyze sentiment of text data |
| `models.py` | RNN/LSTM/GRU model definitions |
| `app.py` | API/prediction interface |
| `requirements.txt` | Python dependencies |

## 🚀 Next Steps

1. **[Complete]** ✅ Data collection setup
2. **[Complete]** ✅ Data preprocessing
3. **[TODO]** Build RNN, LSTM, GRU models
4. **[TODO]** Train and evaluate models
5. **[TODO]** Compare model performance
6. **[TODO]** Integrate sentiment features
7. **[TODO]** Deploy as REST API

## 📝 Notes

- Data is collected in UTC timezone
- All prices are normalized using Z-score
- Sequences are temporally split (no data leakage)
- Sentiment scores range from -1 (most negative) to +1 (most positive)

## 🔗 Resources

- [yfinance Documentation](https://github.com/ranaroussi/yfinance)
- [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment)
- [PRAW Reddit API](https://praw.readthedocs.io/)
- [TextBlob](https://textblob.readthedocs.io/)

---

**Last Updated**: May 3, 2026  
**Data Collection Status**: ✅ Operational
