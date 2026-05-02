import yfinance as yf
import pandas as pd

# Write a function using yfinance to download hourly gold (XAU/USD) price data for the last 60 days and save it to a pandas dataframe.
def fetch_gold_price_data():
    """
    Download hourly gold (XAU/USD) price data for the last 60 days.
    
    Returns:
        pd.DataFrame: DataFrame containing OHLC data with hourly granularity
    """
    try:
        data = yf.download("GC=F", period="60d", interval="1h", progress=False)
        print(f"Successfully fetched {len(data)} hourly gold price records")
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    # Get Gold (XAU/USD) hourly data for 60 days
    gold_data = fetch_gold_price_data()
    if gold_data is not None:
        gold_data.to_csv("market_prices.csv")
        print("Data saved to market_prices.csv")
        print(gold_data.head())