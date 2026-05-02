# Notebooks Directory

This directory contains the Kaggle notebook files used for model training and evaluation.

## Structure

```
notebooks/
├── README.md                   # This file
├── RNN_Training.ipynb         # RNN model notebook (Mudasar)
├── LSTM_Training.ipynb        # LSTM model notebook (Friend 1)
├── GRU_Training.ipynb         # GRU model notebook (Friend 2)
└── Example_Complete.ipynb     # Reference implementation (optional)
```

## Kaggle Notebook Links

Each team member should train their model on Kaggle:

### Team Member → Notebook Link Format
- **Mudasar (RNN):** https://www.kaggle.com/code/mudasarbhatti/rnn-training
- **Friend 1 (LSTM):** https://www.kaggle.com/code/{kaggle_username}/lstm-training
- **Friend 2 (GRU):** https://www.kaggle.com/code/{kaggle_username}/gru-training

## How to Create Kaggle Notebook

### Step 1: Go to Kaggle Code
1. Navigate to https://www.kaggle.com/code
2. Click "New Notebook"
3. Choose Python

### Step 2: Add Dataset
1. Click "Input" (left panel)
2. Search "financial-prediction-data"
3. Select the dataset

### Step 3: Enable GPU
1. Click "Settings" (⚙️ icon)
2. Set Accelerator to "GPU"
3. Save

### Step 4: Start Coding

Use the example structure below:

```python
# Cell 1: Import libraries
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, 
    recall_score, roc_auc_score
)

# Cell 2: Load data
X_train = np.load('/kaggle/input/financial-prediction-data/X_train.npy')
X_test = np.load('/kaggle/input/financial-prediction-data/X_test.npy')
y_train = np.load('/kaggle/input/financial-prediction-data/y_train.npy')
y_test = np.load('/kaggle/input/financial-prediction-data/y_test.npy')

print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")

# Cell 3: Build model
model = Sequential([
    LSTM(64, activation='relu', input_shape=(5, 5)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print(model.summary())

# Cell 4: Train model
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=8,
    validation_split=0.2,
    verbose=1
)

# Cell 5: Evaluate model
scores = model.evaluate(X_test, y_test, verbose=0)
print(f"Loss: {scores[0]:.4f}")
print(f"Accuracy: {scores[1]:.4f}")

# Cell 6: Calculate metrics
y_pred = model.predict(X_test)
y_pred_binary = np.round(y_pred).flatten()

metrics = {
    'metric': ['accuracy', 'f1_score', 'precision', 'recall', 'auc_roc', 'loss'],
    'value': [
        accuracy_score(y_test, y_pred_binary),
        f1_score(y_test, y_pred_binary),
        precision_score(y_test, y_pred_binary, zero_division=0),
        recall_score(y_test, y_pred_binary, zero_division=0),
        roc_auc_score(y_test, y_pred),
        scores[0]
    ]
}

results_df = pd.DataFrame(metrics)
print("\n=== FINAL RESULTS ===")
print(results_df)

# Cell 7: Save results and model
model.save('lstm_model.h5')
results_df.to_csv('lstm_results.csv', index=False)
print("\nFiles saved!")
```

## Notebook Template

### Complete Template Structure
```python
# ============================================================================
# FINANCIAL PREDICTION MODEL - LSTM TRAINING
# Team: Friend 1
# Dataset: https://www.kaggle.com/datasets/mudasarbhatti/financial-prediction-data
# ============================================================================

### 1. SETUP & IMPORTS
# - Import all necessary libraries
# - Display GPU status
# - Set random seeds for reproducibility

### 2. DATA LOADING
# - Load X_train, X_test, y_train, y_test
# - Print shapes and statistics
# - Display class distribution

### 3. EXPLORATORY ANALYSIS
# - Visualize data samples
# - Show feature distributions
# - Analyze class balance

### 4. MODEL ARCHITECTURE
# - Define LSTM/RNN/GRU model
# - Print model summary
# - Explain layer choices

### 5. TRAINING
# - Compile model
# - Train with validation split
# - Plot training history

### 6. EVALUATION
# - Make predictions on test set
# - Calculate all metrics
# - Display confusion matrix

### 7. RESULTS SUMMARY
# - Print performance metrics
# - Compare with expected performance
# - Save model and results

### 8. EXPORT
# - Save .h5 model file
# - Save results .csv file
# - Create config .json file
```

## Download and Save to Git

### Step 1: Download from Kaggle
1. Open your notebook
2. Click "File" → "Download notebook"
3. This downloads `.ipynb` file

### Step 2: Export Results
```bash
# After running notebook, download:
# - lstm_model.h5 (model)
# - lstm_results.csv (results)
```

### Step 3: Add to Repository
```bash
# For LSTM
git checkout -b model-training/lstm-training
cd notebooks
cp ~/Downloads/LSTM_Training.ipynb .
cd ../models
cp ~/Downloads/lstm_model.h5 .
cd ../results
cp ~/Downloads/lstm_results.csv .
git add ../notebooks/LSTM_Training.ipynb ../models/lstm_model.h5 ../results/lstm_results.csv
git commit -m "Add: LSTM training notebook and results"
git push origin model-training/lstm-training
```

## Expected Training Times

| Model | Dataset Size | GPU Type | Epochs | Estimated Time |
|---|---|---|---|---|
| RNN | 40 samples | Kaggle GPU | 50 | 2-3 min |
| LSTM | 40 samples | Kaggle GPU | 50 | 3-4 min |
| GRU | 40 samples | Kaggle GPU | 50 | 3-4 min |

*Times may vary based on Kaggle GPU availability*

## Common Issues & Solutions

### Issue: "No GPU detected"
**Solution:**
1. Go to Settings ⚙️
2. Set Accelerator to "GPU"
3. Restart kernel (Kernel → Restart)

### Issue: "Dataset not found"
**Solution:**
1. Click "Input" button (left sidebar)
2. Search "financial-prediction-data"
3. Add dataset to notebook

### Issue: "Module not found"
**Solution:** Run this in first cell:
```python
import sys
!pip install tensorflow scikit-learn --upgrade
```

### Issue: "Memory error"
**Solution:**
1. Reduce batch_size to 4
2. Reduce epochs to 25
3. Use simpler model (fewer units)

## Performance Tips

### To Improve Accuracy
- Increase epochs to 100
- Add more layers
- Use dropout for regularization
- Try different optimizers (adam, rmsprop)

### To Speed Up Training
- Reduce batch_size to 4
- Use fewer epochs (25)
- Simplify model architecture
- Enable GPU acceleration

### Example with Regularization
```python
from tensorflow.keras.layers import Dropout

model = Sequential([
    LSTM(64, activation='relu', input_shape=(5, 5), return_sequences=True),
    Dropout(0.2),
    LSTM(32, activation='relu'),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='sigmoid')
])
```

## Step-by-Step Workflow

1. **Create notebook** on Kaggle
2. **Add dataset** to inputs
3. **Enable GPU** in settings
4. **Copy code** from template
5. **Modify for your model type** (RNN/LSTM/GRU)
6. **Run all cells** (Cell → Run All)
7. **Download** `.ipynb`, `.h5`, `.csv` files
8. **Add to git** in models/ and results/ directories
9. **Commit** with message "Add: [MODEL] training notebook and results"
10. **Push** to `model-training/[model]-training` branch

## Example Output

After running a complete notebook, you should see:

```
X_train shape: (40, 5, 5)
X_test shape: (10, 5, 5)

Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 lstm (LSTM)                 (None, 64)                18048     
 dense (Dense)               (None, 32)                2080      
 dense_1 (Dense)             (None, 1)                 33        
=================================================================
Total params: 20,161
Trainable params: 20,161

Epoch 1/50
1/5 [=====>........................] - ETA: 2s - loss: 0.6931 - accuracy: 0.5000
2/5 [====>........................] - ETA: 0s - loss: 0.6847 - accuracy: 0.6875
...

Loss: 0.3841
Accuracy: 0.8500

=== FINAL RESULTS ===
           metric     value
0       accuracy  0.850000
1       f1_score  0.818182
2      precision  0.880000
3         recall  0.780000
4        auc_roc  0.910000
5           loss  0.384100

Files saved!
```

---

**Ready to train? Start at step 1 above!** 🚀
