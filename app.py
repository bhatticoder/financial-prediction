from __future__ import annotations

import os
import json
import shutil
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

# Silence TensorFlow startup warnings before importing keras.
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

import numpy as np
import pandas as pd
import yfinance as yf
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from tensorflow import keras


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
MODEL_DIR = BASE_DIR / "models"
RESULTS_DIR = BASE_DIR / "results"
RUNTIME_MODEL_DIR = MODEL_DIR / ".runtime"

MARKET_SYMBOL = "SPY"
LOOKBACK = 5
DEFAULT_ROWS = 48
FEATURE_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]
MODEL_NAMES = Literal["gru", "lstm", "rnn"]

MODEL_PATHS = {
    "gru": MODEL_DIR / "gru.keras.zip",
    "lstm": MODEL_DIR / "lstm_financial_model.keras.zip",
    "rnn": MODEL_DIR / "stable_rnn_model.keras",
}

RESULTS_PATHS = {
    "gru": RESULTS_DIR / "gru.csv",
    "lstm": RESULTS_DIR / "lstm_final_results.csv",
    "rnn": RESULTS_DIR / "rnn_stable_results.csv",
}

app = FastAPI(title="MarketMind AI", version="2.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class PredictionRequest(BaseModel):
    features: Optional[list[list[float]]] = Field(
        default=None,
        description="Window of OHLCV rows. The latest 5 rows are used for prediction.",
    )


def _ensure_runtime_dir() -> Path:
    RUNTIME_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    return RUNTIME_MODEL_DIR


def _prepared_model_path(model_name: str) -> Path:
    source = MODEL_PATHS[model_name]
    if source.suffix == ".zip":
        target = _ensure_runtime_dir() / source.stem
        if not target.exists() or target.stat().st_mtime < source.stat().st_mtime:
            shutil.copyfile(source, target)
        return target
    return source


@lru_cache(maxsize=3)
def _load_model(model_name: str):
    path = _prepared_model_path(model_name)
    return keras.models.load_model(path, compile=False)


def _normalize_window(values: np.ndarray) -> np.ndarray:
    array = np.asarray(values, dtype=np.float32)
    if array.ndim != 2 or array.shape[1] != len(FEATURE_COLUMNS):
        raise HTTPException(
            status_code=400,
            detail=f"Expected a 2D window with {len(FEATURE_COLUMNS)} features.",
        )

    mean = array.mean(axis=0, keepdims=True)
    std = array.std(axis=0, keepdims=True)
    std[std == 0] = 1.0
    return (array - mean) / std


def _fetch_live_market_data(rows: int = DEFAULT_ROWS) -> pd.DataFrame:
    history = yf.download(
        MARKET_SYMBOL,
        period="7d",
        interval="1h",
        auto_adjust=True,
        progress=False,
        threads=False,
    )

    if history is None or history.empty:
        raise HTTPException(status_code=503, detail="Unable to fetch live market data right now.")

    history = history.reset_index()
    timestamp_col = "Datetime" if "Datetime" in history.columns else "Date"
    history = history.rename(columns={timestamp_col: "timestamp"})

    if isinstance(history.columns, pd.MultiIndex):
        history.columns = [col[0] if isinstance(col, tuple) else col for col in history.columns]

    history = history[["timestamp", "Open", "High", "Low", "Close", "Volume"]].copy()
    history["timestamp"] = pd.to_datetime(history["timestamp"], utc=True, errors="coerce")
    history = history.dropna(subset=["timestamp", "Open", "High", "Low", "Close"])
    history["Volume"] = pd.to_numeric(history["Volume"], errors="coerce").fillna(0)
    history = history.sort_values("timestamp").tail(rows).reset_index(drop=True)

    previous_close = history["Close"].shift(1)
    history["change_pct"] = ((history["Close"] - previous_close) / previous_close * 100).replace([np.inf, -np.inf], np.nan)
    history["change_pct"] = history["change_pct"].fillna(0.0)
    history["direction"] = (history["change_pct"] >= 0).astype(int)

    return history


def _records_for_frontend(df: pd.DataFrame) -> list[dict]:
    records: list[dict] = []
    for row in df.itertuples(index=False):
        records.append(
            {
                "timestamp": pd.Timestamp(row.timestamp).isoformat(),
                "Open": round(float(row.Open), 4),
                "High": round(float(row.High), 4),
                "Low": round(float(row.Low), 4),
                "Close": round(float(row.Close), 4),
                "Volume": int(float(row.Volume)),
                "change_pct": round(float(row.change_pct), 4),
                "direction": int(row.direction),
            }
        )
    return records


def _prepare_prediction_window(features: np.ndarray) -> np.ndarray:
    if features.shape[0] < LOOKBACK:
        raise HTTPException(status_code=400, detail=f"Need at least {LOOKBACK} rows of data for prediction.")
    window = features[-LOOKBACK:]
    return _normalize_window(window)


def _predict_direction(model_name: str, features: np.ndarray) -> dict:
    model = _load_model(model_name)
    prepared = _prepare_prediction_window(features)
    batch = np.expand_dims(prepared, axis=0)

    prediction = model.predict(batch, verbose=0)
    probability = float(np.squeeze(prediction))
    direction = "up" if probability >= 0.5 else "down"
    confidence = probability if direction == "up" else 1 - probability

    return {
        "model": model_name,
        "direction": direction,
        "probability_up": round(probability, 6),
        "confidence": round(confidence, 6),
        "lookback": LOOKBACK,
        "symbol": MARKET_SYMBOL,
        "timeframe": "1h",
    }


def _parse_metrics(model_name: str) -> dict:
    path = RESULTS_PATHS[model_name]
    if not path.exists():
        return {"model": model_name, "accuracy": None, "f1_score": None, "precision": None, "recall": None, "loss": None}

    try:
        df = pd.read_csv(path)
    except Exception:
        return {"model": model_name, "accuracy": None, "f1_score": None, "precision": None, "recall": None, "loss": None}

    last = df.iloc[-1].to_dict()

    accuracy = last.get("accuracy", last.get("val_accuracy"))
    if model_name == "gru" and pd.isna(accuracy):
        accuracy = df.get("val_accuracy", pd.Series(dtype=float)).dropna().max() if "val_accuracy" in df else None

    f1_score = last.get("f1_score")
    precision = last.get("precision")
    recall = last.get("recall")
    loss = last.get("loss", last.get("val_loss"))

    return {
        "model": model_name,
        "accuracy": None if pd.isna(accuracy) else round(float(accuracy), 4),
        "f1_score": None if pd.isna(f1_score) else round(float(f1_score), 4),
        "precision": None if pd.isna(precision) else round(float(precision), 4),
        "recall": None if pd.isna(recall) else round(float(recall), 4),
        "loss": None if pd.isna(loss) else round(float(loss), 4),
    }


@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(STATIC_DIR / "dashboard.html")


@app.get("/dashboard", response_class=FileResponse)
def dashboard():
    return FileResponse(STATIC_DIR / "dashboard.html")


@app.get("/api/latest")
def api_latest(model: MODEL_NAMES = Query("gru")):
    df = _fetch_live_market_data()
    records = _records_for_frontend(df)
    return records


@app.post("/api/predict")
def api_predict(payload: PredictionRequest, model: MODEL_NAMES = Query("gru")):
    if payload.features is None:
        df = _fetch_live_market_data(rows=max(DEFAULT_ROWS, LOOKBACK))
        features = df[FEATURE_COLUMNS].to_numpy(dtype=np.float32)
    else:
        features = np.asarray(payload.features, dtype=np.float32)

    return _predict_direction(model, features)


@app.get("/api/metrics")
def api_metrics(model: MODEL_NAMES = Query("gru")):
    return _parse_metrics(model)


@app.get("/health")
def health():
    return {"status": "ok", "models": list(MODEL_PATHS.keys()), "symbol": MARKET_SYMBOL, "timeframe": "1h"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
