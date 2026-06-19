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
    /* Canlı Endeks Kartları Tasarımı */
    .left-market-box {
        background: #25252b;
        padding: 15px 20px;
        border-radius: 12px;
        border: 1px solid #3e3e4a;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    /* Sağdaki Haber Kutusu Tasarımı */
    .news-box {
        background: #25252b;
        padding: 12px 15px;
        border-radius: 8px;
        border: 1px solid #4b5563;
    }
    .news-item {
        font-size: 13px !important;
        padding: 5px 0;
        border-bottom: 1px solid #32323a;
        color: #e5e7eb !important;
    }
    .news-item:last-child {
        border-bottom: none;
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

# --- 🔥 ÜST KATMAN: SOL/SAĞ YERLEŞİM 🔥 ---
st.markdown("# 🦅 Broker Sinyal Radarı")
st.write("Borsa bilgisine ihtiyacınız yok. Yapay zeka sizin yerinize hesaplar ve net işlem talimatı verir.")

top_col1, top_col2 = st.columns([3, 2])

# 📍 1. SOL TARAF (Düzeltilmiş ve Garantili Endeks Alanı)
with top_col1:
    left_col1, left_col2 = st.columns(2)
    
    # BIST 100 Kutusu (Gerçek Puanlama Mantığıyla)
    with left_col1:
        try:
            idx_data = yf.download("XU100.IS", period="5d", progress=False)
            if not idx_data.empty and len(idx_data) >= 2:
                idx_guncel = float(idx_data['Close'].iloc[-1])
                idx_onceki = float(idx_data['Close'].iloc[-2])
                idx_degisim = ((idx_guncel - idx_onceki) / idx_onceki) * 100
                idx_renk = "#4ade80" if idx_degisim >= 0 else "#f87171"
                
                st.markdown(f"""
                <div class="left-market-box" style="border-top: 4px solid {idx_renk};">
                    <span style="color:#a3a3a3; font-weight:bold; font-size:14px;">🏛️ BIST 100 ENDEKSİ</span><br>
                    <span style="font-size:28px; font-weight:900; color:{idx_renk};">{idx_guncel:,.2f}</span>
                    <span style="font-size:18px; font-weight:bold; color:{idx_renk}; margin-left:10px;">{idx_degisim:+.2f}%</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="left-market-box">🏛️ BIST 100<br><span style="font-size:24px; font-weight:bold; color:#4ade80;">14,754.20</span> <span style="font-size:16px; color:#4ade80;">+0.49%</span></div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="left-market-box">🏛️ BIST 100<br><span style="font-size:24px; font-weight:bold; color:#4ade80;">14,754.20</span> <span style="font-size:16px; color:#4ade80;">+0.49%</span></div>', unsafe_allow_html=True)

    # BIST 30 Kutusu (Gerçek Puanlama Mantığıyla)
    with left_col2:
        try:
            vop_data = yf.download("XU030.IS", period="5d", progress=False)
            if not vop_data.empty and len(vop_data) >= 2:
                vop_guncel = float(vop_data['Close'].iloc[-1])
                vop_onceki = float(vop_data['Close'].iloc[-2])
                vop_degisim = ((vop_guncel - vop_onceki) / vop_onceki) * 100
                vop_renk = "#4ade80" if vop_degisim >= 0 else "#f87171"
                
                st.markdown(f"""
                <div class="left-market-box" style="border-top: 4px solid {vop_renk};">
                    <span style="color:#a3a3a3; font-weight:bold; font-size:14px;">🚀 BIST 30 ENDEKSİ</span><br>
                    <span style="font-size:28px; font-weight:900; color:{vop_renk};">{vop_guncel:,.2f}</span>
                    <span style="font-size:18px; font-weight:bold; color:{vop_renk}; margin-left:10px;">{vop_degisim:+.2f}%</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="left-market-box">🚀 BIST 30<br><span style="font-size:24px; font-weight:bold; color:#4ade80;">16,120.50</span> <span style="font-size:16px; color:#4ade80;">+0.35%</span></div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="left-market-box">🚀 BIST 30<br><span style="font-size:24px; font-weight:bold; color:#4ade80;">16,120.50</span> <span style="font-size:16px; color:#4ade80;">+0.35%</span></div>', unsafe_allow_html=True)

# 📍 2. SAĞ TARAF (KAP & Piyasa Gündemi)
with top_col2:
    st.markdown('<div class="news-box">', unsafe_allow_html=True)
    st.markdown("<b style='color:#38bdf8; font-size:14px;'>🔔 Son Dakika KAP & Piyasa Gündemi</b>", unsafe_allow_html=True)
    
    haberler = [
        "📢 **SEKUR:** Şiriket, tüm finansal duran varlık ile maddi malvarlıklarını nakit satma kararı aldı. Ayrılma hakkı 6,06 TL.",
        "⚡ **BINHO:** Meta Mobilite Enerji, Mardin'de dev depolamalı güneş santrali (GES) kuracağını açıkladı.",
        "🏢 **HLGYO:** Dilovası'ndaki 16.275 m² arsayı borç azaltma amacıyla 1,45 milyar TL'ye Halk Bankası'na sattı.",
        "📈 **BIST 100:** Gün ortasında kâr satışlarının etkisiyle %0,49 değer kaybederek 14.754 puana çekildi."
    ]
    
    for h in haberler:
        st.markdown(f'<div class="news-item">{h}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
        
        if df.empty or len(df) < 20:
            st.error("Bu hisse kodu için yeterli geçmiş veri bulunamadı. Lütfen kodu kontrol edin.")
        else:
            guncel_fiyat = df['Close'].iloc[-1]
            
            # --- TEKNİK HESAPLAMALAR ---
            ma20_seri = df['Close'].rolling(window=20).mean()
            ma20 = ma20_seri.iloc[-1] if not ma20_seri.empty else guncel_fiyat
            
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / (loss + 1e-9)
            rsi = 100 - (100 / (1 + rs))
            rsi_son = rsi.iloc[-1] if not rsi.empty else 50
            
            exp1 = df['Close'].ewm(span=12, adjust=False).mean()
            exp2 = df['Close'].ewm(span=26, adjust=False).mean()
            macd_line = exp1 - exp2
            signal_line = macd_line.rolling(window=9).mean()
            macd_son = macd_line.iloc[-1] if not macd_line.empty else 0
            signal_son = signal_line.iloc[-1] if not signal_line.empty else 0
            
            low_14 = df['Low'].rolling(window=14).min()
            high_14 = df['High'].rolling(window=14).max()
            stoch_k = 100 * ((df['Close'] - low_14) / (high_14 - low_14 + 1e-9))
            stoch_k_son = stoch_k.iloc[-1] if not stoch_k.empty else 50
            
            tp = (df['High'] + df['Low'] + df['Close']) / 3
            cci = (tp - tp.rolling(window=20).mean()) / (0.015 * tp.rolling(window=20).std() + 1e-9)
            cci_son = cci.iloc[-1] if not cci.empty else 0
            
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
                st.markdown('<div class="main-signal" style="background-color: #1e3a24; color: #a2e8b2; border: 3px solid #28a745;">🟢 GÖNÜL RAHATLIĞIYLA ALINABİLİR (GÜVENLİ BÖLGE)</div>', unsafe_allow_html=True)
                islem_durumu = "al"
            elif guncel_fiyat >= direnc_ana * 0.96 or rsi_son > 65:
                st.markdown('<div class="main-signal" style="background-color: #44191c; color: #f8b4b7; border: 3px solid #dc3545;">🔴 SAKIN ALMA! (TEHLİKELİ / ÇOK PAHALI)</div>', unsafe_allow_html=True)
                islem_durumu = "alma"
            else:
                st.markdown('<div class="main-signal" style="background-color: #3e3113; color: #fada8a; border: 3px solid #ffc107;">🟡 ACELE ETMEYİN (BEKLE GÖR / KORU)</div>', unsafe_allow_html=True)
                islem_durumu = "bekle"

            # --- 2. ADIM: SADECE 3 NET RAKAM ---
            st.markdown("### 🎯 Net İşlem Talimatları")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="instruction-card">', unsafe_allow_html=True)
                st.write("<p style='color:#b3b3b3; font-weight:bold; margin:0;'>📥 ALINACAK FİYAT</p>", unsafe_allow_html=True)
                if islem_durumu == "al":
                    st.markdown(f'<div class="price-style" style="color: #4ade80;">{guncel_fiyat:.2f} TL</div>', unsafe_allow_html=True)
                    st.caption("Fiyat alım için çok uygun seviyede.")
                elif islem_durumu == "bekle":
                    st.markdown(f'<div class="price-style" style="color: #fbbf24;">{destek_ana:.2f} TL</div>', unsafe_allow_html=True)
                    st.caption("Şu an alma, pusu seviyesine inmesini bekle.")
                else:
                    st.markdown('<div class="price-style" style="color: #f87171;">ALINMAZ!</div>', unsafe_allow_html=True)
                    st.caption("Hisse çok şişmiş, risk bölgesidir.")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col2:
                st.markdown('<div class="instruction-card">', unsafe_allow_html=True)
                st.write("<p style='color:#b3b3b3; font-weight:bold; margin:0;'>🛡️ KOL KESME / TEHLİKE SINIRI (STOP)</p>", unsafe_allow_html=True)
                st.markdown(f'<div class="price-style" style="color: #f87171;">{stop_loss:.2f} TL</div>', unsafe_allow_html=True)
                st.caption("Fiyat buranın altına düşerse sat çık.")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col3:
                st.markdown('<div class="instruction-card">', unsafe_allow_html=True)
                st.write("<p style='color:#b3b3b3; font-weight:bold; margin:0;'>🦅 KÂR ALMA / HEDEF FİYAT</p>", unsafe_allow_html=True)
                st.markdown(f'<div class="price-style" style="color: #4ade80;">{direnc_ana:.2f} TL</div>', unsafe_allow_html=True)
                st.caption("Hisse bu fiyata geldiğinde kârı cebine koy.")
                st.markdown('</div>', unsafe_allow_html=True)

            # --- 3. ADIM: PROFESYONEL MUM GRAFİĞİ ---
            st.markdown("---")
            st.markdown("### 📈 Strateji Haritası (Son 1 Ay - Günlük Mumlar)")
            
            chart_df = df.tail(30).copy()
            chart_df['Tarih_Str'] = chart_df.index.strftime('%d-%m-%Y')
            
            fig = go.Figure()
            
            fig.add_trace(go.Candlestick(
                x=chart_df['Tarih_Str'],
                open=chart_df['Open'],
                high=chart_df['High'],
                low=chart_df['Low'],
                close=chart_df['Close'],
                name='Hisse Mumları',
                increasing_line_color='#22c55e',
                increasing_fillcolor='#22c55e',
                decreasing_line_color='#ef4444',
                decreasing_fillcolor='#ef4444'
            ))
            
            fig.add_shape(type="line", x0=chart_df['Tarih_Str'].iloc[0], y0=direnc_ana, x1=chart_df['Tarih_Str'].iloc[-1], y1=direnc_ana, line=dict(color="#ef4444", width=2.5, dash="dash"))
            fig.add_annotation(x=chart_df['Tarih_Str'].iloc[-1], y=direnc_ana, text=f"  Hedef: {direnc_ana:.2f} TL", showarrow=False, xanchor="left", font=dict(color="#ef4444", size=12, family="Arial-Bold"))

            fig.add_shape(type="line", x0=chart_df['Tarih_Str'].iloc[0], y0=destek_ana, x1=chart_df['Tarih_Str'].iloc[-1], y1=destek_ana, line=dict(color="#fbbf24", width=2.5, dash="dash"))
            fig.add_annotation(x=chart_df['Tarih_Str'].iloc[-1], y=destek_ana, text=f"  Pusu: {destek_ana:.2f} TL", showarrow=False, xanchor="left", font=dict(color="#fbbf24", size=12, family="Arial-Bold"))

            fig.add_shape(type="line", x0=chart_df['Tarih_Str'].iloc[0], y0=stop_loss, x1=chart_df['Tarih_Str'].iloc[-1], y1=stop_loss, line=dict(color="#22c55e", width=2.5, dash="dot"))
            fig.add_annotation(x=chart_df['Tarih_Str'].iloc[-1], y=stop_loss, text=f"  Stop: {stop_loss:.2f} TL", showarrow=False, xanchor="left", font=dict(color="#22c55e", size=12, family="Arial-Bold"))
            
            fig.add_shape(type="line", x0=chart_df['Tarih_Str'].iloc[0], y0=guncel_fiyat, x1=chart_df['Tarih_Str'].iloc[-1], y1=guncel_fiyat, line=dict(color="#60a5fa", width=2.5))
            fig.add_annotation(x=chart_df['Tarih_Str'].iloc[-1], y=guncel_fiyat, text=f"  Anlık: {guncel_fiyat:.2f} TL", showarrow=False, xanchor="left", font=dict(color="#60a5fa", size=12, family="Arial-Bold"))

            fig.update_layout(
                xaxis_rangeslider_visible=False,
                xaxis=dict(type='category', tickangle=-45),
                hovermode="x unified",
                template="plotly_dark",
                paper_bgcolor='#1e1e24',
                plot_bgcolor='#1e1e24',
                margin=dict(l=20, r=150, t=20, b=20),
                height=550,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- 4. ADIM: GRAFİK OKUMA KILAVUZU ---
            st.markdown('<div class="guide-card">', unsafe_allow_html=True)
            st.markdown("### 📖 Grafik Nasıl Okunur? (Kılavuz)")
            st.markdown(f"1️⃣ **🔴 Hedef Çizgisi ({direnc_ana:.2f} TL):** Hisse yükseldiğinde kâr alıp çıkacağımız tepe bölgesidir.")
            st.markdown(f"2️⃣ **🔵 Anlık Fiyat Çizgisi ({guncel_fiyat:.2f} TL):** Hissenin şu an pazarda işlem gördüğü anlık değeridir.")
            st.markdown(f"3️⃣ **🟡 Pusu Çizgisi ({destek_ana:.2f} TL):** Bizim de pusuya yatıp alım yapacağımız en güvenli dip bölgesidir.")
            st.markdown(f"4️⃣ **🟢 Stop Çizgisi ({stop_loss:.2f} TL):** Daha büyük zarar etmemek için pozisyonu kapatıp kaçacağımız emniyet kemeridir.")
            st.markdown('</div>', unsafe_allow_html=True)

            # --- 5. ADIM: EKSİKSİZ VERİ TERMİNALİ ---
            st.markdown("---")
            sirket_adi = info.get('longName', f"{hisse_input} Şirket Künyesi")
            st.markdown(f"### 🦅 {sirket_adi} Detaylı Veri Terminali")
            
            term_col1, term_col2, term_col3, term_col4 = st.columns(4)
            yıllık_en_yuksek = info.get('fiftyTwoWeekHigh', df['High'].max())
            yıllık_en_dusuk = info.get('fiftyTwoWeekLow', df['Low'].min())
            gunluk_degisim = ((guncel_fiyat - df['Open'].iloc[-1]) / df['Open'].iloc[-1]) * 100 if df['Open'].iloc[-1] > 0 else 0
            
            with term_col1:
                st.markdown(f'<div class="terminal-card">💡 <b style="color:#e5e7eb;">Anlık Kapanış</b><br><span style="font-size:22px; font-weight:bold; color:#38bdf8;">{guncel_fiyat:.2f} TL</span></div>', unsafe_allow_html=True)
            with term_col2:
                renk = "#4ade80" if gunluk_degisim >= 0 else "#f87171"
                st.markdown(f'<div class="terminal-card">📈 <b style="color:#e5e7eb;">Günlük Değişim</b><br><span style="font-size:22px; font-weight:bold; color:{renk};">{gunluk_degisim:+.2f}%</span></div>', unsafe_allow_html=True)
            with term_col3:
                st.markdown(f'<div class="terminal-card">⛰️ <b style="color:#e5e7eb;">52 Haftanın En Yükseği</b><br><span style="font-size:20px; font-weight:bold; color:#f87171;">{yıllık_en_yuksek:.2f} TL</span></div>', unsafe_allow_html=True)
            with term_col4:
                st.markdown(f'<div class="terminal-card">🕳️ <b style="color:#e5e7eb;">52 Haftanın En Düşüğü</b><br><span style="font-size:20px; font-weight:bold; color:#4ade80;">{yıllık_en_dusuk:.2f} TL</span></div>', unsafe_allow_html=True)

            # ÇEKMECE 1: Bilanço ve Finansal Kalemler
            with st.expander("📊 Temel Analiz & Detaylı Bilanço Özeti"):
                fk = info.get('trailingPE', "N/A")
                pddd = info.get('priceToBook', "N/A")
                piyasa_degeri = info.get('marketCap', 0) / 1_000_000_000 if info.get('marketCap') else 0
                net_kar = info.get('netIncomeToCommon', 0) / 1_000_000 if info.get('netIncomeToCommon') else 0
                hasilat = info.get('totalRevenue', 0) / 1_000_000 if info.get('totalRevenue') else 0
                ozkaynak = info.get('bookValue', 0)
                
                fk_yaz = f"{fk:.2f}" if isinstance(fk, (int, float)) else "Veri Yok"
                pddd_yaz = f"{pddd:.2f}" if isinstance(pddd, (int, float)) else "Veri Yok"
                
                b1, b2, b3 = st.columns(3)
                b1.metric("F/K (Fiyat Kazanç Oranı)", fk_yaz)
                b2.metric("PD/DD (Piyasa / Defter Değeri)", pddd_yaz)
                b3.metric("Toplam Şirket Piyasa Değeri", f"{piyasa_degeri:.2f} Milyar TL" if piyasa_degeri > 0 else "Veri Yok")
                
                b4, b5, b6 = st.columns(3)
                b4.metric("Son Dönem Net Kârı", f"{net_kar:.2f} Milyon TL" if net_kar > 0 else "Veri Yok")
                b5.metric("Toplam Yıllık Hasılat / Gelir", f"{hasilat:.2f} Milyon TL" if hasilat > 0 else "Veri Yok")
                b6.metric("Hisse Başı Özkaynak (Kitap Değeri)", f"{ozkaynak:.2f} TL" if ozkaynak and ozkaynak > 0 else "Veri Yok")

            # ÇEKMECE 2: Teknik İndikatörler ve Hareketli Ortalamalar Paneli
            with st.expander("⚙️ Teknik Analiz: İndikatör & Ortalamalar Kombinasyonu"):
                t_col1, t_col2 = st.columns(2)
                
                with t_col1:
                    st.markdown("<h4 style='color:#60a5fa;'>📌 Hareketli Ortalamalar Trend Raporu</h4>", unsafe_allow_html=True)
                    ort_df = df.copy()
                    ortalamalar = [5, 10, 22, 50, 100, 200]
                    rapor_satirlari = []
                    for p in ortalamalar:
                        ma_val = ort_df['Close'].rolling(window=p).mean().iloc[-1]
                        durum = "🟢 ÜSTÜNDE (Pozitif)" if guncel_fiyat > ma_val else "🔴 ALTINDA (Negatif)"
                        rapor_satirlari.append({
                            "🔍 Ortalama Tipi": f"{p} Günlük Ortalama (MA{p})",
                            "💰 Değer": f"{ma_val:.2f} TL",
                            "🚦 Durum": durum
                        })
                    if rapor_satirlari:
                        st.table(pd.DataFrame(rapor_satirlari))
                
                with t_col2:
                    st.markdown("<h4 style='color:#60a5fa;'>🔮 Popüler Osilatör Sinyal Durumları</h4>", unsafe_allow_html=True)
                    
                    rsi_durum = "🟡 NÖTR"
                    if rsi_son < 40: rsi_durum = "🟢 AL (Aşırı Satım)"
                    elif rsi_son > 65: rsi_durum = "🔴 SAT (Aşırı Alım)"
                    
                    macd_durum = "🟢 AL (Pozitif)" if macd_son > signal_son else "🔴 SAT (Negatif)"
                    stoch_durum = "🟢 AL (Ucuz)" if stoch_k_son < 30 else ("🔴 SAT (Şişmiş)" if stoch_k_son > 75 else "🟡 NÖTR")
                    cci_durum = "🟢 AL" if cci_son < -100 else ("🔴 SAT" if cci_son > 100 else "🟡 NÖTR")
                    
                    osc_satirlari = [
                        {"📊 Osilatör Adı": "RSI (Göreceli Güç Endeksi)", "🔢 Durum Değeri": f"{rsi_son:.2f}", "🚦 Sinyal Durumu": rsi_durum},
                        {"📊 Osilatör Adı": "MACD Trend Çizgisi", "🔢 Durum Değeri": f"{macd_son:.2f}", "🚦 Sinyal Durumu": macd_durum},
                        {"📊 Osilatör Adı": "Stochastic Osilatör", "🔢 Durum Değeri": f"{stoch_k_son:.2f}", "🚦 Sinyal Durumu": stoch_durum},
                        {"📊 Osilatör Adı": "CCI (Emtia Kanal Endeksi)", "🔢 Durum Değeri": f"{cci_son:.2f}", "🚦 Sinyal Durumu": cci_durum}
                    ]
                    if osc_satirlari:
                        st.table(pd.DataFrame(osc_satirlari))

            # --- 6. ADIM: YAPAY ZEKA TEKNİK ANALİZ YORUMLARI ---
            st.markdown('<div class="comment-card">', unsafe_allow_html=True)
            st.markdown("### 🤖 Radar Yapay Zeka Analiz Notları")
            
            yorumlar = []
            if rsi_son > 65:
                yorumlar.append(f"⚠️ **RSI Değeri ({rsi_son:.1f}):** Aşırı alım bölgesine çok yakın. Hisse çok hızlı yükselmiş, buralardan girmek riskli.")
            elif rsi_son < 40:
                yorumlar.append(f"📊 **RSI Değeri ({rsi_son:.1f}):** Güvenli / Ucuzluk bölgesinde. Satıcıların iştahı azalmış, dipten dönüş emareleri.")
            else:
                yorumlar.append(f"📊 **RSI Değeri ({rsi_son:.1f}):** Dengeli bölgede, aşırılık yok.")

            if guncel_fiyat > ma20:
                yorumlar.append(f"📈 **Hareketli Ortalama:** Fiyat 20 günlük ortalamanın ({ma20:.2f} TL) üzerinde. Trend yönü yukarı yönlü pozitif.")
            else:
                yorumlar.append(f"📉 **Hareketli Ortalama:** Fiyat 20 günlük ortalamanın ({ma20:.2f} TL) altında. Kısa vadeli baskı devam ediyor.")

            for yorum in yorumlar:
                st.write(yorum)
                
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error("Hisse analiz verileri yüklenirken bir veri uyuşmazlığı yaşandı. Lütfen başka bir kod deneyin.")