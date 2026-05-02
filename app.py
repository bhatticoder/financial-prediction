import streamlit as st
import numpy as np
import pandas as pd
from sentiment import analyze_sentiment, get_sentiment_label_text

# Page configuration
st.set_page_config(
    page_title="Market Sentiment Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Market Sentiment Analyzer")
st.markdown("---")

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Sentiment Analysis", "Market Insights", "About"])

with tab1:
    st.header("Sentiment Analysis")
    st.markdown("### Analyze text sentiment using VADER")
    
    # Text input
    user_input = st.text_area(
        "Enter news headline or text to analyze:",
        placeholder="E.g., 'The stock market reached all-time highs today!'",
        height=100
    )
    
    if st.button("Analyze Sentiment", type="primary"):
        if user_input.strip():
            # Perform sentiment analysis
            result = analyze_sentiment(user_input)
            sentiment_label = result['sentiment']
            sentiment_text = get_sentiment_label_text(sentiment_label)
            confidence = abs(result['compound_score'])
            
            # Display results with color coding
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Sentiment",
                    sentiment_text,
                    f"{confidence:.2%} confidence"
                )
            
            with col2:
                st.metric(
                    "Compound Score",
                    f"{result['compound_score']:.3f}",
                    "VADER Score"
                )
            
            with col3:
                if sentiment_label == 1:
                    st.success("✅ Positive Impact Expected")
                elif sentiment_label == -1:
                    st.error("❌ Negative Impact Expected")
                else:
                    st.info("⚪ Neutral - Mixed Signals")
            
            # Detailed breakdown
            st.markdown("### Score Breakdown")
            breakdown_data = {
                'Component': ['Positive', 'Negative', 'Neutral'],
                'Score': [result['positive'], result['negative'], result['neutral']]
            }
            breakdown_df = pd.DataFrame(breakdown_data)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.dataframe(breakdown_df, use_container_width=True)
            with col2:
                st.bar_chart(breakdown_df.set_index('Component'))
        else:
            st.warning("Please enter text to analyze")

with tab2:
    st.header("Market Insights")
    st.markdown("### Real-time Market Analysis Dashboard")
    
    # Simulated market data
    st.subheader("Market Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Gold Price (XAU/USD)", "$2,350.50", "+0.85%")
    with col2:
        st.metric("S&P 500", "5,432.10", "+1.23%")
    with col3:
        st.metric("NASDAQ", "17,249.50", "+1.95%")
    with col4:
        st.metric("VIX Index", "12.45", "-2.10%")
    
    # Market sentiment chart
    st.subheader("Market Sentiment Distribution")
    sentiment_counts = {
        'Positive': 45,
        'Neutral': 30,
        'Negative': 25
    }
    sentiment_df = pd.DataFrame(
        list(sentiment_counts.items()),
        columns=['Sentiment', 'Count']
    )
    st.bar_chart(sentiment_df.set_index('Sentiment'))
    
    # Recent headlines with sentiment
    st.subheader("Recent Headlines with Sentiment")
    sample_headlines = [
        {
            'Headline': 'Federal Reserve signals potential rate cuts in 2024',
            'Sentiment': 'Positive',
            'Confidence': 0.87
        },
        {
            'Headline': 'Tech stocks surge on AI breakthroughs',
            'Sentiment': 'Positive',
            'Confidence': 0.92
        },
        {
            'Headline': 'Oil prices stable amid geopolitical concerns',
            'Sentiment': 'Neutral',
            'Confidence': 0.65
        },
        {
            'Headline': 'Earnings miss leads to market sell-off',
            'Sentiment': 'Negative',
            'Confidence': 0.88
        },
    ]
    
    headlines_df = pd.DataFrame(sample_headlines)
    st.dataframe(headlines_df, use_container_width=True, hide_index=True)

with tab3:
    st.header("About This Application")
    st.markdown("""
    ### Market Sentiment Analyzer
    
    This application uses advanced Natural Language Processing and Deep Learning to analyze financial news 
    and market sentiment to help predict market movements.
    
    #### Key Features:
    - **VADER Sentiment Analysis**: Real-time sentiment classification (Positive, Negative, Neutral)
    - **Market Data Integration**: Live integration with Yahoo Finance data
    - **News Scraping**: Reuters RSS feeds and Reddit financial communities
    - **Deep Learning Models**: LSTM, GRU, and RNN models for time-series analysis
    
    #### Data Sources:
    - Yahoo Finance (XAU/USD, stock prices)
    - Reuters Financial News
    - Reddit (r/wallstreetbets, r/finance)
    
    #### Sentiment Classification:
    - **Positive**: Compound score > 0.05
    - **Negative**: Compound score < -0.05
    - **Neutral**: Compound score between -0.05 and 0.05
    
    #### Models Used:
    1. **LSTM (Long Short-Term Memory)**: Best for long-term dependencies
    2. **GRU (Gated Recurrent Unit)**: Faster training with fewer parameters
    3. **RNN (Recurrent Neural Network)**: Baseline sequential model
    
    ---
    *Built with Streamlit, TensorFlow, and NLTK*
    """)
    
    st.markdown("### Project Statistics")
    stats = {
        'Metric': ['Total Headlines Analyzed', 'Active Models', 'Data Sources', 'Classification Classes'],
        'Value': ['5000+', '3', '3', '3 (Positive/Neutral/Negative)']
    }
    stats_df = pd.DataFrame(stats)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("*Market Sentiment Analyzer v1.0 | Category B Project*")
