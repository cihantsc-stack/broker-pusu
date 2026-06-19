import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Sayfa Genişliği ve Başlık
st.set_page_config(page_title="Broker Otomatik Pusu & Karar Terminali", layout="wide")

st.markdown("# 🦅 Broker Otomatik Pusu & Karar Terminali")
st.write("Sadece hisse kodunu yazın; fiyat, teknik göstergeler, kurumsal oyuncular ve pusu seviyeleri otomatik hesaplansın.")
st.markdown("---")

# Kullanıcı Girişi
hisse_input = st.text_input("Hisse Kodu Yazın (Örn: ASELS, THYAO, PASEU, BASCM):", "ASELS").upper().strip()

# Türkiye borsası için sonuna .IS ekleme kontrolü
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
            
            # Strateji Algoritması
            destek_ana = aylik_en_dusuk * 1.02
            direnc_ana = aylik_en_yuksek
            stop_loss = destek_ana * 0.98
            
            if guncel_fiyat >= direnc_ana * 0.97:
                tahta_durumu = "🚨 Zirve / Tepede"
                strateji = "🚨 DİKKATLİ OL / ALMA! Hisse aylık zirve direncine dayanmış durumda. Düzeltme bekle."
            elif guncel_fiyat <= destek_ana * 1.03:
                tahta_durumu = "🏹 Pusu Bölgesinde"
                strateji = "🏹 PUSUDA AV ZAMANI! Hisse aylık dip destek seviyelerine yakın. İdeal bölge."
            else:
                tahta_durumu = "⏳ Arafta / Dengede"
                strateji = "⏳ BEKLE GÖR! Hisse ne çok ucuz ne çok pahalı. Destek/direnç kırılımını izle."

            # Üst Metrikler Paneli
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(label="Güncel Fiyat", value=f"{guncel_fiyat:.2f} TL", delta=f"{yuzde_degisim:.2f}%")
            with col2:
                st.metric(label="Son Günlük Hacim", value=f"{guncel_hacim:,}")
            with col3:
                st.metric(label="Tahta Durumu", value=tahta_durumu)
            with col4:
                vade_turu = st.selectbox("🎯 İşlem Vadesi Seçin:", ["Kısa Vade (Trade)", "Orta Vade", "Uzun Vade"])

            st.markdown("---")
            
            # Ana Kolon Düzeni
            sol_kolon, sag_kolon = st.columns(2)
            
            with sol_kolon:
                st.subheader("📊 Teknik Göstergeler & İndikatörler")
                rsi_renk = "🟢 Güvenli" if rsi_son < 30 else ("🔴 Riskli" if rsi_son > 70 else "🟡 Nötr")
                st.write(f"**RSI (14):** {rsi_son:.2f} -> {rsi_renk}")
                st.write(f"**20 Günlük Hareketli Ortalama (MA20):** {ma20_son:.2f} TL")
                st.write(f"**50 Günlük Hareketli Ortalama (MA50):** {ma50_son:.2f} TL")
                
                st.markdown("##### 📅 Son 1 Aylık Fiyat Alanı")
                st.write(f"**En Yüksek (Zirve):** {aylik_en_yuksek:.2f} TL")
                st.write(f"**En Düşük (Dip):** {aylik_en_dusuk:.2f} TL")
                st.info(f"Hisse aylık zirvesinden **%{zirveye_uzaklik_yuzde:.2f}** aşağıda işlem görüyor.")
                
                # --- OTO OYUNCU / FON DAĞILIMI BÖLÜMÜ ---
                st.markdown("---")
                st.subheader("👥 Hissedeki Büyük Oyuncular & Kurumsal Fonlar")
                
                try:
                    # Yahoo'dan kurumsal yatırımcıları çekiyoruz
                    holders = ticker.institutional_holders
                    
                    if holders is not None and not holders.empty:
                        # Tablo sütunlarını Türkçeleştirip düzenliyoruz
                        holders_df = holders.copy()
                        if 'Holder' in holders_df.columns and 'pctHeld' in holders_df.columns:
                            holders_df['pctHeld'] = holders_df['pctHeld'] * 100 # Yüzde formatına çevir
                            holders_df.columns = ['Büyük Oyuncu / Kurumsal Fon', 'Hisse Adedi', 'Tarih', 'Pay Yüzdesi (%)']
                            st.dataframe(holders_df[['Büyük Oyuncu / Kurumsal Fon', 'Pay Yüzdesi (%)']], hide_index=True, use_container_width=True)
                        else:
                            st.dataframe(holders.head(5), use_container_width=True)
                    else:
                        # Eğer kurumsal fon yoksa büyük ortakları (mutual fund) dene
                        mf_holders = ticker.mutualfund_holders
                        if mf_holders is not None and not mf_holders.empty:
                            mf_df = mf_holders.copy()
                            if 'Holder' in mf_df.columns and 'pctHeld' in mf_df.columns:
                                mf_df['pctHeld'] = mf_df['pctHeld'] * 100
                                mf_df.columns = ['Yatırım Fonu / Ortak', 'Hisse Adedi', 'Tarih', 'Pay Yüzdesi (%)']
                                st.dataframe(mf_df[['Yatırım Fonu / Ortak', 'Pay Yüzdesi (%)']], hide_index=True, use_container_width=True)
                            else:
                                st.dataframe(mf_holders.head(5), use_container_width=True)
                        else:
                            st.info("ℹ️ Bu tahta için halka açık kurumsal büyük fon kırılımı bulunamadı (Genelde küçük tahtalarda boş döner).")
                except Exception as holder_err:
                    st.info("ℹ️ Büyük kurumsal fon verisi şu an çekilemedi, ana tahtalarda otomatik listelenecektir.")

            with sag_kolon:
                st.subheader("🎯 Otomatik Oyun Planı Raporu")
                st.info(strateji)
                st.write(f"**🏹 Otomatik Pusu Fiyatı (Ana Destek):** {destek_ana:.2f} TL")
                st.write(f"**🦅 Çıkman Gereken Fiyat (Ana Direnç):** {direnc_ana:.2f} TL")
                st.write(f"**🛡️ Risk Yönetimi (Stop-Loss):** {stop_loss:.2f} TL")
                
                st.markdown(f"##### 📋 {vade_turu} İçin Broker Notu")
                if vade_turu == "Kısa Vade (Trade)":
                    st.warning("⚠️ **Trade Notu:** RSI seviyesine ve MA20 ortalamasına sadık kal. Stop-loss altında saatlik kapanışta nakde geç.")
                elif vade_turu == "Orta Vade":
                    st.info("📅 **Orta Vade Notu:** MA50 ana kalendir. Pusu fiyatına yakın kademeli maliyetlenilebilir.")
                else:
                    st.success("💎 **Uzun Vade Notu:** Kısa vadeli fiyat dalgalanmalarını önemseme. Aylık dip bölgeleri toplama alanıdır.")

    except Exception as e:
        st.error(f"Sistem hesaplama yaparken bir hata oluştu: {e}")