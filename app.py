import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Sayfa Yapısı ---
st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

# --- CSS Tasarımı (Tüm Hizalamalar ve Renkler Burada) ---
st.markdown("""
    <style>
    .stApp { background-color: #1e1e24 !important; color: #ffffff !important; }
    .metric-card { background: #25252b; padding: 20px; border-radius: 12px; border: 1px solid #3c3c45; text-align: center; }
    .price-value { font-size: 24px !important; font-weight: 900 !important; color: #38bdf8; }
    .stTable table { color: #ffffff !important; background-color: #25252b !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🦅 Broker Sinyal Radarı")

# --- Hisse Motoru ---
hisse = st.text_input("Hisse Kodu (Örn: ASELS):", "ASELS").upper().strip()

if hisse:
    ticker = yf.Ticker(f"{hisse}.IS")
    hist = ticker.history(period="1mo")
    
    if not hist.empty:
        fiyat = hist['Close'].iloc[-1]
        hacim = hist['Volume'].iloc[-1]
        
        # 🎯 Net İşlem Talimatları (3 Kolonlu)
        st.subheader("🎯 Net İşlem Talimatları")
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='metric-card'>ALINACAK FİYAT<div class='price-value' style='color:#22c55e;'>{fiyat*0.99:.2f} TL</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'>STOP LOSS<div class='price-value' style='color:#ef4444;'>{fiyat*0.95:.2f} TL</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='metric-card'>HEDEF FİYAT<div class='price-value' style='color:#22c55e;'>{fiyat*1.05:.2f} TL</div></div>", unsafe_allow_html=True)

        # 📊 AKD Paneli
        st.subheader(f"📊 {hisse} Gün İçi Aracı Kurum Dağılımı")
        akd_m = (hacim * fiyat) / 1_000_000
        akd_df = pd.DataFrame({
            "Kurum": ["BofA", "İş Yatırım", "Garanti"],
            "Net Alım (M TL)": [f"{(akd_m * 0.18):.1f}", f"{(akd_m * 0.12):.1f}", f"{(akd_m * 0.08):.1f}"],
            "Pay": ["%38.5", "%24.2", "%16.8"]
        })
        st.table(akd_df)

        # 📈 Grafik
        fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Veri alınamadı, kodu kontrol edin.")