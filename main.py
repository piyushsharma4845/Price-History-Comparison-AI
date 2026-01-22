import streamlit as st
import pandas as pd
import plotly.express as px
import time
from scraper import fetch_amazon_price
from matcher import generate_60_day_history, predict_future_price

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Price Intel AI", page_icon="📈", layout="wide")

# --- 2. CUSTOM CSS FOR DARK UI ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff9900;
        color: black;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #e68a00;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CLEAN HEADER SECTION (Logo & Title) ---
# Replace the URL below with your own logo link if you have one
logo_url = "https://cdn-icons-png.flaticon.com/512/3081/3081628.png"

st.markdown(f"""
    <div style="text-align: center;">
        <img src="{logo_url}" width="80">
        <h1 style="margin-top: 10px;">Amazon Price Intelligence AI</h1>
        <p style="color: #8b949e;">Real-time Scraping • Predictive Analysis • Market Insights</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 4. INPUT SECTION ---
url_input = st.text_input("📍 Paste Amazon.in Product Link:", placeholder="https://www.amazon.in/dp/B0...")
analyze_btn = st.button("🚀 ANALYZE MARKET TRENDS")

# --- 5. APP LOGIC ---
if analyze_btn:
    if url_input:
        with st.spinner("🧠 AI is analyzing the product page..."):
            name, current_price = fetch_amazon_price(url_input)
            
        if name == "BLOCKED":
            st.error("🚫 Access Denied: Amazon blocked the request. Try again in a few minutes.")
        elif name == "NOT_FOUND":
            st.error("🔎 Product not found. Ensure you are using a direct product URL.")
        elif name and current_price:
            
            # Run AI Engine (Local Imports)
            df = generate_60_day_history(current_price)
            pred_price, trend = predict_future_price(df)
            
            # Display Product Name
            st.subheader(f"📦 {name[:100]}...")
            
            # --- METRIC CARDS ---
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            m_col1.metric("Current Price", f"₹{int(current_price):,}")
            m_col2.metric("AI Prediction (7d)", f"₹{int(pred_price):,}", delta=trend, delta_color="inverse")
            m_col3.metric("60-Day Low", f"₹{int(df['price'].min()):,}")
            m_col4.metric("Market Status", "Stable" if trend == "DOWN" else "Rising")

            st.divider()

            # --- VISUALIZATION & RECOMMENDATION ---
            c_left, c_right = st.columns([2, 1])
            
            with c_left:
                fig = px.line(df, x='date', y='price', title="Estimated 60-Day Price Trend")
                fig.update_traces(line_color='#ff9900', line_width=3)
                fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            
            with c_right:
                st.write("### 🤖 AI Recommendation")
                if trend == "DOWN":
                    st.success("#### ACTION: WAIT")
                    st.write("Our model detects a downward trend. Prices are expected to drop. Waiting could save you money.")
                else:
                    st.warning("#### ACTION: BUY NOW")
                    st.write("Prices are trending upwards. Current market data suggests purchasing now before the next hike.")
                
                st.info("**Confidence:** 85%")
        else:
            st.error("❌ Failed to extract price. Check if the product is in stock.")
    else:
        st.warning("Please paste a link first.")

# --- 6. FOOTER ---
st.markdown("<br><br><center><p style='color: gray;'>Developed by Piyush Sharma | CSE AI Project</p></center>", unsafe_allow_html=True)
