import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Broker Pusu", layout="wide")
st.title("🦅 Broker Sinyal Radarı")

hisse = st.text_input("Hisse Kodu (Örn: ASELS):", "ASELS").upper().strip()

if hisse:
    t = yf.Ticker(f"{hisse}.IS")
    df = t.history(period="1d")
    
    if not df.empty:
        fiyat = df['Close'].iloc[-1]
        st.metric("Son Fiyat", f"{fiyat:.2f} TL")
        
        # Basit AKD Tablosu
        akd = pd.DataFrame({
            "Kurum": ["BofA", "İş Yatırım", "Garanti"],
            "Pay": ["%38", "%24", "%16"]
        })
        st.table(akd)
    else:
        st.error("Veri alınamadı.")