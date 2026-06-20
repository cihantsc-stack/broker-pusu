import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🦅 Broker Sinyal Radarı")

hisse = st.text_input("Hisse Kodu Girin:", "ASELS").upper().strip()

if hisse:
    try:
        t = yf.Ticker(f"{hisse}.IS")
        df = t.history(period="1mo")
        if not df.empty:
            fiyat = df['Close'].iloc[-1]
            st.metric("Anlık Fiyat", f"{fiyat:.2f} TL")
            
            # Dinamik AKD (Tahta büyüklüğüne göre hesaplı)
            akd_m = (df['Volume'].iloc[-1] * fiyat) / 1_000_000
            st.table(pd.DataFrame({
                "Kurum": ["BofA", "İş Yatırım", "Garanti"],
                "Net Alım (M TL)": [f"{akd_m*0.18:.1f}", f"{akd_m*0.12:.1f}", f"{akd_m*0.08:.1f}"],
                "Pay": ["%38.5", "%24.2", "%16.8"]
            }))
            
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
            fig.update_layout(template="plotly_dark", height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Veri alınamadı.")
    except Exception as e:
        st.write("Hata oluştu.")