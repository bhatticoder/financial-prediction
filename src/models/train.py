# src/models/train.py
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

def train_model(model, model_name, X_train, y_train, X_val, y_val, epochs=50, batch_size=32):
    """
    Train a recurrent model (GRU, LSTM, or RNN)
    
    Args:
        model: PyTorch model instance
        model_name: Name of model (for logging)
        X_train, y_train: Training data
        X_val, y_val: Validation data
        epochs: Number of training epochs
        batch_size: Batch size for training
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    # Create data loaders
    train_dataset = TensorDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    best_val_loss = float('inf')
    
    for epoch in range(epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            X_val_device = X_val.to(device)
            y_val_device = y_val.to(device)
            val_outputs = model(X_val_device)
            val_loss = criterion(val_outputs, y_val_device).item()
        
        if (epoch + 1) % 10 == 0:
            print(f"{model_name} - Epoch {epoch+1}/{epochs}, Train Loss: {train_loss/len(train_loader):.4f}, Val Loss: {val_loss:.4f}")
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            import os
            os.makedirs("models", exist_ok=True)
            torch.save(model.state_dict(), f"models/{model_name.lower()}_best.pt")
    
    print(f"{model_name} training complete. Best Val Loss: {best_val_loss:.4f}")
