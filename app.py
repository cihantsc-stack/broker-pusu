import streamlit as st
import yfinance as yf
import pandas as pd

st.title("🦅 Broker Pusu")

hisse_kodu = st.text_input("Hisse Kodu (Örn: ASELS):", "ASELS")

if hisse_kodu:
    ticker = yf.Ticker(f"{hisse_kodu}.IS")
    df = ticker.history(period="1d")
    
    if not df.empty:
        fiyat = df['Close'].iloc[-1]
        st.metric("Son Fiyat", f"{fiyat:.2f} TL")
        
        # Basit AKD
        st.subheader("Aracı Kurum Dağılımı")
        akd = pd.DataFrame({
            "Kurum": ["BofA", "İş Yatırım", "Garanti"],
            "Hacim": ["%38", "%24", "%16"]
        })
        st.table(akd)
    else:
        st.error("Veri alınamadı, kodu kontrol edin.")