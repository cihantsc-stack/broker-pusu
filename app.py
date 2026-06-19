import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 🏛️ SAYFA VE OTOMATİK GÜNCELLEME
# ==========================================
st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

if "favori_hisseler" not in st.session_state:
    st.session_state.favori_hisseler = ["ASELS", "THYAO"]

try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=600000, key="radar_final_refresh")
except:
    pass

# ==========================================
# 🎨 TÜM RADAR CSS TASARIMI
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #1e1e24 !important; color: #ffffff !important; }
    .instruction-card { background: #25252b; padding: 20px; border-radius: 12px; border: 1px solid #4b5563; text-align: center; }
    .main-signal { font-size: 30px !important; font-weight: 900 !important; text-align: center; padding: 25px; border-radius: 16px; margin-bottom: 20px; }
    .ytd-tag { background-color: #3b2314; color: #f59e0b !important; font-weight: bold; padding: 4px 10px; border-radius: 6px; font-size: 11px; }
    .left-market-box { background: #25252b; padding: 12px; border-radius: 12px; border: 1px solid #3e3e4a; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🦅 Broker Sinyal Radarı")

# --- ENDEKS KISMI ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("BIST 100", "9,852.40", "+0.34%")
c2.metric("BIST 30", "10,842.15", "+0.41%")
c3.metric("VİOP ENDEKS", "10,972.30", "+0.46%")
c4.markdown("<div class='instruction-card'>15 DK GECİKMELİ VERİ</div>", unsafe_allow_html=True)

st.markdown("---")

# --- HİSSE MOTORU ---
hisse_input = st.text_input("Hisse Kodu (Örn: ASELS):", "ASELS").upper().strip()

if hisse_input:
    # Sinyal değişkenleri (Gerçek hesaplamaların buraya gelmeli)
    islem_durumu = "al"
    stop_loss = 350.00
    direnc_ana = 450.00
    
    # 🎯 3 NET RAKAM KARTI
    st.markdown("### 🎯 Net İşlem Talimatları")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="instruction-card" style="height: 140px;">', unsafe_allow_html=True)
        st.write("<p style='color:#ffffff !important; font-weight:bold; margin-bottom:10px;'>📥 ALIM DURUMU</p>", unsafe_allow_html=True)
        color = "#22c55e" if islem_durumu == "al" else "#ef4444"
        text = "ALINIR" if islem_durumu == "al" else "ALINMAZ"
        st.markdown(f'<div style="font-size: 26px !important; font-weight: 900 !important; color: {color} !important;">{text}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="instruction-card" style="height: 140px;">', unsafe_allow_html=True)
        st.write("<p style='color:#ffffff !important; font-weight:bold; margin-bottom:10px;'>🛡️ KOL KESME (STOP)</p>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 26px !important; font-weight: 900 !important; color: #ef4444 !important;">{stop_loss:.2f} TL</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="instruction-card" style="height: 140px;">', unsafe_allow_html=True)
        st.write("<p style='color:#ffffff !important; font-weight:bold; margin-bottom:10px;'>🦅 HEDEF FİYAT</p>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 26px !important; font-weight: 900 !important; color: #22c55e !important;">{direnc_ana:.2f} TL</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)