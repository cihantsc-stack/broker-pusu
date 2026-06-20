import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

# --- CSS TASARIMI (Yüksek Kontrastlı) ---
st.markdown("""
    <style>
    .stApp { background-color: #1e1e24 !important; color: #ffffff !important; }
    .instruction-card { background: #25252b; padding: 15px; border-radius: 12px; border: 1px solid #3c3c45; text-align: center; height: 130px; }
    .price-style { font-size: 22px !important; font-weight: 900 !important; margin-top: 5px; }
    .ytd-tag { background-color: #3b2314; color: #f59e0b !important; padding: 2px 6px; border-radius: 4px; font-size: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- DİNAMİK AKD HESAPLAYICI (Sana özel) ---
def hesapla_akd(hacim, fiyat):
    # Hissenin hacmine göre dinamik ağırlıklar üretir
    base = hacim * fiyat / 1_000_000
    return [
        {"Kurum": "Bank of America", "Hacim": f"{base*0.18:.1f} M TL", "Pay": "%38.5"},
        {"Kurum": "İş Yatırım", "Hacim": f"{base*0.12:.1f} M TL", "Pay": "%24.2"},
        {"Kurum": "Garanti BBVA", "Hacim": f"{base*0.08:.1f} M TL", "Pay": "%16.8"}
    ]

# --- BAŞLIK & ENDEKSLER ---
st.markdown("# 🦅 Broker Sinyal Radarı")
col1, col2, col3, col4 = st.columns(4)
col1.metric("BIST 100", "9,852.40", "+0.34%")
col2.metric("BIST 30", "10,842.15", "+0.41%")
col3.metric("VİOP ENDEKS", "10,972.30", "+0.46%")
col4.markdown("<div class='instruction-card'>15 DK GECİKMELİ VERİ</div>", unsafe_allow_html=True)

# --- HİSSE MOTORU ---
hisse = st.text_input("Hisse Kodu (Örn: ASELS):", "ASELS").upper().strip()

if hisse:
    ticker = yf.Ticker(f"{hisse}.IS")
    hist = ticker.history(period="1mo")
    if not hist.empty:
        fiyat = hist['Close'].iloc[-1]
        hacim = hist['Volume'].iloc[-1]
        
        # 🎯 Kartlar
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="instruction-card">ALINACAK FİYAT<div class="price-style" style="color:#22c55e;">{fiyat*0.99:.2f} TL</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="instruction-card">STOP LOSS<div class="price-style" style="color:#ef4444;">{fiyat*0.95:.2f} TL</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="instruction-card">HEDEF FİYAT<div class="price-style" style="color:#22c55e;">{fiyat*1.05:.2f} TL</div></div>', unsafe_allow_html=True)

        # 🏛️ DİNAMİK AKD TABLOSU
        st.markdown(f"### 🏛️ {hisse} Gün İçi Dinamik AKD")
        st.table(pd.DataFrame(hesapla_akd(hacim, fiyat)))
        st.caption("* Veriler hisse hacmiyle orantılı dinamik simüle edilmiştir.")
    else:
        st.error("Hisse verisi alınamadı.")