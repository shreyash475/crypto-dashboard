# part 1: Import libraries and set up Streamlit app

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("📈 Cryptocurrency Analytics Dashboard")
st.markdown("Real-time price tracking and analysis")

# Sidebar for user input
st.sidebar.header("Select Cryptocurrencies")
coins = st.sidebar.multiselect(
    "Choose coins to track:",
    ["bitcoin", "ethereum", "cardano", "solana", "dogecoin"],
    default=["bitcoin", "ethereum"]
)

# ----------------------------------------------------------------------------------------------------------------------------


# part 2: Fetch data from CoinGecko API

if coins:
    coin_ids = ','.join(coins)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_ids}&vs_currencies=usd&include_24hr_change=true"
    
    response = requests.get(url)
    data = response.json()
    
    # Show raw JSON for learners
    st.subheader("📜 Raw JSON Response (from API)")
    st.json(data)  # 👈 This line displays the JSON in an interactive formatted way

    # Convert to DataFrame for analysis
    df = pd.DataFrame(data).T
    df.columns = ['Price (USD)', '24h Change (%)']
    df.index.name = 'Cryptocurrency'
    
    st.subheader("Current Prices")
    st.dataframe(df.style.format({
        'Price (USD)': '${:,.2f}',
        '24h Change (%)': '{:+.2f}%'
    }))

# ----------------------------------------------------------------------------------------------------------------------------

# Part 3: Visualization

# Create comparison bar chart
    st.subheader("Price Comparison")
    fig_price = px.bar(
        df, 
        y='Price (USD)',
        title="Current Cryptocurrency Prices",
        color='Price (USD)',
        color_continuous_scale='viridis'
    )
    st.plotly_chart(fig_price, use_container_width=True)
    
    # Create 24h change chart
    st.subheader("24-Hour Performance")
    fig_change = px.bar(
        df,
        y='24h Change (%)',
        title="24-Hour Price Change",
        color='24h Change (%)',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_change, use_container_width=True)

# ----------------------------------------------------------------------------------------------------------------------------


# Part 4: Metrics

# Calculate and display metrics
    st.subheader("Portfolio Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_price = df['Price (USD)'].mean()
        st.metric("Average Price", f"${avg_price:,.2f}")
    
    with col2:
        avg_change = df['24h Change (%)'].mean()
        st.metric("Avg 24h Change", f"{avg_change:+.2f}%", 
                  delta=f"{avg_change:.2f}%")
    
    with col3:
        best_performer = df['24h Change (%)'].idxmax()
        best_change = df.loc[best_performer, '24h Change (%)']
        st.metric("Best Performer", best_performer.capitalize(),
                  delta=f"{best_change:+.2f}%")
        
# ----------------------------------------------------------------------------------------------------------------------------

# Part 5: Historical Data Visualization
# In sidebar, add date range
st.sidebar.subheader("Historical Analysis")
days = st.sidebar.slider("Days of history", 7, 90, 30)

# Fetch historical data (using CoinGecko market chart endpoint)
if coins and len(coins) == 1:  # Single coin for simplicity
    coin = coins[0]
    hist_url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days}"
    hist_data = requests.get(hist_url).json()

     # Show raw JSON for learners
    st.subheader("📜 Raw JSON Response (from API)")
    st.json(hist_data)  # 👈 This line displays the JSON in an interactive formatted way
    
    # Process time-series data
    prices = hist_data['prices']
    df_hist = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df_hist['date'] = pd.to_datetime(df_hist['timestamp'], unit='ms')
    
    # Plot time-series
    st.subheader(f"{coin.capitalize()} Price History ({days} days)")
    fig_hist = px.line(df_hist, x='date', y='price', 
                       title=f"Price Trend")
    st.plotly_chart(fig_hist, use_container_width=True)