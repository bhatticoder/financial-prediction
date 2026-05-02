"""
TRAINING YOUR MODELS ON KAGGLE (FREE GPU)
Complete Step-by-Step Guide
"""

def print_kaggle_guide():
    guide = """
╔════════════════════════════════════════════════════════════════════════════╗
║     TRAIN YOUR MODELS ON KAGGLE - FREE GPU - COMPLETE GUIDE               ║
╚════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHY KAGGLE?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ FREE GPU (NVIDIA Tesla T4 - 16GB VRAM)
✓ Unlimited Notebooks (Python, R, Julia)
✓ Pre-installed libraries (TensorFlow, PyTorch, Keras, etc.)
✓ No setup required
✓ Can download results back to your local machine
✓ Free tier: 30 hours/week GPU access

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: Prepare Your Local Data Files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your current files:
├─ data/X_train.npy         ✓ Ready
├─ data/X_test.npy          ✓ Ready
├─ data/y_train.npy         ✓ Ready
├─ data/y_test.npy          ✓ Ready
└─ data/prices_*.csv        ✓ Ready

All data is already prepared! ✓


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: Create Kaggle Account (Free)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to: https://www.kaggle.com
2. Click "Sign Up"
3. Use Google, GitHub, or email to register
4. NO CREDIT CARD REQUIRED ✓

Total time: 5 minutes


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: Create Kaggle Dataset (Upload Your Data)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option A: Using Web Interface (Easy)
────────────────────────────────────

1. Go to: https://www.kaggle.com/datasets/create/new
2. Click "Upload files"
3. Select these files from your machine:
   └─ Zip them first:
      • Go to: g:\\Fast\\Semester 6\\ANN Project\\data\\
      • Right-click → Send to → Compressed (zipped) folder
      • Name it: "financial-prediction-data.zip"
      
4. Upload the ZIP file
5. Fill in:
   ├─ Title: "Financial Market Prediction Dataset"
   ├─ Description: "Training data for RNN, LSTM, GRU models"
   ├─ Category: "Finance"
   └─ Make it: "Public" (so you can use it in notebooks)

6. Click "Create"
7. Wait for upload to complete (2-5 minutes)
8. Copy the dataset URL (e.g., https://www.kaggle.com/datasets/yourname/financial-prediction-data)

Total time: 10 minutes


Option B: Using Kaggle CLI (Advanced)
──────────────────────────────────────

1. Install Kaggle CLI:
   $ pip install kaggle

2. Get API token from: https://www.kaggle.com/settings/account
   └─ Click "Create New API Token"
   └─ This downloads kaggle.json

3. Place kaggle.json in: C:\\Users\\YourUsername\\.kaggle\\

4. In your project directory, create dataset-metadata.json:

   {
     "id": "bhatticoder/financial-prediction-data",
     "title": "Financial Market Prediction Dataset",
     "code_license": "CC0",
     "dataset_type": "other",
     "is_private": false
   }

5. Upload:
   $ kaggle datasets create -p ./data


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4: Create Kaggle Notebook & Train Models
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to Kaggle home: https://www.kaggle.com
2. Click "Code" → "Create a notebook"
3. Name it: "Financial Prediction - Train Models"
4. Select Language: Python
5. Click "Create notebook"

Your notebook is ready! ✓


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5: Copy This Code Into Your Kaggle Notebook
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cell 1: Setup & Import
──────────────────────

# Mount Kaggle Dataset
import os
from pathlib import Path

# Check if data is available
data_dir = '/kaggle/input/financial-prediction-data'
# OR if you uploaded as ZIP:
# import zipfile
# with zipfile.ZipFile('/kaggle/input/financial-prediction-data/financial-prediction-data.zip', 'r') as zip_ref:
#     zip_ref.extractall('/tmp/data')
# data_dir = '/tmp/data'

print("Available files in dataset:")
print(os.listdir(data_dir))


Cell 2: Load Data
─────────────────

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Load your prepared data
X_train = np.load(f'{data_dir}/X_train.npy')
X_test = np.load(f'{data_dir}/X_test.npy')
y_train = np.load(f'{data_dir}/y_train.npy')
y_test = np.load(f'{data_dir}/y_test.npy')

print(f"✓ Data loaded successfully!")
print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"y_test shape: {y_test.shape}")


Cell 3: Verify GPU
──────────────────

import tensorflow as tf

print("GPU Available:", tf.test.is_built_with_cuda())
print("GPU Devices:", tf.config.list_physical_devices('GPU'))

# Force GPU Usage
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"✓ GPU configured successfully!")
    except RuntimeError as e:
        print(f"Error setting memory growth: {e}")


Cell 4: Build Models
────────────────────

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, LSTM, GRU, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# 1. RNN MODEL
rnn_model = Sequential([
    SimpleRNN(64, activation='relu', input_shape=(5, 5), return_sequences=False),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

rnn_model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("✓ RNN Model Built")


# 2. LSTM MODEL
lstm_model = Sequential([
    LSTM(64, activation='relu', input_shape=(5, 5), return_sequences=True),
    Dropout(0.2),
    LSTM(32, activation='relu', return_sequences=False),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

lstm_model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("✓ LSTM Model Built")


# 3. GRU MODEL
gru_model = Sequential([
    GRU(64, activation='relu', input_shape=(5, 5), return_sequences=True),
    Dropout(0.2),
    GRU(32, activation='relu', return_sequences=False),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

gru_model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("✓ GRU Model Built")


Cell 5: Train All Models
────────────────────────

import time

results = {}
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

models = {
    'RNN': rnn_model,
    'LSTM': lstm_model,
    'GRU': gru_model
}

for model_name, model in models.items():
    print(f"\n{'='*60}")
    print(f"Training {model_name} Model...")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    history = model.fit(
        X_train, y_train,
        epochs=100,
        batch_size=8,
        validation_split=0.2,
        callbacks=[early_stop],
        verbose=1
    )
    
    training_time = time.time() - start_time
    
    print(f"\n✓ {model_name} training completed in {training_time:.2f} seconds")
    
    results[model_name] = {
        'model': model,
        'history': history,
        'training_time': training_time
    }


Cell 6: Evaluate All Models
───────────────────────────

print("\n" + "="*60)
print("MODEL EVALUATION RESULTS")
print("="*60)

evaluation_results = {}

for model_name, result_dict in results.items():
    model = result_dict['model']
    
    print(f"\n{model_name} Model:")
    print("-" * 40)
    
    # Make predictions
    y_pred_proba = model.predict(X_test)
    y_pred = (y_pred_proba > 0.5).astype(int).flatten()
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    
    evaluation_results[model_name] = {
        'accuracy': accuracy,
        'f1_score': f1,
        'precision': precision,
        'recall': recall,
        'confusion_matrix': cm,
        'predictions': y_pred
    }
    
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"Confusion Matrix:\\n{cm}")


Cell 7: Create Comparison Table
───────────────────────────────

import pandas as pd

# Create DataFrame
comparison_df = pd.DataFrame({
    'Model': list(evaluation_results.keys()),
    'Accuracy': [evaluation_results[m]['accuracy'] for m in evaluation_results.keys()],
    'F1-Score': [evaluation_results[m]['f1_score'] for m in evaluation_results.keys()],
    'Precision': [evaluation_results[m]['precision'] for m in evaluation_results.keys()],
    'Recall': [evaluation_results[m]['recall'] for m in evaluation_results.keys()]
})

print("\n" + "="*60)
print("MODEL COMPARISON TABLE")
print("="*60)
print(comparison_df.to_string(index=False))

# Find best model
best_model_name = comparison_df.loc[comparison_df['F1-Score'].idxmax(), 'Model']
print(f"\n🏆 BEST MODEL: {best_model_name}")

# Save comparison to CSV
comparison_df.to_csv('/kaggle/working/model_comparison.csv', index=False)
print("✓ Saved to model_comparison.csv")


Cell 8: Save Models & Results
─────────────────────────────

# Save trained models
for model_name, result_dict in results.items():
    model = result_dict['model']
    model.save(f'/kaggle/working/{model_name}_model.h5')
    print(f"✓ Saved {model_name} model")

# Save results as JSON
import json

results_json = {
    model_name: {
        'accuracy': float(evaluation_results[model_name]['accuracy']),
        'f1_score': float(evaluation_results[model_name]['f1_score']),
        'precision': float(evaluation_results[model_name]['precision']),
        'recall': float(evaluation_results[model_name]['recall']),
        'training_time': results[model_name]['training_time']
    }
    for model_name in results.keys()
}

with open('/kaggle/working/model_results.json', 'w') as f:
    json.dump(results_json, f, indent=2)

print("✓ Results saved!")


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 6: Run Your Notebook
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Copy all cells above into your Kaggle notebook
2. In your notebook settings (gear icon):
   ├─ Accelerator: GPU (Select T4 GPU)
   ├─ Internet: Enable internet (for pip installs)
   └─ Click Save

3. Run all cells: Click "Run All" button
4. Wait for training to complete (~5-10 minutes total)

Expected Output:
- Training logs for each model
- Accuracy, F1-Score, etc.
- Model comparison table
- ✓ Trained models saved
- ✓ Results saved to CSV & JSON


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 7: Download Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After training completes:

1. Click "Output" folder (bottom left)
2. Download these files:
   ├─ model_comparison.csv        ← FOR YOUR REPORT!
   ├─ model_results.json
   ├─ RNN_model.h5
   ├─ LSTM_model.h5
   └─ GRU_model.h5

3. Move downloaded files to your local folder:
   └─ g:\\Fast\\Semester 6\\ANN Project\\results\\


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 8: Push Results to GitHub
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. In your local terminal:
   $ cd "g:\\Fast\\Semester 6\\ANN Project"
   
2. Add the downloaded results:
   $ git add results/
   $ git add models/
   
3. Commit:
   $ git commit -m "Add trained models (RNN, LSTM, GRU) and results"
   
4. Push:
   $ git push origin main

5. Your GitHub now has:
   ✓ Training code
   ✓ Results table (model_comparison.csv)
   ✓ Trained models (.h5 files)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPLETE WORKFLOW SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Timeline:
├─ Step 1-2: Prepare data (DONE) ............................ ✓
├─ Step 3: Create Kaggle account ........................... 5 min
├─ Step 4: Upload dataset to Kaggle ........................ 10 min
├─ Step 5: Create Kaggle notebook .......................... 2 min
├─ Step 6: Run notebook (GPU Training) ..................... 10 min
├─ Step 7: Download results ................................ 2 min
├─ Step 8: Push to GitHub .................................. 3 min
└─ TOTAL: ~35 minutes to get results!

Output you'll have:
✓ model_comparison.csv     ← For your IEEE report
✓ Trained models (.h5)     ← For deployment (if needed)
✓ JSON results             ← Raw data
✓ GitHub commits           ← Shows progress


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMPORTANT NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Kaggle GPU Training Benefits:
  ├─ Much faster than CPU (~10x)
  ├─ FREE - No credit card needed
  ├─ Pre-installed libraries
  ├─ Results can be downloaded
  ├─ Can make notebook public (shows your work)
  └─ Great for portfolio!

⚠️  Kaggle Limits:
  ├─ 30 hours/week GPU usage (plenty for this project)
  ├─ Needs internet connection
  ├─ Public notebooks show your code
  └─ Session timeout after 1 hour of inactivity

💡 Pro Tips:
  ├─ Save model frequently (checkpoints)
  ├─ Use early stopping to prevent overfitting
  ├─ Monitor GPU usage in notebook settings
  ├─ Make notebook private during development
  └─ Publish after completion for portfolio


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Questions? 
• Kaggle Docs: https://www.kaggle.com/docs
• TensorFlow GPU: https://www.tensorflow.org/guide/gpu
• Kaggle Community: https://www.kaggle.com/discussion

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready? Start with: https://www.kaggle.com/signup

Good luck! 🚀
    """
    print(guide)

if __name__ == "__main__":
    print_kaggle_guide()
