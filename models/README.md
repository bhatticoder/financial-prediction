# Models Directory

This directory contains the trained machine learning models for financial market prediction.

## Structure

```
models/
├── README.md                    # This file
├── rnn_model.h5                # RNN trained model (Mudasar)
├── lstm_model.h5               # LSTM trained model (Friend 1)
├── gru_model.h5                # GRU trained model (Friend 2)
├── model_configs/
│   ├── rnn_config.json         # RNN architecture config
│   ├── lstm_config.json        # LSTM architecture config
│   └── gru_config.json         # GRU architecture config
└── model_summary.txt           # Architecture summaries for all models
```

## Team Members & Models

| Team Member | Model | File | Branch |
|---|---|---|---|
| Mudasar Bhatti | RNN | `rnn_model.h5` | `model-training/rnn-training` |
| Friend 1 | LSTM | `lstm_model.h5` | `model-training/lstm-training` |
| Friend 2 | GRU | `gru_model.h5` | `model-training/gru-training` |

## Model Files

### HDF5 Format (.h5)
- Complete model saved including weights and architecture
- Can be loaded directly: `model = tf.keras.models.load_model('rnn_model.h5')`

### Configuration Files (.json)
- Layer architecture details
- Hyperparameters used
- Training settings

Example:
```json
{
  "model_type": "RNN",
  "layers": [
    {"type": "SimpleRNN", "units": 64, "activation": "relu", "input_shape": [5, 5]},
    {"type": "Dense", "units": 32, "activation": "relu"},
    {"type": "Dense", "units": 1, "activation": "sigmoid"}
  ],
  "epochs": 50,
  "batch_size": 8,
  "optimizer": "adam",
  "loss": "binary_crossentropy"
}
```

## How to Use the Models

### Loading in Python
```python
import tensorflow as tf

# Load model
model = tf.keras.models.load_model('models/rnn_model.h5')

# Make predictions
predictions = model.predict(X_test)

# Get summary
model.summary()
```

### Comparing Models
```python
from tensorflow.keras.models import load_model
import pandas as pd

models = {
    'RNN': load_model('models/rnn_model.h5'),
    'LSTM': load_model('models/lstm_model.h5'),
    'GRU': load_model('models/gru_model.h5')
}

results = {}
for name, model in models.items():
    preds = model.predict(X_test)
    results[name] = evaluate_model(preds, y_test)

comparison_df = pd.DataFrame(results).T
print(comparison_df)
```

## Saving Steps (For Each Team Member)

After training on Kaggle:

1. **Download model from Kaggle**
   - Go to your notebook
   - Download the `.h5` file
   - Download the config `.json` file

2. **Add to repository**
   ```bash
   # For Friend 1 (LSTM)
   git checkout -b model-training/lstm-training
   cp /path/to/lstm_model.h5 models/
   cp /path/to/lstm_config.json models/model_configs/
   git add models/
   git commit -m "Add: LSTM trained model and config"
   git push origin model-training/lstm-training
   ```

3. **Create Pull Request**
   - Go to GitHub
   - Create PR from your branch to `model-training`
   - Add results summary in PR description

## Performance Metrics Storage

Results for each model are stored in `../results/` directory:
- `../results/rnn_results.csv` - RNN metrics
- `../results/lstm_results.csv` - LSTM metrics
- `../results/gru_results.csv` - GRU metrics

See [../results/README.md](../results/README.md) for format details.

## File Size Reference

| Model | Typical Size |
|---|---|
| RNN | 100-200 KB |
| LSTM | 120-250 KB |
| GRU | 110-230 KB |

*Sizes depend on number of layers and units*

---

**Note:** All models use the same input data format (40, 5, 5) with binary classification output.
