# Results Directory

This directory stores the evaluation metrics and performance results for all trained models.

## Structure

```
results/
├── README.md                   # This file
├── rnn_results.csv            # RNN evaluation metrics
├── lstm_results.csv           # LSTM evaluation metrics
├── gru_results.csv            # GRU evaluation metrics
├── final_comparison.csv       # Combined comparison table
└── model_comparison_plot.png  # Visualization (optional)
```

## CSV Format

Each results file should follow this format:

### rnn_results.csv
```
metric,value
accuracy,0.85
f1_score,0.82
precision,0.88
recall,0.78
auc_roc,0.91
loss,0.38
```

### Sample Results File
```csv
metric,value,train_time_sec,model_size_kb
accuracy,0.85,245.3,156
f1_score,0.82,245.3,156
precision,0.88,245.3,156
recall,0.78,245.3,156
auc_roc,0.91,245.3,156
loss,0.38,245.3,156
```

## Required Metrics

Each model must evaluate on:

| Metric | Description | Formula | Range |
|--------|---|---|---|
| Accuracy | Percentage of correct predictions | (TP + TN) / Total | 0-1 |
| F1 Score | Harmonic mean of precision & recall | 2 * (P * R) / (P + R) | 0-1 |
| Precision | True positives out of predicted positives | TP / (TP + FP) | 0-1 |
| Recall | True positives out of actual positives | TP / (TP + FN) | 0-1 |
| AUC-ROC | Area under ROC curve | - | 0-1 |
| Loss | Binary cross-entropy loss | - | 0+ |

**Abbreviations:** TP=True Positive, TN=True Negative, FP=False Positive, FN=False Negative, P=Precision, R=Recall

## Python Code to Generate Results

### Using scikit-learn
```python
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, 
    recall_score, roc_auc_score
)

# Load data and model
X_test = np.load('/kaggle/input/financial-prediction-data/X_test.npy')
y_test = np.load('/kaggle/input/financial-prediction-data/y_test.npy')
model = tf.keras.models.load_model('lstm_model.h5')

# Get predictions
y_pred = model.predict(X_test)
y_pred_binary = np.round(y_pred).flatten()

# Calculate metrics
metrics = {
    'metric': ['accuracy', 'f1_score', 'precision', 'recall', 'auc_roc', 'loss'],
    'value': [
        accuracy_score(y_test, y_pred_binary),
        f1_score(y_test, y_pred_binary),
        precision_score(y_test, y_pred_binary, zero_division=0),
        recall_score(y_test, y_pred_binary, zero_division=0),
        roc_auc_score(y_test, y_pred),
        model.evaluate(X_test, y_test, verbose=0)[0]
    ]
}

# Save to CSV
results_df = pd.DataFrame(metrics)
results_df.to_csv('lstm_results.csv', index=False)
print(results_df)
```

## Comparison File

After all models are trained, create `final_comparison.csv`:

```csv
model,accuracy,f1_score,precision,recall,auc_roc,loss,train_time_sec
RNN,0.85,0.82,0.88,0.78,0.91,0.38,245
LSTM,0.82,0.80,0.85,0.76,0.88,0.42,315
GRU,0.88,0.85,0.90,0.81,0.93,0.36,280
```

### Python to Generate Comparison
```python
import pandas as pd

# Load individual results
rnn = pd.read_csv('rnn_results.csv')
lstm = pd.read_csv('lstm_results.csv')
gru = pd.read_csv('gru_results.csv')

# Create comparison
comparison = pd.DataFrame({
    'model': ['RNN', 'LSTM', 'GRU'],
    'accuracy': [rnn[rnn['metric']=='accuracy']['value'].values[0], ...],
    'f1_score': [...],
    # ... add other metrics
})

comparison.to_csv('final_comparison.csv', index=False)
print(comparison)
```

## Kaggle Notebook Output

When saving results from Kaggle notebook:

```python
# After evaluation
results_df.to_csv('/kaggle/working/lstm_results.csv', index=False)

# Download: Click "Output" tab → Download files
```

## How to Submit Results

### Step 1: Generate CSV
Run evaluation code in Kaggle notebook

### Step 2: Download File
1. Go to notebook → Output section
2. Download `.csv` file

### Step 3: Add to Repository
```bash
# For LSTM model by Friend 1
git checkout -b model-training/lstm-training
git pull origin model-training
cp ~/Downloads/lstm_results.csv results/
git add results/lstm_results.csv
git commit -m "Add: LSTM evaluation results"
git push origin model-training/lstm-training
```

### Step 4: Create Pull Request
1. Go to GitHub
2. Create PR from your branch to `model-training`
3. Include results summary in description

## Results Template for PR Description

```markdown
## LSTM Model Results

### Performance Metrics
- Accuracy: 82%
- F1-Score: 0.80
- Precision: 85%
- Recall: 76%
- AUC-ROC: 0.88

### Training Details
- Epochs: 50
- Batch Size: 8
- Loss: 0.42
- Training Time: ~315 seconds

### Architecture
- Input: (40, 5, 5)
- Layer 1: LSTM(64, activation='relu')
- Layer 2: Dense(32, activation='relu')
- Output: Dense(1, activation='sigmoid')

### Files Included
- results/lstm_results.csv - Metrics
- models/lstm_model.h5 - Trained model
- models/model_configs/lstm_config.json - Configuration
```

## Expected Performance

Based on similar financial prediction models:

| Model | Expected Accuracy | Expected F1 |
|---|---|---|
| RNN | 75-85% | 0.72-0.83 |
| LSTM | 78-88% | 0.75-0.86 |
| GRU | 76-86% | 0.73-0.84 |

*Actual results may vary based on implementation and hyperparameters*

## Column Standardization

Make sure column names are consistent:

✅ **Use these names:**
- `accuracy`
- `f1_score`
- `precision`
- `recall`
- `auc_roc`
- `loss`

❌ **Don't use these:**
- `Accuracy` (capital letters)
- `f1-score` (hyphens instead of underscores)
- `F1` (abbreviated)
- `accuracy_score` (different naming)

---

**Questions?** See [../DATASET_INFO.md](../DATASET_INFO.md) for data format or [../TEAM_COLLABORATION_GUIDE.py](../TEAM_COLLABORATION_GUIDE.py) for workflow.
