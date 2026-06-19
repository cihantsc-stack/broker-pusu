import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time

# Sayfa Yapısı
st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

# Zaman dilimi için korumalı kütüphane kontrolü
try:
    import pytz
    has_pytz = True
except ImportError:
    has_pytz = False

# Otomatik Yenileme (Sayfayı her 10 saniyede bir komple tetikler ve veriyi günceller)
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=10000, key="global_data_refresh")
except:
    pass

# CSS Düzenlemeleri
st.markdown("""
    <style>
    .stApp { background-color: #1e1e24 !important; color: #f3f4f6 !important; }
    label { color: #f3f4f6 !important; font-weight: bold !important; }
    .main-signal {
        font-size: 32px !important; font-weight: 900 !important; text-align: center;
        padding: 30px; border-radius: 16px; margin-bottom: 25px; letter-spacing: 1px;
    }
    .instruction-card {
        background: #25252b; padding: 20px; border-radius: 12px;
        text-align: center; border: 1px solid #32323a;
    }
    .price-style { font-size: 28px !important; font-weight: bold !important; margin-top: 10px; }
    .terminal-card { background: #25252b; padding: 15px; border-radius: 10px; border: 1px solid #32323a; text-align: center; }
    
    /* Endeks Kutuları Tasarımı */
    .market-box {
        background: #25252b; padding: 12px 15px; border-radius: 12px;
        text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.2); border: 1px solid #3e3e4a;
    }
    .time-box {
        background: #10b981; padding: 12px; border-radius: 12px;
        text-align: center; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🦅 Broker Sinyal Radarı")

# --- 🔥 ÜST KATMAN: CANLI AKAN SAAT & 3 ENDEKS (BIST100 - BIST30 - VİOP) 🔥 ---
grid_col1, grid_col2, grid_col3, grid_col4 = st.columns([1.5, 2, 2, 2])

# 🧭 SOL BAŞ: Saniye Saniye İlerleyen Dijital Saat
with grid_col1:
    if has_pytz:
        tz = pytz.timezone("Europe/Istanbul")
        su_an = datetime.now(tz)
    else:
        from datetime import timedelta
        su_an = datetime.utcnow() + timedelta(hours=3)
    
    saat_str = su_an.strftime("%H:%M:%S")
    
    st.markdown(f"""
    <div class="time-box">
        <span style="color:#ffffff; font-weight:bold; font-size:11px;">⏱️ CANLI SİSTEM SAATİ</span><br>
        <span style="font-size:26px; font-weight:900; color:#ffffff;">{saat_str}</span>
    </div>
    """, unsafe_allow_html=True)

# Verileri Çekme Fonksiyonu
def endeks_veri_cek(ticker_kod):
    try:
        t = yf.Ticker(ticker_kod)
        h = t.history(period="2d")
        if not h.empty and len(h) >= 2:
            guncel = h['Close'].iloc[-1]
            onceki = h['Close'].iloc[-2]
            degisim = ((guncel - onceki) / onceki) * 100
            return guncel, degisim
        return None, None
    except:
        return None, None

# 🏛️ BIST 100
with grid_col2:
    b100_f, b100_d = endeks_veri_cek("XU100.IS")
    if b100_f:
        renk = "#4ade80" if b100_d >= 0 else "#f87171"
        st.markdown(f'<div class="market-box" style="border-top: 4px solid {renk};"><span style="color:#a3a3a3; font-size:12px; font-weight:bold;">🏛️ BIST 100</span><br><span style="font-size:20px; font-weight:900; color:{renk};">{b100_f:,.2f}</span><br><span style="font-size:12px; font-weight:bold; color:{renk};">{b100_d:+.2f}%</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="market-box">🏛️ BIST 100<br><span style="font-size:18px; color:#a3a3a3;">Yükleniyor...</span></div>', unsafe_allow_html=True)

# 🚀 BIST 30
with grid_col3:
    b30_f, b30_d = endeks_veri_cek("XU030.IS")
    if b30_f:
        renk = "#4ade80" if b30_d >= 0 else "#f87171"
        st.markdown(f'<div class="market-box" style="border-top: 4px solid {renk};"><span style="color:#a3a3a3; font-size:12px; font-weight:bold;">🚀 BIST 30</span><br><span style="font-size:20px; font-weight:900; color:{renk};">{b30_f:,.2f}</span><br><span style="font-size:12px; font-weight:bold; color:{renk};">{b30_d:+.2f}%</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="market-box">🚀 BIST 30<br><span style="font-size:18px; color:#a3a3a3;">Yükleniyor...</span></div>', unsafe_allow_html=True)

# ⚡ VİOP (BIST 30 Yakın Vade Kontratı Yahoo Ticker'ı)
with grid_col4:
    viop_f, viop_d = endeks_veri_cek("F_XU0300226.IS")  # Yahoo Finans standart vadeli kontrat kodu
    if not viop_f:  # Eğer vadeli sembol değiştiyse yedek olarak ana endeksi göster
        viop_f, viop_d = b30_f, b30_d
    
    renk = "#4ade80" if viop_d >= 0 else "#f87171"
    st.markdown(f'<div class="market-box" style="border-top: 4px solid {renk};"><span style="color:#a3a3a3; font-size:12px; font-weight:bold;">⚡ VİOP (XU030 Vade)</span><br><span style="font-size:20px; font-weight:900; color:{renk};">{viop_f:,.2f}</span><br><span style="font-size:12px; font-weight:bold; color:{renk};">{viop_d:+.2f}%</span></div>', unsafe_allow_html=True)

st.markdown("---")

# --- 🔥 ALT KATMAN: ÇOKLU HİSSE SEÇİMİ VE ANLIK TAKİP LİSTESİ 🔥 ---
st.markdown("### 🦅 Çoklu Hisse Sinyal ve Takip Radarı")
secilen_hisseler = st.multiselect(
    "Takip etmek istediğiniz hisseleri seçin veya kodunu yazın:",
    ["ASELS", "THYAO", "EKOS", "EREGL", "TUPRS", "FROTO", "BIMAS", "SASA"],
    default=["ASELS", "THYAO", "EKOS"]
)

if secilen_hisseler:
    for hisse in secilen_hisseler:
        hisse_ticker = f"{hisse.upper().strip()}.IS"
        try:
            ticker = yf.Ticker(hisse_ticker)
            df = ticker.history(period="1y")
            
            if not df.empty and len(df) >= 20:
                guncel_fiyat = df['Close'].iloc[-1]
                
                # Sinyal Hesaplamaları (Hızlı Özet)
                ma20 = df['Close'].rolling(window=20).mean().iloc[-1]
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (gain / (loss + 1e-9)))).iloc[-1]
                
                with st.expander(f"📈 {hisse.upper()} - Anlık Fiyat: {guncel_fiyat:.2f} TL (Detayları Görmek İçin Tıklayın)"):
                    # Sinyal Durumu
                    if rsi < 45 and guncel_fiyat > ma20:
                        st.markdown(f'<div class="main-signal" style="background-color: #1e3a24; color: #a2e8b2; padding:15px; font-size:20px !important;">🟢 ALINABİLİR BÖLGE ({hisse.upper()})</div>', unsafe_allow_html=True)
                    elif rsi > 65:
                        st.markdown(f'<div class="main-signal" style="background-color: #44191c; color: #f8b4b7; padding:15px; font-size:20px !important;">🔴 SAKIN ALMA! (PAHALI) ({hisse.upper()})</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="main-signal" style="background-color: #3e3113; color: #fada8a; padding:15px; font-size:20px !important;">🟡 BEKLE GÖR / KORU ({hisse.upper()})</div>', unsafe_allow_html=True)
                    
                    # Kartlar
                    c1, c2, c3 = st.columns(3)
                    c1.markdown(f'<div class="instruction-card">📥 AL FİYATI<br><span class="price-style" style="color:#4ade80;">{guncel_fiyat:.2f} TL</span></div>', unsafe_allow_html=True)
                    c2.markdown(f'<div class="instruction-card">🛡️ STOP LOSS<br><span class="price-style" style="color:#f87171;">{guncel_fiyat*0.97:.2f} TL</span></div>', unsafe_allow_html=True)
                    c3.markdown(f'<div class="instruction-card">🦅 HEDEF FİYAT<br><span class="price-style" style="color:#38bdf8;">{df["High"].tail(21).max():.2f} TL</span></div>', unsafe_allow_html=True)
        except:
            pass
else:
    st.info("Lütfen takip etmek için yukarıdaki kutudan en az bir hisse seçin broker.")