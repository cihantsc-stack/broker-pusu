import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Sayfa Yapısı
st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

# Hafıza Yönetimi (Hisselerin sıfırlanmasını engeller)
if "secilen_hisseler" not in st.session_state:
    st.session_state.secilen_hisseler = ["ASELS", "THYAO", "EKOS"]

# Otomatik Yenileme (Sayfa kilitlenmesini önlemek için süre 15 saniyeye optimize edildi)
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=15000, key="radar_global_refresh")
except:
    pass

# CSS Düzenlemeleri
st.markdown("""
    <style>
    .stApp { background-color: #1e1e24 !important; color: #f3f4f6 !important; }
    label { color: #f3f4f6 !important; font-weight: bold !important; }
    .main-signal {
        font-size: 24px !important; font-weight: 900 !important; text-align: center;
        padding: 15px; border-radius: 12px; margin-bottom: 15px;
    }
    .instruction-card {
        background: #25252b; padding: 15px; border-radius: 10px;
        text-align: center; border: 1px solid #32323a;
    }
    .price-style { font-size: 22px !important; font-weight: bold !important; margin-top: 5px; }
    
    /* Üst Endeks Kutuları */
    .market-box {
        background: #25252b; padding: 12px; border-radius: 12px;
        text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.2); border: 1px solid #3e3e4a;
    }
    .time-box {
        background: #10b981; padding: 12px; border-radius: 12px;
        text-align: center; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🦅 Broker Sinyal Radarı")

# --- ÜST KATMAN: CANLI SAAT & ENDEKSLER ---
grid_col1, grid_col2, grid_col3, grid_col4 = st.columns([1.5, 2, 2, 2])

# 🧭 1. Dijital Saat (Türkiye Saati)
with grid_col1:
    try:
        import pytz
        tz = pytz.timezone("Europe/Istanbul")
        su_an = datetime.now(tz)
    except:
        from datetime import timedelta
        su_an = datetime.utcnow() + timedelta(hours=3)
    
    saat_str = su_an.strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="time-box">
        <span style="color:#ffffff; font-weight:bold; font-size:11px;">⏱️ CANLI SİSTEM SAATİ</span><br>
        <span style="font-size:24px; font-weight:900; color:#ffffff;">{saat_str}</span>
    </div>
    """, unsafe_allow_html=True)

# Gecikmeli Veri Çekme Fonksiyonu
def hızlı_veri_cek(ticker_kod):
    try:
        t = yf.Ticker(ticker_kod)
        h = t.history(period="2d")
        if not h.empty and len(h) >= 2:
            return h['Close'].iloc[-1], ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
        return None, None
    except:
        return None, None

# 🏛️ BIST 100
with grid_col2:
    f, d = hızlı_veri_cek("XU100.IS")
    if f:
        r = "#4ade80" if d >= 0 else "#f87171"
        st.markdown(f'<div class="market-box" style="border-top: 4px solid {r};"><span style="color:#a3a3a3; font-size:12px; font-weight:bold;">🏛️ BIST 100</span><br><span style="font-size:18px; font-weight:900; color:{r};">{f:,.2f}</span><br><span style="font-size:11px; font-weight:bold; color:{r};">{d:+.2f}%</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="market-box">🏛️ BIST 100<br><span style="color:#a3a3a3;">Yükleniyor...</span></div>', unsafe_allow_html=True)

# 🚀 BIST 30
with grid_col3:
    f, d = hızlı_veri_cek("XU030.IS")
    if f:
        r = "#4ade80" if d >= 0 else "#f87171"
        st.markdown(f'<div class="market-box" style="border-top: 4px solid {r};"><span style="color:#a3a3a3; font-size:12px; font-weight:bold;">🚀 BIST 30</span><br><span style="font-size:18px; font-weight:900; color:{r};">{f:,.2f}</span><br><span style="font-size:11px; font-weight:bold; color:{r};">{d:+.2f}%</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="market-box">🚀 BIST 30<br><span style="color:#a3a3a3;">Yükleniyor...</span></div>', unsafe_allow_html=True)

# ⚡ VİOP / Vadeli
with grid_col4:
    f_v, d_v = hızlı_veri_cek("F_XU0300226.IS")
    if not f_v:
        f_v, d_v = f, d
    if f_v:
        r = "#4ade80" if d_v >= 0 else "#f87171"
        st.markdown(f'<div class="market-box" style="border-top: 4px solid {r};"><span style="color:#a3a3a3; font-size:12px; font-weight:bold;">⚡ VİOP (Yakın Vade)</span><br><span style="font-size:18px; font-weight:900; color:{r};">{f_v:,.2f}</span><br><span style="font-size:11px; font-weight:bold; color:{r};">{d_v:+.2f}%</span></div>', unsafe_allow_html=True)

st.markdown("---")

# --- ALT KATMAN: GÜVENLİ ÇOKLU HİSSE SEÇİMİ ---
st.markdown("### 🦅 Çoklu Hisse Sinyal ve Takip Radarı")

# Hafızadan beslenen multiselect (Sayfa yenilense de seçimler artık patlamaz)
secim = st.multiselect(
    "Takip etmek istediğiniz hisseleri seçin:",
    ["ASELS", "THYAO", "EKOS", "EREGL", "TUPRS", "FROTO", "BIMAS", "SASA"],
    default=st.session_state.secilen_hisseler
)
st.session_state.secilen_hisseler = secim

if st.session_state.secilen_hisseler:
    for hisse in st.session_state.secilen_hisseler:
        hisse_ticker = f"{hisse.upper().strip()}.IS"
        try:
            ticker = yf.Ticker(hisse_ticker)
            df = ticker.history(period="6mo")
            
            if not df.empty and len(df) >= 20:
                guncel_fiyat = df['Close'].iloc[-1]
                ma20 = df['Close'].rolling(window=20).mean().iloc[-1]
                
                # Basit RSI Hesaplama
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (gain / (loss + 1e-9)))).iloc[-1]
                
                with st.expander(f"📈 {hisse.upper()} - Güncel: {guncel_fiyat:.2f} TL"):
                    if rsi < 45 and guncel_fiyat > ma20:
                        st.markdown(f'<div class="main-signal" style="background-color: #1e3a24; color: #a2e8b2;">🟢 GÜVENLİ ALIM BÖLGESİ</div>', unsafe_allow_html=True)
                    elif rsi > 65:
                        st.markdown(f'<div class="main-signal" style="background-color: #44191c; color: #f8b4b7;">🔴 RİSKLİ / PAHALI BÖLGE</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="main-signal" style="background-color: #3e3113; color: #fada8a;">🟡 NÖTR / BEKLE GÖR</div>', unsafe_allow_html=True)
                    
                    c1, c2, c3 = st.columns(3)
                    c1.markdown(f'<div class="instruction-card">📥 Kapanış Fiyatı<br><span class="price-style" style="color:#4ade80;">{guncel_fiyat:.2f} TL</span></div>', unsafe_allow_html=True)
                    c2.markdown(f'<div class="instruction-card">🛡️ Destek / Stop<br><span class="price-style" style="color:#f87171;">{guncel_fiyat*0.97:.2f} TL</span></div>', unsafe_allow_html=True)
                    c3.markdown(f'<div class="instruction-card">🦅 21 Günlük Zirve<br><span class="price-style" style="color:#38bdf8;">{df["High"].tail(21).max():.2f} TL</span></div>', unsafe_allow_html=True)
        except:
            st.warning(f"{hisse} verisi o an çekilemedi, bir sonraki döngüde tekrar denenecek.")
else:
    st.info("Lütfen takip etmek için yukarıdaki menüden hisse seçin.")