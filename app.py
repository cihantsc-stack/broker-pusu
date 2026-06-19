import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Sayfa Yapısı
st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

# CSS ile Ekranı Sadeleştirme ve Kutuları Büyütme
st.markdown("""
    <style>
    .reportview-container { background: #fafafa; }
    .stAlert { border-radius: 16px !important; padding: 20px !important; }
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
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #eaeaea;
    }
    .price-style {
        font-size: 28px !important;
        font-weight: bold !important;
        color: #111111;
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
            
            # Teknik Hesaplamalar (Arka Planda Gizli Çalışacak)
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
            direnc_ana = aylik_en_yuksek
            stop_loss = destek_ana * 0.98

            # Basit Puanlama
            puan = 0
            if rsi_son < 45: puan += 1
            if guncel_fiyat > ma20: puan += 1
            if zirveye_uzaklik > 15: puan += 1

            # --- 1. ADIM: DEV SİNYAL KUTUSU ---
            if puan >= 2 and guncel_fiyat <= destek_ana * 1.05:
                st.markdown('<div class="main-signal" style="background-color: #d4edda; color: #155724; border: 3px solid #28a745;">🟢 GÖNÜL RAHATLIĞIYLA ALINABİLİR (GÜVENLİ BÖLGE)</div>', unsafe_allow_html=True)
                islem_durumu = "al"
            elif guncel_fiyat >= direnc_ana * 0.96 or rsi_son > 65:
                st.markdown('<div class="main-signal" style="background-color: #f8d7da; color: #721c24; border: 3px solid #dc3545;">🔴 SAKIN ALMA! (TEHLİKELİ / ÇOK PAHALI)</div>', unsafe_allow_html=True)
                islem_durumu = "alma"
            else:
                st.markdown('<div class="main-signal" style="background-color: #fff3cd; color: #856404; border: 3px solid #ffc107;">🟡 ACELE ETMEYİN (BEKLE GÖR / KORU)</div>', unsafe_allow_html=True)
                islem_durumu = "bekle"

            # --- 2. ADIM: SADECE 3 NET RAKAM ---
            st.markdown("### 🎯 Net İşlem Talimatları")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="instruction-card">', unsafe_allow_html=True)
                st.write("📥 **ALINACAK FİYAT**")
                if islem_durumu == "al":
                    st.markdown(f'<div class="price-style" style="color: #28a745;">{guncel_fiyat:.2f} TL</div>', unsafe_allow_html=True)
                    st.caption("Fiyat şu an alım için çok uygun seviyede.")
                elif islem_durumu == "bekle":
                    st.markdown(f'<div class="price-style" style="color: #ffc107;">{destek_ana:.2f} TL</div>', unsafe_allow_html=True)
                    st.caption("Şu an alma, fiyatın bu seviyeye düşmesini bekle.")
                else:
                    st.markdown('<div class="price-style" style="color: #dc3545;">ALINMAZ!</div>', unsafe_allow_html=True)
                    st.caption("Hisse çok şişmiş, burası zarar etme bölgesidir.")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col2:
                st.markdown('<div class="instruction-card">', unsafe_allow_html=True)
                st.write("🛡️ **KOL KESME / TEHLİKE SINIRI (STOP)**")
                st.markdown(f'<div class="price-style" style="color: #721c24;">{stop_loss:.2f} TL</div>', unsafe_allow_html=True)
                st.caption("Fiyat buranın altına düşerse zarar büyümesin diye sat çık.")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col3:
                st.markdown('<div class="instruction-card">', unsafe_allow_html=True)
                st.write("🦅 **KÂR ALMA / HEDEF FİYAT**")
                st.markdown(f'<div class="price-style" style="color: #155724;">{direnc_ana:.2f} TL</div>', unsafe_allow_html=True)
                st.caption("Hisse bu fiyata geldiğinde kârını cebine koy, vedalaş.")
                st.markdown('</div>', unsafe_allow_html=True)

            # --- 3. ADIM: ANLIK FİYAT ÇİZGİLİ MUM GRAFİĞİ ---
            st.markdown("---")
            st.markdown("### 📈 Strateji Haritası (Son 1 Ay - Günlük Mumlar)")
            
            chart_df = df.tail(30)
            fig = go.Figure()
            
            # Mum Grafiği
            fig.add_trace(go.Candlestick(
                x=chart_df.index,
                open=chart_df['Open'],
                high=chart_df['High'],
                low=chart_df['Low'],
                close=chart_df['Close'],
                name='Hisse Mumları',
                increasing_line_color='#28a745',
                decreasing_line_color='#dc3545'
            ))
            
            # Strateji Çizgileri (Hedef, Pusu, Stop)
            fig.add_shape(type="line", x0=chart_df.index[0], y0=direnc_ana, x1=chart_df.index[-1], y1=direnc_ana, line=dict(color="Red", width=2, dash="dash"))
            fig.add_shape(type="line", x0=chart_df.index[0], y0=destek_ana, x1=chart_df.index[-1], y1=destek_ana, line=dict(color="Orange", width=2, dash="dash"))
            fig.add_shape(type="line", x0=chart_df.index[0], y0=stop_loss, x1=chart_df.index[-1], y1=stop_loss, line=dict(color="Green", width=2, dash="dot"))
            
            # 🔥 ANLIK FİYAT ÇİZGİSİ (Mavi renkte ince düz çizgi ve sağa etiket)
            fig.add_shape(type="line", x0=chart_df.index[0], y0=guncel_fiyat, x1=chart_df.index[-1], y1=guncel_fiyat, line=dict(color="#1f77b4", width=2))
            fig.add_annotation(x=chart_df.index[-1], y=guncel_fiyat, text=f"Anlık: {guncel_fiyat:.2f} TL", showarrow=False, xshift=15, yshift=0, font=dict(color="#1f77b4", size=12, family="Arial-Bold"))

            fig.update_layout(
                xaxis_rangeslider_visible=False,
                hovermode="x unified",
                template="plotly_white",
                margin=dict(l=20, r=20, t=20, b=20),
                height=450,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("Veriler yüklenirken geçici bir kesinti oluştu, lütfen az sonra tekrar deneyin.")