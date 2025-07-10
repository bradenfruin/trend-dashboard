import streamlit as st
import yfinance as yf

def get_stock_metrics(ticker):
    df = yf.Ticker(ticker).history(period="6mo")
    if len(df) < 100:
        return None

    current = df['Close'].iloc[-1]
    prev = df['Close'].iloc[-2]
    day_change = ((current - prev) / prev) * 100
    high_20w = df['Close'].rolling(100).max().iloc[-1]
    roc_20w = ((current - df['Close'].iloc[-100]) / df['Close'].iloc[-100]) * 100
    stop = current * 0.8

    spx = yf.Ticker("^GSPC").history(period="1y")
    spx_200ma = spx['Close'].rolling(200).mean().iloc[-1]
    regime_up = spx['Close'].iloc[-1] > spx_200ma

    return {
        "ticker": ticker,
        "price": current,
        "day_change": day_change,
        "high_20w": high_20w,
        "roc_20w": roc_20w,
        "regime_up": regime_up,
        "stop": stop
    }

st.title("📈 Trend Following Stock Summary")
tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]

for ticker in tickers:
    metrics = get_stock_metrics(ticker)
    if metrics:
        price_color = "green" if metrics["roc_20w"] > 30 else "red"
        regime_color = "green" if metrics["regime_up"] else "red"

        st.markdown(
            f"**{metrics['ticker']}** - "
            f":{price_color}[{metrics['price']:.2f} ({metrics['day_change']:+.2f}%)] - "
            f"High: {metrics['high_20w']:.2f} - "
            f":{regime_color}[Regime: {'Up' if metrics['regime_up'] else 'Down'}] - "
            f"Stop: {metrics['stop']:.2f}"
        )
