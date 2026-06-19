import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Sayfa Yapısı
st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

# CSS ile Arka Planı Gri Yapma, Yazı Renklerini Okunabilir Hale Getirme
st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e24 !important;
        color: #f3f4f6 !important;
    }
    label {
        color: #f3f4f6 !important;
        font-weight: bold !important;
    }
    .stAlert { 
        border-radius: 16px !important; 
        padding: 20px !important; 
    }
    .main-signal {
        font-size: 32px !important;
        font-weight: 900 !important;
        text-align: center;
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 25px;
        letter-spacing: 1px;
    }
    .instruction-card {
        background: #25252b;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        text-align: center;
        border: 1px solid #32323a;
    }
    .price-style {
        font-size: 28px !important;
        font-weight: bold !important;
        margin-top: 10px;
    }
    .comment-card {
        background: #25252b;
        padding: 22px;
        border-radius: 12px;
        border-left: 5px solid #60a5fa;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .guide-card {
        background: #25252b;
        padding: 20px;
        border-radius: 12px;
        border: 1px dashed #4b5563;
        margin-top: 15px;
    }
    .terminal-card {
        background: #25252b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #32323a;
        text-align: center;
    }
    
    [data-testid="stMetricLabel"] {
        color: #e5e7eb !important;
        font-size: 14px !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 24px !important;
        font-weight: 800 !important;
    }
    .stTable, table {
        color: #f3f4f6 !important;
        background-color: #25252b !important;
    }
    th {
        background-color: #32323a !important;
        color: #60a5fa !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }
    td {
        color: #f3f4f6 !important;
        font-size: 13px !important;
    }
    .stExpander p {
        color: #ffffff !important;
        font-weight: bold !important;
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
        
        try:
            info = ticker.info
            if not info: info = {}
        except:
            info = {}
        
        if df.empty:
            st.error("Hisse kodu bulunamadı. Lütfen doğru yazdığınızdan emin olun.")
        else:
            guncel_fiyat = df['Close'].iloc[-1]
            
            # Arka Plandaki Teknik Hesaplamalar
            ma20_seri = df['Close'].rolling(window=20).mean()
            ma20 = ma20_seri.iloc[-1]
            
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
            direnc_ana = aylik_en_yuksek
            stop_loss = destek_ana * 0.98

            # Puanlama Kriterleri
            puan = 0
            if rsi_son < 45: puan += 1
            if guncel_fiyat > ma20: puan += 1
            if zirveye_uzaklik > 15: puan += 1

            # --- 1. ADIM: DEV SİNYAL KUTUSU ---
            if puan >= 2 and guncel_fiyat <= destek_ana * 1.05:
                st.markdown('<div class="main-signal" style="background-color: #1e3a24; color: #a2e8b2; border: 3px solid #28a745;">🟢 GÖNÜL RAHATLIĞIYLA ALINAB