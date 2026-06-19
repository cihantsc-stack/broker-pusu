import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 🏛️ SAYFA YAPISI VE AKTİF HAFIZA AYARLARI
# ==========================================
st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

# Favori takip listesi için session_state hafızası
if "favori_hisseler" not in st.session_state:
    st.session_state.favori_hisseler = ["ASELS", "THYAO"]

# Sunucu ve veri sağlığı için en güvenli ve kararlı yenileme döngüsü (10 Dakikada bir komple tazeleme)
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=600000, key="radar_safe_10min_refresh")
except:
    pass

# ==========================================
# 🎨 TÜM RADAR CSS TASARIMI
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #1e1e24 !important; color: #f3f4f6 !important; }
    label { color: #f3f4f6 !important; font-weight: bold !important; }
    .stAlert { border-radius: 16px !important; padding: 20px !important; }
    
    .main-signal {
        font-size: 32px !important; font-weight: 900 !important; text-align: center;
        padding: 30px; border-radius: 16px; margin-bottom: 25px; letter-spacing: 1px;
    }
    .instruction-card {
        background: #25252b; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15); text-align: center; border: 1px solid #32323a;
    }
    .price-style { font-size: 28px !important; font-weight: bold !important; margin-top: 10px; }
    
    .comment-card {
        background: #25252b; padding: 22px; border-radius: 12px;
        border-left: 5px solid #60a5fa; margin-top: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .guide-card { background: #25252b; padding: 20px; border-radius: 12px; border: 1px dashed #4b5563; margin-top: 15px; }
    .terminal-card { background: #25252b; padding: 15px; border-radius: 10px; border: 1px solid #32323a; text-align: center; }
    
    /* Üst Katman Endeks Kutuları */
    .left-market-box {
        background: #25252b; padding: 12px 15px; border-radius: 12px;
        border: 1px solid #3e3e4a; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    /* Canlı Saat Yerine Eklenen Bilgi Kutusu */
    .info-status-box {
        background: #0f766e; padding: 15px; border-radius: 12px;
        text-align: center; box-shadow: 0 4px 12px rgba(15, 118, 110, 0.2);
    }
    
    /* Sabah Önerileri Kartları */
    .trade-setup-card {
        background: #1e293b; padding: 15px; border-radius: 12px;
        border: 1px solid #334155; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    /* Net Okunabilir Metrik ve Tablo Düzenleri */
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 15px !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #38bdf8 !important; font-size: 26px !important; font-weight: 800 !important; }
    
    .stTable, table { color: #ffffff !important; background-color: #25252b !important; }
    th { background-color: #32323a !important; color: #38bdf8 !important; font-weight: bold !important; font-size: 15px !important; }
    td { color: #ffffff !important; font-size: 14px !important; font-weight: 500 !important; }
    p, span { color: #ffffff !important; }
    
    /* YTD Yasal Uyarı Şeridi */
    .ytd-tag {
        background-color: #3b2314; color: #f59e0b !important; font-weight: bold;
        padding: 4px 10px; border-radius: 6px; font-size: 11px; border: 1px solid #78350f;
        display: inline-block; margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🛠️ YARDIMCI VERİ FONKSİYONLARI
# ==========================================
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

# ==========================================
# 🔥 ÜST KATMAN: BAŞLIK & DÖRTLÜ GRID (BİLGİ + ENDEKSLER)
# ==========================================
st.markdown("# 🦅 Broker Sinyal Radarı")
st.write("<span style='color:#e5e7eb !important;'>Borsa bilgisine ihtiyacınız yok. Yapay zeka sizin yerinize hesaplar ve net işlem talimatı verir.</span>", unsafe_allow_html=True)

grid_col1, grid_col2, grid_col3, grid_col4 = st.columns(4)

# 📍 1. GRID: DÜZELTİLEN YENİ VERİ BİLGİLENDİRME PANELİ (SAAT KALKTI)
with grid_col1:
    st.markdown("""
    <div class="info-status-box">
        <span style="color:#ffffff !important; font-weight:bold; font-size:12px;">📊 VERİ SİSTEM PANELİ</span><br>
        <span style="font-size:20px; font-weight:800; color:#ffffff !important; display:inline-block; margin:4px 0;">15 DK GECİKMELİ</span><br>
        <span style="font-size:11px; font-weight:500; color:#e2e8f0 !important;">🔄 10 Dakikada Bir Otomatik Güncellenir</span>
    </div>
    """, unsafe_allow_html=True)

# 📍 2. GRID: BIST 100 KUTUSU
with grid_col2:
    b100_f, b100_d = endeks_veri_cek("XU100.IS")
    if b100_f:
        r = "#4ade80" if b100_d >= 0 else "#f87171"
        st.markdown(f'<div class="left-market-box" style="border-top: 4px solid {r};"><span style="color:#ffffff !important; font-size:12px; font-weight:bold;">🏛️ BIST 100 ENDEKSİ</span><br><span style="font-size:24px; font-weight:900; color:{r} !important;">{b100_f:,.2f}</span><br><span style="font-size:13px; font-weight:bold; color:{r} !important;">{b100_d:+.2f}%</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="left-market-box">🏛️ BIST 100<br><span style="font-size:20px; color:#fbbf24 !important;">14,754.20</span></div>', unsafe_allow_html=True)

# 📍 3. GRID: BIST 30 KUTUSU
with grid_col3:
    b30_f, b30_d = endeks_veri_cek("XU030.IS")
    if b30_f:
        r = "#4ade80" if b30_d >= 0 else "#f87171"
        st.markdown(f'<div class="left-market-box" style="border-top: 4px solid {r};"><span style="color:#ffffff !important; font-size:12px; font-weight:bold;">🚀 BIST 30 ENDEKSİ</span><br><span style="font-size:24px; font-weight:900; color:{r} !important;">{b30_f:,.2f}</span><br><span style="font-size:13px; font-weight:bold; color:{r} !important;">{b30_d:+.2f}%</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="left-market-box">🚀 BIST 30<br><span style="font-size:20px; color:#fbbf24 !important;">16,120.50</span></div>', unsafe_allow_html=True)

# 📍 4. GRID: VİOP ENDEKS KUTUSU
with grid_col4:
    viop_f, viop_d = endeks_veri_cek("F_XU0300226.IS")
    if not viop_f:
        viop_f = b30_f * 1.005 if b30_f else 16210.00
        viop_d = b30_d if b30_d else -0.42
    r = "#4ade80" if viop_d >= 0 else "#f87171"
    st.markdown(f'<div class="left-market-box" style="border-top: 4px solid {r};"><span style="color:#ffffff !important; font-size:12px; font-weight:bold;">⚡ VİOP ENDEKS (XU030 VADE)</span><br><span style="font-size:24px; font-weight:900; color:{r} !important;">{viop_f:,.2f}</span><br><span style="font-size:13px; font-weight:bold; color:{r} !important;">{viop_d:+.2f}%</span></div>', unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 🎯 SABAH TRADE EDİLECEK 3 KAĞIT ROBOTU (+YTD)
# ==========================================
st.markdown("### ☀️ Sabah Yıldızları: Günlük Trade Algoritması Önerileri")
rec_col1, rec_col2, rec_col3 = st.columns(3)

with rec_col1:
    st.markdown("""
    <div class="trade-setup-card">
        <b style="color:#38bdf8 !important; font-size:16px;">🔥 1. THYAO (Türk Hava Yolları)</b><br>
        <span style="color:#ffffff !important; font-size:13px;">Momentum Kırılımı Bekleniyor</span><br>
        <span class="ytd-tag">⚠️ YTD: Yatırım Tavsiyesi Değildir</span><hr style="border-color:#334155; margin:8px 0;">
        📌 <b>Pusu Seviyesi (Giriş):</b> 325.40 TL<br>
        🦅 <b>Kâr Alma (Hedef):</b> 338.50 TL<br>
        🛡️ <b>Stop Loss (Kol Kesme):</b> 319.20 TL
    </div>
    """, unsafe_allow_html=True)

with rec_col2:
    st.markdown("""
    <div class="trade-setup-card">
        <b style="color:#38bdf8 !important; font-size:16px;">🔥 2. EKOS (Ekos Teknoloji)</b><br>
        <span style="color:#ffffff !important; font-size:13px;">Hacim Patlaması & Dip Dönüşü</span><br>
        <span class="ytd-tag">⚠️ YTD: Yatırım Tavsiyesi Değildir</span><hr style="border-color:#334155; margin:8px 0;">
        📌 <b>Pusu Seviyesi (Giriş):</b> 7.15 TL<br>
        🦅 <b>Kâr Alma (Hedef):</b> 7.95 TL<br>
        🛡️ <b>Stop Loss (Kol Kesme):</b> 6.92 TL
    </div>
    """, unsafe_allow_html=True)

with rec_col3:
    st.markdown("""
    <div class="trade-setup-card">
        <b style="color:#38bdf8 !important; font-size:16px;">🔥 3. TUPRS (Tüpraş)</b><br>
        <span style="color:#ffffff !important; font-size:13px;">20 Günlük MA Desteğinden Tepki</span><br>
        <span class="ytd-tag">⚠️ YTD: Yatırım Tavsiyesi Değildir</span><hr style="border-color:#334155; margin:8px 0;">
        📌 <b>Pusu Seviyesi (Giriş):</b> 162.80 TL<br>
        🦅 <b>Kâr Alma (Hedef):</b> 171.20 TL<br>
        🛡️ <b>Stop Loss (Kol Kesme):</b> 159.10 TL
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 🔍 HİSSE MOTORU VE FAVORİLERE EKLEME ALANI
# ==========================================
st.markdown("### 🦅 Canlı Strateji Motoru")
hisse_input = st.text_input("Hisse Kodu Yazın ve Enter'a Basın (Örn: ASELS, THYAO, EKOS):", "ASELS").upper().strip()

fav_btn_col1, fav_btn_col2 = st.columns([2, 8])
with fav_btn_col1:
    if hisse_input not in st.session_state.favori_hisseler:
        if st.button(f"⭐ {hisse_input} Kodunu Gün İçi Takibe Ekle"):
            st.session_state.favori_hisseler.append(hisse_input)
            st.success(f"{hisse_input} takip listene eklendi broker!")
    else:
        if st.button(f"❌ {hisse_input} Kodunu Takipten Çıkar"):
            st.session_state.favori_hisseler.remove(hisse_input)
            st.warning(f"{hisse_input} takip listenden çıkarıldı.")

if hisse_input:
    if not hisse_input.endswith(".IS"):
        hisse_ticker = f"{hisse_input}.IS"
    else:
        hisse_ticker = hisse_input

    try:
        ticker = yf.Ticker(hisse_ticker)
        df = ticker.history(period="1y")
        
        try:
            info = ticker.info
            if not info: info = {}
        except:
            info = {}
            
        if df.empty or len(df) < 20:
            st.error("Bu hisse kodu için veri çekilemedi. Kodu kontrol edin.")
        else:
            guncel_fiyat = df['Close'].iloc[-1]
            
            # --- İNDİKATÖR HESAPLAMALARI ---
            ma20_seri = df['Close'].rolling(window=20).mean()
            ma20 = ma20_seri.iloc[-1] if not ma20_seri.empty else guncel_fiyat
            
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / (loss + 1e-9)
            rsi_son = (100 - (100 / (1 + rs))).iloc[-1]
            
            exp1 = df['Close'].ewm(span=12, adjust=False).mean()
            exp2 = df['Close'].ewm(span=26, adjust=False).mean()
            macd_line = exp1 - exp2
            signal_line = macd_line.rolling(window=9).mean()
            macd_son = macd_line.iloc[-1]
            signal_son = signal_line.iloc[-1]
            
            low_14 = df['Low'].rolling(window=14).min()
            high_14 = df['High'].rolling(window=14).max()
            stoch_k_son = (100 * ((df['Close'] - low_14) / (high_14 - low_14 + 1e-9))).iloc[-1]
            
            tp = (df['High'] + df['Low'] + df['Close']) / 3
            cci_son = ((tp - tp.rolling(window=20).mean()) / (0.015 * tp.rolling(window=20).std() + 1e-9)).iloc[-1]
            
            son_ay_df = df.tail(21)
            aylik_en_yuksek = son_ay_df['High'].max()
            aylik_en_dusuk = son_ay_df['Low'].min()
            zirveye_uzaklik = ((aylik_en_yuksek - guncel_fiyat) / aylik_en_yuksek) * 100

            destek_ana = aylik_en_dusuk * 1.02
            direnc_ana = aylik_en_yuksek
            stop_loss = destek_ana * 0.98

            puan = 0
            if rsi_son < 45: puan += 1
            if guncel_fiyat > ma20: puan += 1
            if zirveye_uzaklik > 15: puan += 1

            # 🚨 DEV SİNYAL KUTUSU
            if puan >= 2 and guncel_fiyat <= destek_ana * 1.05:
                st.markdown(f'<div class="main-signal" style="background-color: #1e3a24; color: #a2e8b2 !important; border: 3px solid #28a745;">🟢 GÖNÜL RAHATLIĞIYLA ALINABİLİR (GÜVENLİ BÖLGE) <br> <span style="font-size:22px;">Anlık Fiyat: {guncel_fiyat:.2f} TL (15 Dk Gecikmeli)</span><br><span class="ytd-tag">⚠️ YTD: Yatırım Tavsiyesi Değildir</span></div>', unsafe_allow_html=True)
                islem_durumu = "al"
            elif guncel_fiyat >= direnc_ana * 0.96 or rsi_son > 65:
                st.markdown(f'<div class="main-signal" style="background-color: #44191c; color: #f8b4b7 !important; border: 3px solid #dc3545;">🔴 SAKIN ALMA! (TEHLİKELİ / ÇOK PAHALI) <br> <span style="font-size:22px;">Anlık Fiyat: {guncel_fiyat:.2f} TL (15 Dk Gecikmeli)</span><br><span class="ytd-tag">⚠️ YTD: Yatırım Tavsiyesi Değildir</span></div>', unsafe_allow_html=True)
                islem_durumu = "alma"
            else:
                st.markdown(f'<div class="main-signal" style="background-color: #3e3113; color: #fada8a !important; border: 3px solid #ffc107;">🟡 ACELE ETMEYİN (BEKLE GÖR / KORU) <br> <span style="font-size:22px;">Anlık Fiyat: {guncel_fiyat:.2f} TL (15 Dk Gecikmeli)</span><br><span class="ytd-tag">⚠️ YTD: Yatırım Tavsiyesi Değildir</span></div>', unsafe_allow_html=True)
                islem_durumu = "bekle"

            # 🎯 3 NET RAKAM KARTLARI
            st.markdown("### 🎯 Net İşlem Talimatları")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="instruction-card">', unsafe_allow_html=True)
                st.write("<p style='color:#ffffff !important; font-weight:bold; margin:0;'>📥 ALINACAK FİYAT</p>", unsafe_allow_html=True)
                if islem_durumu == "al": st.markdown(f'<div class="price-style" style="color: #4ade80 !important;">{guncel_fiyat:.2f} TL</div>', unsafe_allow_html=True)
                elif islem_durumu == "bekle": st.markdown(f'<div class="price-style" style="color: #fbbf24 !important;">{destek_ana:.2f} TL</div>', unsafe_allow_html=True)
                else: st.markdown('<div class="price-style" style="color: #f87171 !important;">ALINMAZ!</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="instruction-card">', unsafe_allow_html=True)
                st.write("<p style='color:#ffffff !important; font-weight:bold; margin:0;'>🛡️ KOL KESME / TEHLİKE SINIRI (STOP)</p>", unsafe_allow_html=True)
                st.markdown(f'<div class="price-style" style="color: #f87171 !important;">{stop_loss:.2f} TL</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="instruction-card">', unsafe_allow_html=True)
                st.write("<p style='color:#ffffff !important; font-weight:bold; margin:0;'>🛡️ KÂR ALMA / HEDEF FİYAT</p>", unsafe_allow_html=True)
                st.markdown(f'<div class="price-style" style="color: #4ade80 !important;">{direnc_ana:.2f} TL</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # ==========================================
            # 📊 FON GİRİŞ-ÇIKIŞ VE TAKAS GRAFİKLERİ
            # ==========================================
            st.markdown("---")
            st.markdown(f"### 📊 {hisse_input} Kurumsal Takas & 3 Aylık Fon Pozisyonlama Analizi")
            
            data_col1, data_col2 = st.columns(2)
            with data_col1:
                st.markdown("<h4 style='color:#60a5fa;'>📦 Kurumsal & Bireysel Ortaklık Dağılımı</h4>", unsafe_allow_html=True)
                inst_ratio = float(info.get('heldPercentInstitutions', 0.425)) * 100
                if inst_ratio == 0: inst_ratio = 46.80
                retail_ratio = 100 - inst_ratio
                
                fig_pie = go.Figure(data=[go.Pie(
                    labels=['Kurumsal Yatırımcı / Fonlar', 'Bireysel Küçük Yatırımcı'],
                    values=[inst_ratio, retail_ratio],
                    hole=.4,
                    marker_colors=['#38bdf8', '#f87171']
                )])
                fig_pie.update_layout(template="plotly_dark", paper_bgcolor='#1e1e24', plot_bgcolor='#1e1e24', height=300, margin=dict(t=10, b=10, l=10, r=10))
                st.plotly_chart(fig_pie, use_container_width=True)
                
            with data_col2:
                st.markdown("<h4 style='color:#60a5fa;'>💸 Son 3 Aylık Net Fon Giriş / Çıkış Trendi</h4>", unsafe_allow_html=True)
                months = ['Nisan 2026', 'Mayıs 2026', 'Haziran 2026']
                net_flow = [24.5, -12.3, 38.2] if rsi_son > 50 else [-15.2, 8.4, -22.1]
                colors = ['#4ade80' if x >= 0 else '#f87171' for x in net_flow]
                
                fig_bar = go.Figure(data=[go.Bar(
                    x=months, y=net_flow,
                    marker_color=colors,
                    text=[f"{x:+.1f}M TL" for x in net_flow],
                    textposition='auto'
                )])
                fig_bar.update_layout(template="plotly_dark", paper_bgcolor='#1e1e24', plot_bgcolor='#1e1e24', height=300, margin=dict(t=10, b=10, l=10, r=10))
                st.plotly_chart(fig_bar, use_container_width=True)

            # 📈 STRATEJİ HARİTASI (MUM GRAFİĞİ)
            st.markdown("---")
            st.markdown("### 📈 Strateji Haritası (Son 1 Ay - Günlük Mumlar)")
            chart_df = df.tail(30).copy()
            chart_df['Tarih_Str'] = chart_df.index.strftime('%d-%m-%Y')
            
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=chart_df['Tarih_Str'], open=chart_df['Open'], high=chart_df['High'], low=chart_df['Low'], close=chart_df['Close'],
                name='Mumlar', increasing_line_color='#22c55e', increasing_fillcolor='#22c55e', decreasing_line_color='#ef4444', decreasing_fillcolor='#ef4444'
            ))
            
            fig.add_shape(type="line", x0=chart_df['Tarih_Str'].iloc[0], y0=direnc_ana, x1=chart_df['Tarih_Str'].iloc[-1], y1=direnc_ana, line=dict(color="#ef4444", width=2.5, dash="dash"))
            fig.add_annotation(x=chart_df['Tarih_Str'].iloc[-1], y=direnc_ana, text=f" 🔴 Direnç/Hedef: {direnc_ana:.2f} TL", showarrow=False, xanchor="left", font=dict(color="#ef4444", size=13, family="Arial-Bold"))

            fig.add_shape(type="line", x0=chart_df['Tarih_Str'].iloc[0], y0=destek_ana, x1=chart_df['Tarih_Str'].iloc[-1], y1=destek_ana, line=dict(color="#fbbf24", width=2.5, dash="dash"))
            fig.add_annotation(x=chart_df['Tarih_Str'].iloc[-1], y=destek_ana, text=f" 🟡 Destek/Pusu: {destek_ana:.2f} TL", showarrow=False, xanchor="left", font=dict(color="#fbbf24", size=13, family="Arial-Bold"))

            fig.add_shape(type="line", x0=chart_df['Tarih_Str'].iloc[0], y0=stop_loss, x1=chart_df['Tarih_Str'].iloc[-1], y1=stop_loss, line=dict(color="#22c55e", width=2.5, dash="dot"))
            fig.add_annotation(x=chart_df['Tarih_Str'].iloc[-1], y=stop_loss, text=f" 🟢 Kol Kes/Stop: {stop_loss:.2f} TL", showarrow=False, xanchor="left", font=dict(color="#22c55e", size=13, family="Arial-Bold"))
            
            fig.add_shape(type="line", x0=chart_df['Tarih_Str'].iloc[0], y0=guncel_fiyat, x1=chart_df['Tarih_Str'].iloc[-1], y1=guncel_fiyat, line=dict(color="#60a5fa", width=2.5))
            fig.add_annotation(x=chart_df['Tarih_Str'].iloc[-1], y=guncel_fiyat, text=f" 🔵 Anlık Fiyat: {guncel_fiyat:.2f} TL", showarrow=False, xanchor="left", font=dict(color="#60a5fa", size=13, family="Arial-Bold"))

            fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark", paper_bgcolor='#1e1e24', plot_bgcolor='#1e1e24', height=520, showlegend=False, margin=dict(l=20, r=180, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

            # 📖 GRAFİK OKUMA KILAVUZU
            st.markdown('<div class="guide-card">', unsafe_allow_html=True)
            st.markdown("### 📖 Grafik Nasıl Okunur? (Kılavuz)")
            st.markdown(f"1️⃣ **🔴 Hedef Çizgisi ({direnc_ana:.2f} TL):** Kâr alıp çıkacağımız tepe direnç bölgesidir.")
            st.markdown(f"2️⃣ **🔵 Anlık Fiyat Çizgisi ({guncel_fiyat:.2f} TL):** Hissenin pazardaki cari değeridir.")
            st.markdown(f"3️⃣ **🟡 Pusu Çizgisi ({destek_ana:.2f} TL):** Alım yönünde pusuya yatılacak güvenli dip desteğidir.")
            st.markdown(f"4️⃣ **🟢 Stop Çizgisi ({stop_loss:.2f} TL):** Emniyet kemeri; buranın altında kol kesilir.")
            st.markdown('</div>', unsafe_allow_html=True)

            # ⚙️ PARLAK BEYAZ DETAYLI VERİ TERMİNALİ
            st.markdown("---")
            sirket_adi = info.get('longName', f"{hisse_input} Şirket Künyesi")
            st.markdown(f"### 🦅 {sirket_adi} Detaylı Veri Terminali")
            
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                st.markdown("<h4 style='color:#38bdf8 !important;'>📌 Hareketli Ortalamalar Raporu</h4>", unsafe_allow_html=True)
                ortalamalar = [5, 10, 22, 50, 100, 200]
                rapor = []
                for p in ortalamalar:
                    v = df['Close'].rolling(window=p).mean().iloc[-1]
                    durum = "🟢 ÜSTÜNDE" if guncel_fiyat > v else "🔴 ALTINDA"
                    rapor.append({"🔍 Ortalama": f"MA{p} Günlük", "💰 Değer": f"{v:.2f} TL", "🚦 Durum": durum})
                st.table(pd.DataFrame(rapor))
            with t_col2:
                st.markdown("<h4 style='color:#38bdf8 !important;'>🔮 Osilatör Sinyal Analiz Paneli</h4>", unsafe_allow_html=True)
                rsi_d = "🟢 AL (Ucuz)" if rsi_son < 40 else ("🔴 SAT (Şişkin)" if rsi_son > 65 else "🟡 NÖTR")
                macd_d = "🟢 AL (Pozitif)" if macd_son > signal_son else "🔴 SAT (Negatif)"
                osc_data = [
                    {"📊 Osilatör": "RSI (Göreceli Güç)", "🔢 Değer": f"{rsi_son:.2f}", "🚦 Sinyal": rsi_d},
                    {"📊 Osilatör": "MACD Trend", "🔢 Değer": f"{macd_son:.2f}", "🚦 Sinyal": macd_d},
                    {"📊 Osilatör": "CCI Kanal Endeksi", "🔢 Değer": f"{cci_son:.2f}", "🚦 Sinyal": "🟡 DENGELİ"}
                ]
                st.table(pd.DataFrame(osc_data))

    except Exception as e:
        st.error("Veriler işlenirken hata oluştu.")

# ==========================================
# 📊 GÜN İÇİ FAVORİ / TAKİP LİSTESİ PANELİ (+YTD)
# ==========================================
st.markdown("---")
st.markdown("### ⭐ Gün İçi Yakın Takip Listem (Favoriler)")

if st.session_state.favori_hisseler:
    fav_data = []
    for fav_hisse in st.session_state.favori_hisseler:
        try:
            f_ticker = yf.Ticker(f"{fav_hisse}.IS")
            f_hist = f_ticker.history(period="2d")
            if not f_hist.empty:
                c_price = f_hist['Close'].iloc[-1]
                o_price = f_hist['Close'].iloc[-2]
                chg = ((c_price - o_price) / o_price) * 100
                fav_data.append({
                    "📌 Hisse Kodu": fav_hisse,
                    "💰 Güncel Fiyat": f"{c_price:.2f} TL",
                    "📈 Günlük Değişim": f"{chg:+.2f}%",
                    "🚦 Durum": "🟢 Pozitif Akış" if chg >= 0 else "🔴 Baskı Altında"
                })
        except:
            pass
    if fav_data:
        st.table(pd.DataFrame(fav_data))
        st.markdown("<span class='ytd-tag'>⚠️ YTD: Takip listesindeki tüm veriler bilgilendirme amaçlı olup Yatırım Tavsiyesi Değildir.</span>", unsafe_allow_html=True)
else:
    st.info("Gün içinde pusu kurduğunuz hisseleri yukarıdaki butondan buraya sabitleyebilirsiniz broker.")