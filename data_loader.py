"""
Data Loading and Preprocessing Module
Loads and prepares collected data for model training
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional
import os


class DataLoader:
    """Load and preprocess collected financial data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
    
    def get_latest_prices_file(self) -> Optional[Path]:
        """Get the latest prices CSV file"""
        price_files = list(self.data_dir.glob("prices_*.csv"))
        if price_files:
            return sorted(price_files)[-1]
        return None
    
    def get_latest_news_file(self) -> Optional[Path]:
        """Get the latest news CSV file"""
        news_files = list(self.data_dir.glob("news_*.csv"))
        if news_files:
            return sorted(news_files)[-1]
        return None
    
    def get_latest_reddit_file(self) -> Optional[Path]:
        """Get the latest Reddit CSV file"""
        reddit_files = list(self.data_dir.glob("reddit_*.csv"))
        if reddit_files:
            return sorted(reddit_files)[-1]
        return None
    
    def load_prices(self, file_path: Optional[Path] = None) -> pd.DataFrame:
        """
        Load price data
        
        Args:
            file_path: Path to prices CSV. If None, loads latest.
        
        Returns:
            DataFrame with price data
        """
        if file_path is None:
            file_path = self.get_latest_prices_file()
        
        if file_path is None:
            print("No price data files found")
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(file_path)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], utc=True)
            df = df.sort_values('Timestamp').reset_index(drop=True)
            print(f"✓ Loaded prices from: {file_path.name} ({len(df)} records)")
            return df
        except Exception as e:
            print(f"✗ Error loading {file_path}: {e}")
            return pd.DataFrame()
    
    def load_news(self, file_path: Optional[Path] = None) -> pd.DataFrame:
        """Load news data"""
        if file_path is None:
            file_path = self.get_latest_news_file()
        
        if file_path is None:
            print("No news data files found")
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(file_path)
            df['published'] = pd.to_datetime(df['published'], utc=True, errors='coerce')
            print(f"✓ Loaded news from: {file_path.name} ({len(df)} records)")
            return df
        except Exception as e:
            print(f"✗ Error loading {file_path}: {e}")
            return pd.DataFrame()
    
    def load_reddit(self, file_path: Optional[Path] = None) -> pd.DataFrame:
        """Load Reddit data"""
        if file_path is None:
            file_path = self.get_latest_reddit_file()
        
        if file_path is None:
            print("No Reddit data files found")
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(file_path)
            df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
            print(f"✓ Loaded Reddit from: {file_path.name} ({len(df)} records)")
            return df
        except Exception as e:
            print(f"✗ Error loading {file_path}: {e}")
            return pd.DataFrame()
    
    def load_all_data(self) -> dict:
        """Load all available data sources"""
        print("\n" + "="*60)
        print("📊 LOADING DATA")
        print("="*60)
        
        data = {
            'prices': self.load_prices(),
            'news': self.load_news(),
            'reddit': self.load_reddit()
        }
        
        return data
    
    def prepare_target_variable(self, prices_df: pd.DataFrame, lookahead: int = 1) -> pd.DataFrame:
        """
        Prepare target variable for prediction
        Binary classification: 1 = price up, 0 = price down
        
        Args:
            prices_df: DataFrame with OHLC prices
            lookahead: Number of periods ahead to predict
        
        Returns:
            DataFrame with target variable added
        """
        df = prices_df.copy()
        
        # Group by ticker and calculate returns
        def calculate_returns(group):
            group['Close_Future'] = group['Close'].shift(-lookahead)
            group['Return'] = (group['Close_Future'] - group['Close']) / group['Close']
            group['Target'] = (group['Return'] > 0).astype(int)
            return group
        
        df = df.groupby('Ticker', group_keys=False).apply(calculate_returns)
        
        # Remove NaN rows
        df = df.dropna(subset=['Target'])
        
        return df
    
    def create_timeseries_data(self, df: pd.DataFrame, sequence_length: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences for RNN/LSTM training
        
        Args:
            df: DataFrame with features and targets
            sequence_length: Number of time steps in each sequence
        
        Returns:
            X and y arrays for model training
        """
        X = []
        y = []
        
        # Select price features
        feature_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        values = df[feature_cols].values
        targets = df['Target'].values
        
        # Normalize features
        values = (values - values.mean(axis=0)) / (values.std(axis=0) + 1e-8)
        
        # Create sequences
        for i in range(len(values) - sequence_length):
            X.append(values[i:i+sequence_length])
            y.append(targets[i+sequence_length])
        
        X = np.array(X)
        y = np.array(y)
        
        return X, y
    
    def split_train_test(self, X: np.ndarray, y: np.ndarray, test_ratio: float = 0.2) -> Tuple:
        """
        Split data into train and test sets (temporal split)
        
        Args:
            X: Feature sequences
            y: Target values
            test_ratio: Ratio of test data
        
        Returns:
            X_train, X_test, y_train, y_test
        """
        split_idx = int(len(X) * (1 - test_ratio))
        
        X_train = X[:split_idx]
        X_test = X[split_idx:]
        y_train = y[:split_idx]
        y_test = y[split_idx:]
        
        print(f"\n✓ Data split:")
        print(f"  Train: {len(X_train)} samples")
        print(f"  Test:  {len(X_test)} samples")
        
        return X_train, X_test, y_train, y_test
    
    def get_data_summary(self, data: dict) -> None:
        """Print summary of loaded data"""
        print("\n" + "="*60)
        print("📈 DATA SUMMARY")
        print("="*60)
        
        for source_name, df in data.items():
            if not df.empty:
                print(f"\n{source_name.upper()}:")
                print(f"  Records: {len(df)}")
                print(f"  Date Range: {df.iloc[:, 0] if not df.empty else 'N/A'} to {df.iloc[-1, 0] if not df.empty else 'N/A'}")
                print(f"  Columns: {list(df.columns)}")
            else:
                print(f"\n{source_name.upper()}: No data")


def main():
    """Example usage"""
    loader = DataLoader()
    
    # Load all data
    data = loader.load_all_data()
    
    # Print summary
    loader.get_data_summary(data)
    
    # Prepare data for model training
    if not data['prices'].empty:
        print("\n" + "="*60)
        print("🤖 PREPARING DATA FOR TRAINING")
        print("="*60)
        
        # Add target variable
        prices_with_target = loader.prepare_target_variable(data['prices'], lookahead=1)
        print(f"\n✓ Target variable prepared")
        print(f"  Positive class (price up): {(prices_with_target['Target'] == 1).sum()}")
        print(f"  Negative class (price down): {(prices_with_target['Target'] == 0).sum()}")
        
        # Create sequences
        X, y = loader.create_timeseries_data(prices_with_target, sequence_length=5)
        print(f"\n✓ Sequences created:")
        print(f"  X shape: {X.shape}")
        print(f"  y shape: {y.shape}")
        
        # Train-test split
        X_train, X_test, y_train, y_test = loader.split_train_test(X, y, test_ratio=0.2)
        
        # Save for later use
        np.save('data/X_train.npy', X_train)
        np.save('data/X_test.npy', X_test)
        np.save('data/y_train.npy', y_train)
        np.save('data/y_test.npy', y_test)
        print("\n✓ Training data saved to data/ directory")


if __name__ == "__main__":
    main()
