import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Sayfa Yapısı ---
st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

# Session State
if "favori_hisseler" not in st.session_state:
    st.session_state.favori_hisseler = ["ASELS", "THYAO"]

# --- Başlık ---
st.title("🦅 Broker Sinyal Radarı")

# --- Hisse Motoru ---
hisse_input = st.text_input("Hisse Kodu (Örn: ASELS):", "ASELS").upper().strip()

if hisse_input:
    try:
        ticker = yf.Ticker(f"{hisse_input}.IS")
        df = ticker.history(period="1mo")
        
        if not df.empty:
            guncel_fiyat = df['Close'].iloc[-1]
            st.metric("Anlık Fiyat", f"{guncel_fiyat:.2f} TL")
            
            # AKD Simülasyonu
            akd_hacim = df['Volume'].iloc[-1] * guncel_fiyat
            akd_data = pd.DataFrame({
                "Kurum": ["BofA", "İş Yatırım", "Garanti"],
                "Hacim (M TL)": [f"{(akd_hacim * 0.18)/1_000_000:.2f}", f"{(akd_hacim * 0.12)/1_000_000:.2f}", f"{(akd_hacim * 0.08)/1_000_000:.2f}"],
                "Pay": ["%38.5", "%24.2", "%16.8"]
            })
            st.subheader("📊 Gün İçi Aracı Kurum Dağılımı")
            st.table(akd_data)
        else:
            st.error("Veri alınamadı.")
    except Exception as e:
        st.error(f"Hata: {e}")