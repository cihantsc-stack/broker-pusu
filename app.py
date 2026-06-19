import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Sayfa Yapısı
st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

# CSS ile Arka Planı Koyu Yapma ve Elemanları Gece Moduna Uydurma
st.markdown("""
    <style>
    /* Ana Arka Plan ve Metin Renkleri */
    .stApp {
        background-color: #121214 !important;
        color: #e3e3e6 !important;
    }
    /* Girdi Kutusu Etiketi Renklendirme */
    label {
        color: #e3e3e6 !important;
        font-weight: bold !important;
    }
    .stAlert { 
        border-radius: 16px !important; 
        padding: 20px !important; 
    }
    /* Üst Dev Sinyal Kutusu */
    .main-signal {
        font-size: 32px !important;
        font-weight: 900 !important;
        text-align: center;
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 25px;
        letter-spacing: 1px;
    }
    /* 3'lü Net Emir Kartları (Koyu Tema) */
    .instruction-card {
        background: #1a1a1e;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        text-align: center;
        border: 1px solid #2a2a30;
    }
    .instruction-card p {
        color: #b3b3b3 !important;
        margin-bottom: 5px;
    }
    .price-style {
        font-size: 28px !important;
        font-weight: bold !important;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🦅 Broker Sinyal Radarı")
st.write("Borsa bilgisine ihtiyacınız yok. Yapay zeka sizin yerinize hesaplar ve net işlem talimatı verir.")
st.markdown("---")

# Hisse Girişi
hisse_input = st.text_input("Hisse Kodu Yazın ve Enter'a Basın (Örn: ASELS, THYAO, EKOS):", "ASELS").upper().strip()

if hisse_input:
    if not hisse_input.endswith(".IS"):
        hisse_ticker = f"{hisse_input}.IS"
    else:
        hisse_ticker = hisse_input

    try:
        # Veri Çekme
        ticker = yf.Ticker(hisse_ticker)
        df = ticker.history(period="1y")
        
        if df.empty:
            st.error("Hisse kodu bulunamadı. Lütfen doğru yazdığınızdan emin olun.")
        else:
            guncel_fiyat = df['Close'].iloc[-1]
            
            # Arka Plandaki Hesaplamalar
            ma20 = df['Close'].rolling(window=20).mean().iloc[-1]
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / (loss + 1e-9)
            rsi = 100 - (100 / (1 + rs))
            rsi_son = rsi.iloc[-1]
            
            son_ay_df = df.tail(21)
            aylik_en_yuksek = son_ay_df['High'].max()
            aylik_en_dusuk = son_ay_df['Low'].min()
            zirveye_uzaklik = ((aylik_en_yuksek - guncel_fiyat) / aylik_en_yuksek) * 100

            # Seviye Belirleme
            destek_ana = aylik_en_dusuk * 1.02
            direnc