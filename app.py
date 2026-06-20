import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🦅 Broker Sinyal Radarı")

hisse = st.text_input("Hisse Kodu:", "ASELS").upper().strip()

if hisse:
    t = yf.Ticker(f"{hisse}.IS")
    df = t.history(period="1mo")
    if not df.empty:
        fiyat = df['Close'].iloc[-1]
        st.metric("Anlık Fiyat", f"{fiyat:.2f} TL")
        
        # Basit AKD
        st.subheader("📊 Aracı Kurum Dağılımı")
        akd = pd.DataFrame({"Kurum": ["BofA", "İş", "Garanti"], "Pay": ["%38", "%24", "%16"]})
        st.table(akd)
    else:
        st.error("Veri alınamadı.")