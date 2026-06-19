import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Sayfa Genişliği ve Başlık
st.set_page_config(page_title="Broker Otomatik Pusu & Karar Terminali", layout="wide")

# CSS ile Görsel Özelleştirmeler
st.markdown("""
    <style>
    .stAlert {
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .big-signal {
        font-size: 24px !important;
        font-weight: bold !important;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🦅 Broker Otomatik Pusu & Karar Terminali")
st.write("Sıfır borsa bilgisiyle net karar verin: Yapay zeka sinyalleri tarar, yönü, destek/dirençli grafikleri tek bakışta önünüze serer.")
st.markdown("---")

# Kullanıcı Girişi
hisse_input = st.text_input("Hisse Kodu Yazın (Örn: ASELS, THYAO, PASEU, BASCM):", "ASELS").upper().strip()

if hisse_input and not hisse_input.endswith(".IS"):
    hisse_ticker = f"{hisse_input}.IS"
else:
    hisse_ticker = hisse_input

if hisse_input:
    try:
        # Veri Çekme
        ticker = yf.Ticker(hisse_ticker)
        df = ticker.history(period="1y")
        
        if df.empty:
            st.error(f"{hisse_input} için veri bulunamadı. Kodu doğru yazdığınızdan emin olun.")
        else:
            # Güncel Bilgiler
            guncel_fiyat = df['Close'].iloc[-1]
            onceki_kapanis = df['Close'].iloc[-2] if len(df) > 1 else guncel_fiyat
            yuzde_degisim = ((guncel_fiyat - onceki_kapanis) / onceki_kapanis) * 100
            guncel_hacim = df['Volume'].iloc[-1]
            
            # TEKNİK İNDİKATÖRLERİN HESAPLANMASI
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['MA50'] = df['Close'].rolling(window=50).mean()
            ma20_son = df['MA20'].iloc[-1]
            ma50_son = df['MA50'].iloc[-1]
            
            # RSI (14) Hesaplama
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / (loss + 1e-9)
            rsi = 100 - (100 / (1 + rs))
            rsi_son = rsi.iloc[-1]
            
            # Son 1 Aylık Fiyat Alanı
            son_ay_df = df.tail(21)
            aylik_en_yuksek = son_ay_df['High'].max()
            aylik_en_dusuk = son_ay_df['Low'].min()
            zirveye_uzaklik_yuzde = ((aylik_en_yuksek - guncel_fiyat) / aylik_en_yuksek) * 100
            
            # Hacim Analizi
            ort_hacim_10gun = df['Volume'].tail(10).mean()
            hacim_orani = guncel_hacim / (ort_hacim_10gun + 1e-9)

            # Dinamik Pusu Seviyeleri
            destek_ana = aylik_en_dusuk * 1.02
            direnc_ana = aylik_en_yuksek
            stop_loss = destek_ana * 0.98

            # Matematiksel Potansiyel Hesaplama
            potansiyel_kar = ((direnc_ana - guncel_fiyat) / guncel_fiyat) * 100
            potansiyel_zar = ((guncel_fiyat - stop_loss) / guncel_fiyat) * 100

            # --- OLUMLU PUAN HESAPLAMA ---
            olumlu_puan = 0
            if rsi_son < 45: olumlu_puan += 1
            if guncel_fiyat > ma20_son: olumlu_puan += 1
            if zirveye_uzaklik_yuzde > 15: olumlu_puan += 1
            if hacim_orani > 1.2 and yuzde_degisim > 0: olumlu_puan += 1

            # --- EN ÜSTTEKİ BORSA EĞİTMENİ TRAFİK IŞIĞI VE SKOR KARTI ---
            st.markdown("### 🚦 TRAFİK IŞIĞI SİNYALİ & YAPAY ZEKA KARNESİ")
            
            if olumlu_puan >= 3:
                st.markdown('<div class="big-signal" style="background-color: #d4edda; color: #155724; border: 2px solid #c3e6cb;">🟢 GEÇ (GÖNÜL RAHATLIĞIYLA ALINABİLİR BÖLGE)</div>', unsafe_allow_html=True)
                st.success(f"**EĞİTMEN RAPORU:** Bu hisse teknik olarak pusuya yatılacak ideal yerlerde. Risk minimum, kâr potansiyeli yüksek. \n\n"
                           f"🎯 **NE YAPMALI?** Aşağıdaki fiyatlardan kademeli alım emri girip hedefe gitmesini bekleyebilirsiniz. Hiç korkmanıza gerek yok.")
            elif olumlu_puan == 2:
                st.markdown('<div class="big-signal" style="background-color: #fff3cd; color: #856404; border: 2px solid #ffeeba;">🟡 YAVAŞLA / BEKLE (YENİ ALIM İÇİN UYGUN DEĞİL)</div>', unsafe_allow_html=True)
                st.warning(f"**EĞİTMEN RAPORU:** Hisse arafta kalmış. Ne tam dipte ne tam tepede. Buradan bodoslama girmek yazı tura atmaktır. \n\n"
                           f"🎯 **NE YAPMALI?** Elinizde varsa tutun ama yeni alım yapacaksanız acele etmeyin. Fiyatın 'Pusu Fiyatına' düşmesini sabırla bekleyin.")
            else:
                st.markdown('<div class="big-signal" style="background-color: #f8d7da; color: #721c24; border: 2px solid #f5c6cb;">🔴 DUR! KESİNLİKLE GİRİLMEZ (YÜKSEK RİSK / TUZAK)</div>', unsafe_allow_html=True)
                st.error(f"**EĞİTMEN RAPORU:** TEHLİKE! Hisse ya zirvede mal boşaltma aşamasında ya da indikatörler aşırı şişmiş. Buradan bu kağıdı alan birisi çok büyük ihtimalle terste kalır.")

            # --- NET EMİR VE TALİMAT KUTUSU ---
            st.markdown("#### 🎯 HİÇ BİLMEYENLER İÇIN NOKTA ATIŞI TALİMATLAR")
            col_e1, col_e2, col_e3 = st.columns(3)
            with col_e1:
                if olumlu_puan >= 3:
                    st.info(f"📥 **NEREDEN ALALIM?** \n\n**{guncel_fiyat:.2f} TL** seviyesinden şu an kademeli toplanabilir.")
                elif olumlu_puan == 2:
                    st.info(f"📥 **NEREDEN ALALIM?** \n\nŞu an alma. Fiyatın **{destek_ana:.2f} TL** pusu fiyatına inmesini bekle.")
                else:
                    st.info(f"📥 **NEREDEN ALALIM?** \n\n**SAKIN ALMA!** Fiyat çok şişmiş, burası intihar bölgesidir.")
            with col_e2:
                st.warning(f"🛡️ **KAYIP SINIRI (STOP-LESS):** \n\n**{stop_loss:.2f} TL**. Fiyat buraya düşer ve altında kalırsa inatlaşma, hemen sat çık.")
            with col_e3:
                st.success(f"🦅 **KÂR ALMA / ÇIKIŞ YERİ:** \n\n**{direnc_ana:.2f} TL** seviyesine geldiğinde görev tamamlanmıştır, satıp parayı cebine koy.")

            st.markdown("---")

            # Metrikleri Gösteren Çubuk (Termometre Mantığı)
            st.markdown("#### 🌡️ Hisse Konum Göstergesi (Neredeyiz?)")
            st.progress(min(max(int((guncel_fiyat - aylik_en_dusuk) / (aylik_en_yuksek - aylik_en_dusuk + 1e-9) * 100), 0), 100))
            st.caption(f"Sol Taraf: En Düşük ({aylik_en_dusuk:.2f} TL) ---------- Şuan Buradayız ({guncel_fiyat:.2f} TL) ---------- Sağ Taraf: En Yüksek ({aylik_en_yuksek:.2f} TL)")

            # --- PLOTLY DESTEK / DİRENÇ ÇİZGİLİ GRAFİK SİSTEMİ ---
            st.markdown("---")
            st.markdown("#### 📈 Strateji Çizgili Canlı Trend Grafiği")
            grafik_secimi = st.radio("Grafik Periyodu Seçin:", ["1 Günlük Kapanışlar (Son 1 Ay)", "Saatlik Hareketler (Son 1 Hafta)"], horizontal=True)

            # Grafik verisini hazırlama
            if "1 Günlük" in grafik_secimi:
                chart_df = df.tail(30)
                title_suffix = "(Günlük Veri - 1 Ay)"
            else:
                chart_df = ticker.history(period="7d", interval="1h")
                title_suffix = "(Saatlik Veri - 1 Hafta)"

            if not chart_df.empty:
                # Plotly Şekil Nesnesi Oluşturma
                fig = go.Figure()

                # Ana Fiyat Çizgisi
                fig.add_trace(go.Scatter(x=chart_df.index, y=chart_df['Close'], mode='lines', name='Hisse Fiyatı', line=dict(color='#1f77b4', width=3)))

                # Hedef / Direnç Çizgisi (Kırmızı)
                fig.add_shape(type="line", x0=chart_df.index[0], y0=direnc_ana, x1=chart_df.index[-1], y1=direnc_