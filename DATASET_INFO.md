# Dataset Information

## Kaggle Dataset Link
🔗 **https://www.kaggle.com/datasets/mudasarbhatti/financial-prediction-data**

---

## Data Format

### File Sizes
- X_train.npy: ~16 KB
- X_test.npy: ~4 KB
- y_train.npy: ~0.4 KB
- y_test.npy: ~0.08 KB

### Array Shapes
```
X_train.npy : (40, 5, 5)   # 40 samples, 5 timesteps, 5 features
X_test.npy  : (10, 5, 5)   # 10 samples, 5 timesteps, 5 features
y_train.npy : (40,)        # 40 binary labels
y_test.npy  : (10,)        # 10 binary labels
```

---

## Features (5 per timestep)

1. **Open** - Opening price of the day
2. **High** - Highest price reached
3. **Low** - Lowest price reached
4. **Close** - Closing price
5. **Volume** - Trading volume

All features are **Z-score normalized** (mean=0, std=1)

---

## Target Variable

**Binary Classification:**
- **1** = Price goes UP next day ✓
- **0** = Price goes DOWN next day ✗

### Class Distribution
- Positive (up): 32 samples (64%)
- Negative (down): 23 samples (36%)
- Slightly imbalanced dataset

---

## Data Source

- **Source:** Yahoo Finance API
- **Assets:** 
  - Gold futures (GC=F)
  - S&P 500 (^GSPC)
- **Period:** Last 30 days
- **Total Records:** 55 daily price points

---

## Preprocessing Applied

1. **Downloaded daily OHLCV data** from Yahoo Finance
2. **Created sequences** with 5-day sliding window
3. **Target variable** = Next day direction (up/down)
4. **Normalization** using Z-score
5. **Train/Test Split** = 80/20 (temporal order preserved)

---

## How to Load in Kaggle Notebook

### Basic Loading
```python
import numpy as np

# Path in Kaggle
data_path = '/kaggle/input/financial-prediction-data/'

# Load all files
X_train = np.load(data_path + 'X_train.npy')
X_test = np.load(data_path + 'X_test.npy')
y_train = np.load(data_path + 'y_train.npy')
y_test = np.load(data_path + 'y_test.npy')

print(f"X_train: {X_train.shape}")
print(f"X_test: {X_test.shape}")
print(f"y_train: {y_train.shape}")
print(f"y_test: {y_test.shape}")
```

### With TensorFlow
```python
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Load data
X_train = np.load('/kaggle/input/financial-prediction-data/X_train.npy')
X_test = np.load('/kaggle/input/financial-prediction-data/X_test.npy')
y_train = np.load('/kaggle/input/financial-prediction-data/y_train.npy')
y_test = np.load('/kaggle/input/financial-prediction-data/y_test.npy')

# Build model
model = Sequential([
    LSTM(64, activation='relu', input_shape=(5, 5)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train
model.fit(X_train, y_train, epochs=50, batch_size=8, validation_split=0.2)

# Evaluate
from sklearn.metrics import accuracy_score, f1_score
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred.round())}")
print(f"F1-Score: {f1_score(y_test, y_pred.round())}")
```

---

## Key Statistics

| Metric | Value |
|--------|-------|
| Total Samples | 50 (40 train + 10 test) |
| Sequence Length | 5 timesteps |
| Features | 5 (OHLCV) |
| Target Classes | 2 (Binary) |
| Train/Test Ratio | 80/20 |
| Positive Class Ratio | 64% |
| Negative Class Ratio | 36% |

---

## Data Leakage Prevention

✅ **Temporal Split** - Train and test data are temporally separated
✅ **No Leakage** - Test data comes after train data chronologically
✅ **Fair Evaluation** - Models haven't seen test data during training

---

## Important Notes

1. **Small Dataset** - Only 50 sequences total (limited training data)
2. **Class Imbalance** - More positive samples (64%) than negative (36%)
3. **Normalized Features** - Already Z-score normalized, no scaling needed
4. **Binary Classification** - Not regression, use sigmoid activation in output layer

---

## Usage Examples

### RNN Model
```python
from tensorflow.keras.layers import SimpleRNN

model = Sequential([
    SimpleRNN(64, activation='relu', input_shape=(5, 5)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
```

### LSTM Model
```python
from tensorflow.keras.layers import LSTM

model = Sequential([
    LSTM(64, activation='relu', input_shape=(5, 5)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
```

### GRU Model
```python
from tensorflow.keras.layers import GRU

model = Sequential([
    GRU(64, activation='relu', input_shape=(5, 5)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
```

---

## Troubleshooting

### Issue: File not found
```
FileNotFoundError: '/kaggle/input/financial-prediction-data/X_train.npy'
```
**Solution:** In Kaggle notebook, make sure you added the dataset as input

### Issue: Wrong shape
```
Expected (40, 5, 5) but got (40, 5)
```
**Solution:** Check that you're loading the correct .npy file

### Issue: GPU not detected
```
No GPU detected
```
**Solution:** Go to notebook Settings → Accelerator → GPU

---

## Questions?

- **Dataset not public?** → Check Kaggle dataset visibility settings
- **Can't add dataset?** → Try refreshing the Kaggle page
- **Data format issues?** → See code examples above

---

**Happy Training! 🚀**
