import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Sayfa Yapısı
st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

# CSS ile Arka Planı Gri Yapma ve Elemanları Optimize Etme
st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e24 !important;
        color: #e3e3e6 !important;
    }
    label {
        color: #e3e3e6 !important;
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
            
            # Çizgiler ve Sabit Etiketler
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

            # --- 4. ADIM: EL YAZISI ŞEMAYA GÖRE GRAFİK OKUMA KILAVUZU ---
            st.markdown('<div class="guide-card">', unsafe_allow_html=True)
            st.markdown("### 📖 Grafik Nasıl Okunur? (Kılavuz)")
            
            st.markdown(f"1️⃣ **🔴 Hedef Çizgisi ({direnc_ana:.2f} TL):** Hisse yükseldiğinde kâr alıp çıkacağımız, satıcıların güçlü olduğu tepe bölgesidir.")
            st.markdown(f"2️⃣ **🔵 Anlık Fiyat Çizgisi ({guncel_fiyat:.2f} TL):** Hissenin şu an pazarda işlem gördüğü anlık değeridir. Mumların bittiği yeri gösterir.")
            st.markdown(f"3️⃣ **🟡 Pusu Çizgisi ({destek_ana:.2f} TL):** Hissenin geçmişte alıcı bulduğu, bizim de pusuya yatıp alım yapacağımız en güvenli dip bölgesidir.")
            st.markdown(f"4️⃣ **🟢 Stop Çizgisi ({stop_loss:.2f} TL):** İşler ters giderse, daha büyük zarar etmemek için pozisyonu kapatıp kaçacağımız emniyet kemeridir.")
            
            # Dinamik Kılavuz Özeti
            uzaklik_notu = ""
            if guncel_fiyat > destek_ana:
                fark_yuzde = ((guncel_fiyat - destek_ana) / destek_ana) * 100
                uzaklik_notu = f"Mavi anlık fiyat çizgisi, sarı pusu çizgisinin **%{fark_yuzde:.1f}** üzerinde duruyor."
            else:
                uzaklik_notu = "Mavi anlık fiyat çizgisi pusu seviyesinin altına sarkmış durumda."
                
            st.info(f"💡 **Mevcut Konum Özeti:** {uzaklik_notu} Çizgiler birbirine yaklaştıkça alım fırsatı doğar, kırmızı tepeye yaklaştıkça risk artar.")
            st.markdown('</div>', unsafe_allow_html=True)

            # --- 5. ADIM: YAPAY ZEKA TEKNİK ANALİZ YORUMLARI ---
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

            if zirveye_uzaklik > 15:
                yorumlar.append(f"🎯 **Zirve İskontosu:** Hisse son 1 ayın en yüksek seviyesine göre %{zirveye_uzaklik:.1f} aşağıda. Yeterince iskonto sağlamış durumda.")
            else:
                yorumlar.append(f"🚨 **Zirve İskontosu:** Hisse zirvesine sadece %{zirveye_uzaklik:.1f} uzaklıkta. Düzeltme riskini artırır.")

            for yorum in yorumlar:
                st.write(yorum)
                
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error("Veriler yüklenirken bir hata oluştu, lütfen kodu doğru yazdığınızdan emin olun.")