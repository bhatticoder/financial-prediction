import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ==============================================================================
# 1. DATA PIPELINE ARCHITECTURE
# ==============================================================================
def create_data_pipeline():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis('off')
    
    # Define stages
    stages = [
        ("Yahoo Finance\nAPI", 0.5, 1.5, '#FF6B6B'),
        ("Raw OHLCV\nData", 1.5, 1.5, '#4ECDC4'),
        ("Validation &\nCleaning", 2.5, 1.5, '#45B7D1'),
        ("Feature\nSelection", 3.5, 1.5, '#FFA07A'),
        ("Sliding Window\nGeneration", 4.5, 1.5, '#98D8C8'),
        ("Z-Score\nNormalization", 5.5, 1.5, '#F7DC6F'),
        ("Add Target\nLabels", 6.5, 1.5, '#BB8FCE'),
        ("Training\nSequences", 7.5, 1.5, '#85C1E2'),
        ("Model Input\n(5×5)", 8.5, 1.5, '#F8B88B')
    ]
    
    # Draw boxes and arrows
    for i, (label, x, y, color) in enumerate(stages):
        box = FancyBboxPatch((x-0.35, y-0.35), 0.7, 0.7, 
                            boxstyle="round,pad=0.05", 
                            edgecolor='black', facecolor=color, linewidth=2, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Draw arrows between stages
        if i < len(stages) - 1:
            arrow = FancyArrowPatch((x+0.35, y), (stages[i+1][1]-0.35, stages[i+1][2]),
                                  arrowstyle='->', mutation_scale=20, linewidth=2, color='black')
            ax.add_patch(arrow)
    
    ax.set_title('Data Pipeline Architecture', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('figures/data_pipeline.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ data_pipeline.png created")
    plt.close()

# ==============================================================================
# 2. MODEL TRAINING PIPELINE
# ==============================================================================
def create_training_pipeline():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    
    # Top section
    box = FancyBboxPatch((3.5, 6), 3, 0.6, boxstyle="round,pad=0.05",
                        edgecolor='black', facecolor='#90EE90', linewidth=2)
    ax.add_patch(box)
    ax.text(5, 6.3, 'Preprocessed Sequences', ha='center', va='center', 
            fontsize=10, fontweight='bold')
    
    # Arrow down
    arrow = FancyArrowPatch((5, 6), (5, 5.4), arrowstyle='->', mutation_scale=20, linewidth=2)
    ax.add_patch(arrow)
    
    # Train/Test Split
    box = FancyBboxPatch((3.5, 4.8), 3, 0.6, boxstyle="round,pad=0.05",
                        edgecolor='black', facecolor='#87CEEB', linewidth=2)
    ax.add_patch(box)
    ax.text(5, 5.1, 'Train/Test Split (80/20)', ha='center', va='center',
            fontsize=10, fontweight='bold')
    
    # Split arrows
    arrow1 = FancyArrowPatch((4, 4.8), (2.5, 4), arrowstyle='->', mutation_scale=20, linewidth=2)
    arrow2 = FancyArrowPatch((6, 4.8), (7.5, 4), arrowstyle='->', mutation_scale=20, linewidth=2)
    ax.add_patch(arrow1)
    ax.add_patch(arrow2)
    
    # Training Data and Test Data
    box1 = FancyBboxPatch((1, 3.4), 3, 0.6, boxstyle="round,pad=0.05",
                         edgecolor='black', facecolor='#FFB6C1', linewidth=2)
    box2 = FancyBboxPatch((6, 3.4), 3, 0.6, boxstyle="round,pad=0.05",
                         edgecolor='black', facecolor='#FFB6C1', linewidth=2)
    ax.add_patch(box1)
    ax.add_patch(box2)
    ax.text(2.5, 3.7, 'Training Data', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(7.5, 3.7, 'Test Data', ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Train from training data
    arrow = FancyArrowPatch((2.5, 3.4), (2.5, 2.8), arrowstyle='->', mutation_scale=20, linewidth=2)
    ax.add_patch(arrow)
    
    # Three model trainers
    models = [
        ("RNN\nTrainer", 0.5, 2.2, '#FF6B6B'),
        ("LSTM\nTrainer", 2.5, 2.2, '#4ECDC4'),
        ("GRU\nTrainer", 4.5, 2.2, '#45B7D1')
    ]
    
    for label, x, y, color in models:
        box = FancyBboxPatch((x-0.5, y-0.4), 1, 0.8, boxstyle="round,pad=0.05",
                            edgecolor='black', facecolor=color, linewidth=2, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Arrow to trained models
        arrow = FancyArrowPatch((x, y-0.4), (x, 1.2), arrowstyle='->', mutation_scale=15, linewidth=2)
        ax.add_patch(arrow)
    
    # Trained models
    trained = [
        ("RNN\nTrained", 0.5, 0.8),
        ("LSTM\nTrained", 2.5, 0.8),
        ("GRU\nTrained", 4.5, 0.8)
    ]
    
    for label, x, y in trained:
        box = FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6, boxstyle="round,pad=0.05",
                            edgecolor='black', facecolor='#F7DC6F', linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=7, fontweight='bold')
        
        # Arrow to evaluation
        arrow = FancyArrowPatch((x, y-0.3), (6.5, 1.5), arrowstyle='->', mutation_scale=15, linewidth=1.5, alpha=0.6)
        ax.add_patch(arrow)
    
    # Test data arrow to evaluation
    arrow = FancyArrowPatch((7.5, 3.4), (6.5, 1.8), arrowstyle='->', mutation_scale=20, linewidth=2)
    ax.add_patch(arrow)
    
    # Evaluation box
    box = FancyBboxPatch((6, 1.2), 3, 0.6, boxstyle="round,pad=0.05",
                        edgecolor='black', facecolor='#85C1E2', linewidth=2)
    ax.add_patch(box)
    ax.text(7.5, 1.5, 'Evaluation & Metrics', ha='center', va='center',
            fontsize=10, fontweight='bold')
    
    ax.set_title('Model Training Pipeline', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('figures/training_pipeline.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ training_pipeline.png created")
    plt.close()

# ==============================================================================
# 3. INFERENCE SYSTEM ARCHITECTURE
# ==============================================================================
def create_inference_pipeline():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis('off')
    
    stages = [
        ("Live Market\nData (SPY 1H)", 0.5, 1.5, '#90EE90'),
        ("Fetch Latest\n5 Candles", 1.5, 1.5, '#FFB6C1'),
        ("Normalize\nWindow", 2.5, 1.5, '#87CEEB'),
        ("Select\nModel", 3.5, 1.5, '#FFA07A'),
        ("Load Model\n(GRU/LSTM/RNN)", 4.5, 1.5, '#98D8C8'),
        ("Run\nInference", 5.5, 1.5, '#F7DC6F'),
        ("Get Prediction\n+ Confidence", 6.5, 1.5, '#BB8FCE'),
        ("Display in\nDashboard", 7.5, 1.5, '#85C1E2'),
        ("Web Browser\nlocalhost:8000", 8.5, 1.5, '#F8B88B')
    ]
    
    for i, (label, x, y, color) in enumerate(stages):
        box = FancyBboxPatch((x-0.35, y-0.35), 0.7, 0.7,
                            boxstyle="round,pad=0.05",
                            edgecolor='black', facecolor=color, linewidth=2, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold')
        
        if i < len(stages) - 1:
            arrow = FancyArrowPatch((x+0.35, y), (stages[i+1][1]-0.35, stages[i+1][2]),
                                  arrowstyle='->', mutation_scale=20, linewidth=2, color='black')
            ax.add_patch(arrow)
    
    ax.set_title('Inference System Architecture', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('figures/inference_pipeline.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ inference_pipeline.png created")
    plt.close()

# ==============================================================================
# 4. CONFUSION MATRIX
# ==============================================================================
def create_confusion_matrix():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # Sample confusion matrices for each model
    models_data = {
        'RNN': np.array([[8, 2], [2, 8]]),
        'LSTM': np.array([[2, 8], [0, 10]]),
        'GRU': np.array([[8, 2], [2, 8]])
    }
    
    models_names = ['RNN', 'LSTM', 'GRU']
    
    for idx, (ax, model_name) in enumerate(zip(axes, models_names)):
        cm = models_data[model_name]
        
        # Normalize for percentage display
        cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
        
        # Create heatmap
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax, 
                   cbar=True, square=True, linewidths=1, linecolor='black',
                   xticklabels=['Down', 'Up'], yticklabels=['Down', 'Up'])
        
        ax.set_title(f'{model_name} Confusion Matrix', fontsize=12, fontweight='bold', pad=10)
        ax.set_ylabel('True Label', fontsize=10)
        ax.set_xlabel('Predicted Label', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('figures/confusion_matrix.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ confusion_matrix.png created")
    plt.close()

# ==============================================================================
# 5. MODEL ARCHITECTURE COMPARISON (BONUS)
# ==============================================================================
def create_model_architecture():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    models_info = {
        'RNN': [
            'Input (5, 5)',
            'Recurrent Layer\n50 units',
            'Dropout (0.2)',
            'Dense (32)',
            'Dense (1)\nSigmoid'
        ],
        'LSTM': [
            'Input (5, 5)',
            'LSTM Layer\n50 units',
            'Dropout (0.2)',
            'Dense (32)',
            'Dense (1)\nSigmoid'
        ],
        'GRU': [
            'Input (5, 5)',
            'GRU Layer\n50 units',
            'Dropout (0.2)',
            'Dense (32)',
            'Dense (1)\nSigmoid'
        ]
    }
    
    colors_list = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    for idx, (ax, (model_name, layers)) in enumerate(zip(axes, models_info.items())):
        ax.set_xlim(0, 2)
        ax.set_ylim(0, len(layers) + 1)
        ax.axis('off')
        
        # Draw layers
        for i, layer in enumerate(layers):
            y_pos = len(layers) - i - 0.5
            color = colors_list[idx] if i == 1 else '#E8E8E8'
            
            box = FancyBboxPatch((0.2, y_pos-0.35), 1.6, 0.7,
                                boxstyle="round,pad=0.05",
                                edgecolor='black', facecolor=color, linewidth=2)
            ax.add_patch(box)
            ax.text(1, y_pos, layer, ha='center', va='center',
                   fontsize=9, fontweight='bold')
            
            # Draw arrows between layers
            if i < len(layers) - 1:
                arrow = FancyArrowPatch((1, y_pos-0.35), (1, y_pos-0.95),
                                      arrowstyle='->', mutation_scale=15, linewidth=2)
                ax.add_patch(arrow)
        
        ax.set_title(f'{model_name} Architecture', fontsize=12, fontweight='bold', pad=10)
    
    plt.tight_layout()
    plt.savefig('figures/model_architecture.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ model_architecture.png created")
    plt.close()

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == '__main__':
    print("Generating all figures...\n")
    
    create_data_pipeline()
    create_training_pipeline()
    create_inference_pipeline()
    create_confusion_matrix()
    create_model_architecture()
    
    print("\n✅ All figures created successfully!")
    print("\nGenerated files:")
    print("  • figures/data_pipeline.png")
    print("  • figures/training_pipeline.png")
    print("  • figures/inference_pipeline.png")
    print("  • figures/confusion_matrix.png")
    print("  • figures/model_architecture.png (bonus)")
