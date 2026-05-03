# Model Training Branch

## Shared Kaggle Dataset
**🔗 Dataset Link:** https://www.kaggle.com/datasets/mudasarbhatti/financial-prediction-data

All team members use this same dataset for training their models.

---

## Team Members & Models

| Member | Model | Status |
|--------|-------|--------|
| Mudasar Bhatti | RNN | Training |
| Friend 1 | LSTM | Pending |
| Friend 2 | GRU | Pending |

---

## How to Train Your Model

### Step 1: Access the Dataset
Visit: https://www.kaggle.com/datasets/mudasarbhatti/financial-prediction-data

### Step 2: Create Kaggle Notebook
1. Go to https://www.kaggle.com/code
2. Click "New Notebook"
3. Name it: `[YourName] - [ModelType] Training`
4. Click "Add Input" and select `financial-prediction-data`
5. Enable GPU: Settings → Accelerator → GPU

### Step 3: Load Data
```python
import numpy as np

X_train = np.load('/kaggle/input/financial-prediction-data/X_train.npy')
X_test = np.load('/kaggle/input/financial-prediction-data/X_test.npy')
y_train = np.load('/kaggle/input/financial-prediction-data/y_train.npy')
y_test = np.load('/kaggle/input/financial-prediction-data/y_test.npy')

print(f"X_train shape: {X_train.shape}")  # (40, 5, 5)
print(f"X_test shape: {X_test.shape}")    # (10, 5, 5)
```

### Step 4: Train Your Model
Write your own model code (RNN, LSTM, or GRU)

### Step 5: Save Results
```python
import pandas as pd

results = {
    'model': 'LSTM',  # or RNN, GRU
    'accuracy': accuracy,
    'f1_score': f1,
    'precision': precision,
    'recall': recall,
    'trained_by': 'Your Name'
}

results_df = pd.DataFrame([results])
results_df.to_csv('model_results.csv', index=False)
```

### Step 6: Download Files
- Download your notebook
- Download `model_results.csv`

### Step 7: Push to GitHub
```bash
# Clone/checkout model-training
git checkout model-training
git checkout -b model-training/[your-model]-training

# Add your files
cp ~/Downloads/[notebook].ipynb notebooks/
cp ~/Downloads/model_results.csv results/

# Push
git add .
git commit -m "Add [MODEL] model training and results"
git push origin model-training/[your-model]-training
```

### Step 8: Create Pull Request
Go to GitHub → Create PR from `model-training/[your-model]-training` → `model-training`

---

## Results Directory

```
results/
├── rnn_results.csv
├── lstm_results.csv
└── gru_results.csv
```

Each CSV should contain:
- model
- accuracy
- f1_score
- precision
- recall
- trained_by

---

## Models Directory

```
models/
├── rnn_model.py
├── lstm_model.py
└── gru_model.py
```

Pure Python implementations (optional if sharing Kaggle notebooks)

---

## Notebooks Directory

```
notebooks/
├── RNN_Training.ipynb
├── LSTM_Training.ipynb
└── GRU_Training.ipynb
```

Kaggle notebooks (after training)

---

## Final Output

After all 3 models are trained:
- `final_comparison.csv` - Combined results from all models
- Ready for IEEE report

---

## Questions?

1. Can't access Kaggle dataset? 
   → Make sure it's set to Public
   → Try: https://www.kaggle.com/datasets/mudasarbhatti/financial-prediction-data

2. Data loading issues?
   → Check the DATASET_INFO.md for exact paths
   → Verify you added the dataset as input in your notebook

3. Git issues?
   → See TEAM_COLLABORATION_GUIDE.py for detailed commands

---

**Let's go! 🚀**
