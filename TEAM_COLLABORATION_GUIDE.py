"""
TEAM COLLABORATION GUIDE
Model Training Branch Setup
"""

SETUP_INSTRUCTIONS = """
╔════════════════════════════════════════════════════════════════════════════╗
║              TEAM MODEL TRAINING - COLLABORATION SETUP                     ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 OBJECTIVE:
All team members train models in a shared "model-training" branch using the 
same dataset from Kaggle.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SHARED KAGGLE DATASET:
https://www.kaggle.com/datasets/mudasarbhatti/financial-prediction-data

Data Files Available:
✓ X_train.npy (40 sequences)
✓ X_test.npy (10 sequences)
✓ y_train.npy (40 targets)
✓ y_test.npy (10 targets)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 SETUP (DO THIS FIRST - MUDASAR):

1. Create "model-training" branch locally:
   $ git checkout -b model-training

2. Create this folder structure:
   ```
   model-training/
   ├── README.md (with dataset link)
   ├── DATASET_INFO.md
   ├── models/
   │   ├── rnn_model.py
   │   ├── lstm_model.py
   │   └── gru_model.py
   ├── results/
   │   ├── rnn_results.csv
   │   ├── lstm_results.csv
   │   └── gru_results.csv
   └── notebooks/
       ├── RNN_Training.ipynb
       ├── LSTM_Training.ipynb
       └── GRU_Training.ipynb
   ```

3. Create README.md:
   ```markdown
   # Model Training Branch
   
   ## Shared Dataset
   **Kaggle Dataset:** https://www.kaggle.com/datasets/mudasarbhatti/financial-prediction-data
   
   ## Team Members & Models
   - Mudasar Bhatti: RNN Model
   - Friend 1: LSTM Model
   - Friend 2: GRU Model
   
   ## How to Train Your Model
   1. Create Kaggle notebook
   2. Add dataset from URL above
   3. Load data from:
      /kaggle/input/financial-prediction-data/
   4. Train your model
   5. Download code & results
   6. Push to this branch
   
   ## Results
   - All results saved in results/
   - Models code in models/
   - Final comparison: final_comparison.csv
   ```

4. Create DATASET_INFO.md:
   ```markdown
   # Dataset Information
   
   ## Kaggle Dataset Link
   https://www.kaggle.com/datasets/mudasarbhatti/financial-prediction-data
   
   ## Data Format
   - X_train.npy: Shape (40, 5, 5) - 40 samples, 5 timesteps, 5 features
   - X_test.npy: Shape (10, 5, 5)
   - y_train.npy: Shape (40,) - binary targets
   - y_test.npy: Shape (10,)
   
   ## Features
   1. Open price
   2. High price
   3. Low price
   4. Close price
   5. Volume
   
   ## Loading Data in Kaggle Notebook
   ```python
   import numpy as np
   X_train = np.load('/kaggle/input/financial-prediction-data/X_train.npy')
   X_test = np.load('/kaggle/input/financial-prediction-data/X_test.npy')
   y_train = np.load('/kaggle/input/financial-prediction-data/y_train.npy')
   y_test = np.load('/kaggle/input/financial-prediction-data/y_test.npy')
   ```
   
   ## Class Distribution
   - Positive (price up): 32 samples (64%)
   - Negative (price down): 23 samples (36%)
   ```

5. Push to GitHub:
   $ git add .
   $ git commit -m "Setup: Create model-training branch structure with dataset link"
   $ git push origin model-training

6. Go to GitHub → Create Pull Request (model-training → main)
   Leave it OPEN for team to see

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FOR EACH TEAM MEMBER (Friends 1 & 2):

1. Clone the repository:
   $ git clone https://github.com/yourusername/financial-prediction.git
   $ cd financial-prediction

2. Switch to model-training branch:
   $ git checkout model-training

3. Create sub-branch for your model:
   $ git checkout -b model-training/lstm-training  # Friend 1
   $ git checkout -b model-training/gru-training   # Friend 2
   $ git checkout -b model-training/rnn-training   # You

4. See the dataset link:
   $ cat DATASET_INFO.md  # Shows Kaggle dataset URL

5. Go to Kaggle and create notebook:
   - Visit https://www.kaggle.com/code
   - New Notebook
   - Add the dataset: financial-prediction-data
   - Enable GPU
   - Copy code in models/*.py
   - Modify for your model type
   - Train and save results

6. Download your Kaggle files:
   - notebook_name.ipynb (Kaggle notebook)
   - your_model_results.csv (results)

7. Add to your local branch:
   $ cp ~/Downloads/LSTM_Training.ipynb notebooks/
   $ cp ~/Downloads/lstm_results.csv results/
   
   $ git add notebooks/ results/
   $ git commit -m "Add LSTM model training notebook and results"
   $ git push origin model-training/lstm-training

8. Go to GitHub → Create Pull Request:
   - From: model-training/lstm-training
   - To: model-training (NOT main!)
   - Add description of your results

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FINAL STEP (After all 3 models trained):

1. Someone merges all PRs into model-training
2. Create final_comparison.csv:
   $ python combine_results.py

3. Merge model-training → main (final PR)

4. Final structure in main branch:
   ```
   financial-prediction/
   ├── data/ (original data collection)
   ├── models/ (all 3 trained models)
   ├── results/ (all 3 results CSVs)
   ├── notebooks/ (all 3 Kaggle notebooks)
   ├── final_comparison.csv
   └── README.md
   ```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 CHECKLIST FOR EACH PERSON:

Mudasar (RNN):
□ Create model-training branch with structure
□ Add README.md with dataset link
□ Add DATASET_INFO.md
□ Push to GitHub
□ Train RNN on Kaggle using shared dataset
□ Download notebook & results.csv
□ Push to model-training/rnn-training
□ Create PR to model-training branch

Friend 1 (LSTM):
□ Clone repo and checkout model-training
□ See dataset info in DATASET_INFO.md
□ Visit: https://www.kaggle.com/datasets/mudasarbhatti/financial-prediction-data
□ Create Kaggle notebook
□ Train LSTM using shared dataset
□ Download notebook & results.csv
□ Push to model-training/lstm-training branch
□ Create PR to model-training branch

Friend 2 (GRU):
□ Clone repo and checkout model-training
□ See dataset info in DATASET_INFO.md
□ Visit: https://www.kaggle.com/datasets/mudasarbhatti/financial-prediction-data
□ Create Kaggle notebook
□ Train GRU using shared dataset
□ Download notebook & results.csv
□ Push to model-training/gru-training branch
□ Create PR to model-training branch

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMMAND SUMMARY:

# Setup (Mudasar)
git checkout -b model-training
mkdir -p models results notebooks
# Create README.md and DATASET_INFO.md with content above
git add .
git commit -m "Setup: Model training branch with dataset link"
git push origin model-training

# Each Friend
git clone https://github.com/yourusername/financial-prediction.git
git checkout model-training
git checkout -b model-training/lstm-training
# (do kaggle training)
git add notebooks/ results/
git commit -m "Add LSTM training notebook and results"
git push origin model-training/lstm-training
# Create PR on GitHub from model-training/lstm-training → model-training

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ READY? Share this guide with your friends and start training!

Dataset Link: https://www.kaggle.com/datasets/mudasarbhatti/financial-prediction-data
"""

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)
