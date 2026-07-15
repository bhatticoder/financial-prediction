# MarketMind AI - Financial Sentiment & Prediction Dashboard

## 📊 Project Overview
MarketMind AI is a comprehensive full-stack market prediction system that leverages live market data and deep learning models to predict the hourly trend of the SPY index or other commodities.

This project implements:
- **Data Ingestion**: Live market data scraping via Yahoo Finance (`yfinance`) with 1-hour intervals.
- **Deep Learning**: Powerful sequential models including GRU, LSTM, and RNN, trained on historical data.
- **Backend API**: A highly performant FastAPI backend serving model predictions and live market metrics.
- **Frontend Dashboard**: A premium, state-of-the-art Vanilla CSS and HTML5 dashboard featuring Lucide icons, glassmorphism UI, real-time Chart.js integrations, and seamless user experience.

## ✨ Features

- **Live Market Data feed**: Fetches the latest OHLCV market action.
- **Real-Time Predictions**: Calculates probability and confidence intervals for market direction (UP/DOWN) using the last 5 continuous hourly candles.
- **Advanced Model Selection**: Switch seamlessly between GRU, LSTM, and RNN models on the fly.
- **Premium User Interface**: Dark mode aesthetics with dynamic chart visualizations and micro-animations.

---

## 🏗️ Project Architecture

```
Financial Prediction/
├── app.py                   # FastAPI application serving endpoints & UI
├── models/                  # Saved Keras models (GRU, LSTM, RNN)
├── results/                 # Metrics and CSV results of trained models
├── static/
│   └── dashboard.html       # Premium UI dashboard
├── vercel.json              # Vercel deployment configuration
├── requirements.txt         # Python dependencies
└── README.md                # This documentation
```

## 🚀 Installation & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/bhatticoder/Finance-Prediction.git
cd Finance-Prediction
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the FastAPI server via Uvicorn:
```bash
python app.py
```
Open your browser at `http://127.0.0.1:8000` to view the MarketMind AI Dashboard.

---

## 📡 API Endpoints

- `GET /` or `GET /dashboard`: Serves the intuitive UI dashboard.
- `GET /api/latest?model={model_name}`: Retrieves the most recent market metrics and live data feed.
- `POST /api/predict`: Analyzes a custom series of continuous candlesticks and returns high-confidence predictions.
- `GET /api/metrics`: Provides evaluation metrics (Accuracy, F1 Score, Loss) for the selected AI model.
- `GET /health`: Health-check endpoint for service monitoring.

---

## 🌐 Deploying to Vercel

This repository is optimized for Vercel deployment. 

1. Ensure you have a Vercel account linked to your GitHub.
2. Import this repository as a New Project on Vercel.
3. Vercel will automatically detect the Python backend and `vercel.json` configuration.
4. Set the Framework Preset to `Other`.
5. Deploy! Vercel's Serverless Functions will handle the FastAPI routing, predicting, and serving the static dashboard on the edge.

*(Note: Ensure your `requirements.txt` complies with Vercel's Serverless Memory Limits for TensorFlow model loading.)*

---

## 🔧 Troubleshooting

- **No live data on dashboard**: Ensure your internet connection does not block `yfinance` requests.
- **TensorFlow warnings in console**: This is normal output when GPU acceleration is missing; models will effectively default to CPU inference.

---

**Built with ❤️ for advanced financial market analytics.**
