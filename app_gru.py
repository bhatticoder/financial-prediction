# app_gru.py - Enhanced API with GRU model support
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
import torch
import numpy as np
import os
import json
import pandas as pd
from pathlib import Path

# Import model classes
try:
    from models import GRUModel, LSTMModel, RNNModel
except ImportError:
    print("Warning: Could not import models directly")

app = FastAPI()

# Initialize models
models = {}
model_paths = {
    'gru': 'models/gru_best.pt',
    'lstm': 'models/lstm_best.pt',
    'rnn': 'models/rnn_best.pt'
}

# Load models if they exist
for model_name in ['gru', 'lstm', 'rnn']:
    try:
        if model_name == 'gru':
            models[model_name] = GRUModel(input_size=9)
        elif model_name == 'lstm':
            models[model_name] = LSTMModel(input_size=9)
        else:
            models[model_name] = RNNModel(input_size=9)
        
        if os.path.exists(model_paths[model_name]):
            models[model_name].load_state_dict(torch.load(model_paths[model_name]))
        models[model_name].eval()
        print(f"✓ {model_name.upper()} model loaded")
    except Exception as e:
        print(f"✗ Error loading {model_name}: {e}")

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serve the enhanced dashboard"""
    try:
        with open("static/dashboard.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Dashboard not found. Ensure static/dashboard.html exists.</h1>"

@app.get("/api/latest")
def get_latest(model: str = Query("gru", regex="^(gru|lstm|rnn)$")):
    """Get latest market data for specified model"""
    if os.path.exists("data/processed/timeseries.csv"):
        df = pd.read_csv("data/processed/timeseries.csv", index_col=0)
        df.index.name = "timestamp"
        return df.tail(50).reset_index().to_dict(orient="records")
    return {"error": "No data available"}

@app.get("/api/metrics")
def get_metrics(model: str = Query("gru", regex="^(gru|lstm|rnn)$")):
    """Get model performance metrics"""
    if os.path.exists("data/processed/metrics.json"):
        with open("data/processed/metrics.json", "r") as f:
            return json.load(f)
    return {"f1_score": "N/A", "rmse": "N/A"}

@app.post("/api/predict")
def predict(data: dict, model: str = Query("gru", regex="^(gru|lstm|rnn)$")):
    """Make prediction using specified model"""
    if model not in models:
        return {"error": f"Model {model} not available"}
    
    try:
        x = torch.tensor(data["features"], dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            output = models[model](x)
            prob = torch.sigmoid(output.squeeze()).item()
        
        direction = "up" if prob > 0.5 else "down"
        return {"direction": direction, "confidence": round(prob, 4), "model": model}
    except Exception as e:
        return {"error": str(e)}

# Legacy endpoints for backward compatibility
@app.get("/latest")
def get_latest_legacy():
    """Legacy endpoint - defaults to LSTM"""
    return get_latest(model="lstm")

@app.get("/metrics")
def get_metrics_legacy():
    """Legacy endpoint - returns general metrics"""
    return get_metrics()

@app.post("/predict")
def predict_legacy(data: dict):
    """Legacy endpoint - defaults to LSTM"""
    return predict(data, model="lstm")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
