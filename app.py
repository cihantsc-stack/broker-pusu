import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- Sayfa Yapısı ---
st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

# --- CSS Ayarları ---
st.markdown("""
    <style>
    .stApp { background-color: #1e1e24 !important; color: #ffffff !important; }
    .instruction-card { background: #25252b; padding: 20px; border-radius: 12px; border: 1px solid #4b5563; text-align: center; }
    .main-signal { font-size: 32px !important; font-weight: 900 !important; text-align: center; padding: 30px; border-radius: 16px; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# --- SİNYAL MANTIĞI (Örnek değişken tanımları) ---
# (Bu kısım senin ana kodundaki değişkenlerinle aynı olmalı)
islem_durumu = "alma" 
stop_loss = 354.86
direnc_ana = 413.00

# --- 🎯 3 NET RAKAM KARTI (Hata almayacağın temiz yapı) ---
st.markdown("### 🎯 Net İşlem Talimatları")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="instruction-card" style="height: 140px;">', unsafe_allow_html=True)
    st.markdown("<p style='color:#ffffff !important; font-weight:bold; margin-bottom:10px;'>📥 ALIM DURUMU</p>", unsafe_allow_html=True)
    if islem_durumu == "al":
        st.markdown('<div style="font-size: 26px !important; font-weight: 900 !important; color: #22c55e !important;">ALINIR</div>', unsafe_allow_html=True)
    elif islem_durumu == "alma":
        st.markdown('<div style="font-size: 26px !important; font-weight: 900 !important; color: #ef4444 !important;">ALINMAZ</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size: 26px !important; font-weight: 900 !important; color: #fbbf24 !important;">BEKLE</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="instruction-card" style="height: 140px;">', unsafe_allow_html=True)
    st.markdown("<p style='color:#ffffff !important; font-weight:bold; margin-bottom:10px;'>🛡️ KOL KESME (STOP)</p>", unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 26px !important; font-weight: 900 !important; color: #ef4444 !important;">{stop_loss:.2f} TL</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="instruction-card" style="height: 140px;">', unsafe_allow_html=True)
    st.markdown("<p style='color:#ffffff !important; font-weight:bold; margin-bottom:10px;'>🦅 HEDEF FİYAT</p>", unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 26px !important; font-weight: 900 !important; color: #22c55e !important;">{direnc_ana:.2f} TL</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)