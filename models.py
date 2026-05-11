import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Sequential
import numpy as np

# Create three separate functions: build_rnn(), build_lstm(), and build_gru(). Each should take input_shape as an argument and return a compiled TensorFlow model for time-series forecasting.

def build_rnn(input_shape):
    """
    Build a basic RNN model for time-series sentiment-market classification.
    
    Args:
        input_shape (tuple): Input shape (time_steps, features)
        
    Returns:
        keras.Model: Compiled RNN model
    """
    model = Sequential([
        layers.SimpleRNN(50, activation='relu', input_shape=input_shape),
        layers.Dropout(0.2),
        layers.Dense(32, activation='relu'),
        layers.Dense(3, activation='softmax')  # 3-class classification
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def build_lstm(input_shape):
    """
    Define a Keras Sequential model with an LSTM layer (50 units), a Dropout layer (0.2), and a Dense output layer with 'softmax' activation for 3-class sentiment-market classification.
    
    Args:
        input_shape (tuple): Input shape (time_steps, features)
        
    Returns:
        keras.Model: Compiled LSTM model
    """
    model = Sequential([
        layers.LSTM(50, activation='relu', input_shape=input_shape),
        layers.Dropout(0.2),
        layers.Dense(32, activation='relu'),
        layers.Dense(3, activation='softmax')  # 3-class classification
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def build_gru(input_shape):
    """
    Build a GRU model for time-series sentiment-market classification.
    
    Args:
        input_shape (tuple): Input shape (time_steps, features)
        
    Returns:
        keras.Model: Compiled GRU model
    """
    model = Sequential([
        layers.GRU(50, activation='relu', input_shape=input_shape),
        layers.Dropout(0.2),
        layers.Dense(32, activation='relu'),
        layers.Dense(3, activation='softmax')  # 3-class classification
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def get_all_models(input_shape):
    """
    Get all three models for comparison.
    
    Args:
        input_shape (tuple): Input shape (time_steps, features)
        
    Returns:
        dict: Dictionary containing all three models
    """
    return {
        'RNN': build_rnn(input_shape),
        'LSTM': build_lstm(input_shape),
        'GRU': build_gru(input_shape)
    }

def print_model_summary(model, model_name):
    """
    Print model summary and total parameters.
    
    Args:
        model: Keras model
        model_name (str): Name of the model
    """
    print(f"\n{'=' * 60}")
    print(f"{model_name} Model Summary")
    print(f"{'=' * 60}")
    model.summary()
    print(f"Total Parameters: {model.count_params():,}")

if __name__ == "__main__":
    # Example usage with input shape (30 time steps, 4 features)
    input_shape = (30, 4)  # 30 time steps, 4 features (e.g., OHLC)
    
    print("Building Deep Learning Models for Sentiment-Market Analysis")
    print(f"Input Shape: {input_shape}\n")
    
    models = get_all_models(input_shape)
    
    for model_name, model in models.items():
        print_model_summary(model, model_name)
    
    # Create dummy data for testing
    X_dummy = np.random.randn(100, 30, 4)
    y_dummy = tf.keras.utils.to_categorical(np.random.randint(0, 3, 100), 3)
    
    print(f"\n{'=' * 60}")
    print("Training RNN model on dummy data for 1 epoch")
    print(f"{'=' * 60}")
    
    rnn_model = build_rnn(input_shape)
    rnn_model.fit(X_dummy, y_dummy, epochs=1, batch_size=32, verbose=1)
