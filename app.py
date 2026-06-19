import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Sayfa Genişliği ve Başlık
st.set_page_config(page_title="Broker Otomatik Pusu & Karar Terminali", layout="wide")

st.markdown("# 🦅 Broker Otomatik Pusu & Karar Terminali")
st.write("Sadece hisse kodunu yazın; yapay zeka karneyi çıkarsın, hiç bilmeyen bile gönül rahatlığıyla karar versin.")
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

            # Dinamik Pusu Seviyeleri (Emirler için baz alınacak)
            destek_ana = aylik_en_dusuk * 1.02
            direnc_ana = aylik_en_yuksek
            stop_loss = destek_ana * 0.98

            # --- DİNAMİK KARNE SKORLAMA SİSTEMİ ---
            olumlu_puan = 0
            toplam_kriter = 4
            
            # Kriter 1: RSI Durumu
            if rsi_son < 45: olumlu_puan += 1
            # Kriter 2: Fiyat ve Ortalamalar ilişkisi
            if guncel_fiyat > ma20_son: olumlu_puan += 1
            # Kriter 3: Zirveye Uzaklık (Ucuzluk)
            if zirveye_uzaklik_yuzde > 15: olumlu_puan += 1
            # Kriter 4: Hacimli Alım Gücü
            if hacim_orani > 1.2 and yuzde_degisim > 0: olumlu_puan += 1

            st.markdown("### 📋 HİSSE YAPAY ZEKA KARNESİ & EMİR TALİMATI")
            
            # Puanlamaya göre renkli kutuları ve net işlem talimatlarını yakıyoruz
            if olumlu_puan >= 3:
                st.success(f"🟢 **GÜVENLİ BÖLGE (ALIM İÇİN UYGUN) - Skor: {olumlu_puan}/{toplam_kriter}** \n\n"
                           f"Borsadan hiç anlamayan biri bile bu hisseyi şu an gönül rahatlığıyla portföyüne ekleyebilir. \n\n"
                           f"🏁 **NET OYUN PLANI:** \n"
                           f"*   **Alım Yapılabilecek Seviye (Pusu):** {guncel_fiyat:.2f} TL (Mevcut fiyat kademeli alım için makul) \n"
                           f"*   **Tehlike Anında Kaçış (Stop-Loss):** {stop_loss:.2f} TL (Bu fiyatın altına sarkarsa kol kes, zararı büyütme) \n"
                           f"*   **Kâr Alıp Çıkacağın Zaman (Hedef Fiyat):** {direnc_ana:.2f} TL (Hisse buraya gelirse kârını al, vedalaş)")
            elif olumlu_puan == 2:
                st.warning(f"🟡 **DENGELİ / BEKLE GÖR BÖLGESİ - Skor: {olumlu_puan}/{toplam_kriter}** \n\n"
                           f"Şu an ne çok ucuz ne çok pahalı. Acele edip bodoslama dalmayın. \n\n"
                           f"🏁 **NET OYUN PLANI:** \n"
                           f"*   **Alım Yapılabilecek Seviye (Pusu):** {destek_ana:.2f} TL (Fiyatın buraya biraz daha gevşemesini beklersen riskin sıfırlanır) \n"
                           f"*   **Tehlike Anında Kaçış (Stop-Loss):** {stop_loss:.2f} TL (Destek altı kapanış stop gerektirir) \n"
                           f"*   **Kâr Alıp Çıkacağın Zaman (Hedef Fiyat):** {direnc_ana:.2f} TL (Zirve direncine doğru satış düşünülmeli)")
            else:
                st.error(f"🔴 **TEHLİKELİ BÖLGE (UZAK DUR / ALMA!) - Skor: {olumlu_puan}/{toplam_kriter}** \n\n"
                         f"DUR! Borsadan anlamıyorsanız bu aşamada bu hisseden kesinlikle uzak durmalısınız. Hisse tepeye yakın veya aşırı şişmiş durumda. \n\n"
                         f"🏁 **NET OYUN PLANI:** \n"
                         f"*   **Alım Yapılabilecek Seviye (Pusu):** ALMA! (Fiyat çok şişmiş, kesinlikle buradan maliyetlenme) \n"
                         f"*   **Eğer Elinde Varsa Kaçış (Stop-Loss):** {guncel_fiyat * 0.95:.2f} TL (Mevcut fiyatın %5 altına stop koy, terste kalma) \n"
                         f"*   **Kâr Alıp Çıkacağın Zaman (Hedef Fiyat):** {direnc_ana:.2f} TL (Zirve geçilemezse nakde dön)")

            st.markdown("---")

            # Durum Belirleme
            if guncel_fiyat >= direnc_ana * 0.97:
                tahta_durumu = "🚨 Zirve / Tepede"
                strateji = "🚨 DİKKATLİ OL! Hisse aylık zirve direncine dayanmış durumda. Buradan atlamak risklidir, düzeltme bekle."
            elif guncel_fiyat <= destek_ana * 1.03:
                tahta_durumu = "🏹 Pusu Bölgesinde"
                strateji = "🏹 PUSUDA AV ZAMANI! Hisse aylık dip destek seviyelerine yakın. Kademeli alım için ideal bölge."
            else:
                tahta_durumu = "⏳ Arafta / Dengede"
                strateji = "⏳ BEKLE GÖR! Hisse ne çok ucuz ne çok pahalı. Destek veya direnç kırılımlarına göre pozisyon al."

            if hacim_orani > 1.5 and yuzde_degisim > 0:
                balina_notu = "🐋 Hacim son 10 günün ortalamasını patlatmış ve fiyat yukarı gidiyor. Büyük oyuncular mal topluyor olabilir."
                balina_durum = "🟢 Para Girişi Var"
            elif hacim_orani > 1.5 and yuzde_degisim < 0:
                balina_notu = "⚠️ Yüksek hacimle fiyat aşağı basılıyor. Büyük oyuncular mal çıkıyor olabilir, dikkatli ol."
                balina_durum = "🔴 Para Çıkışı Var"
            else:
                balina_notu = "💤 Büyük oyuncular şu an tahtada agresif bir işlem yapmıyor, sakin seyir."
                balina_durum = "🟡 Sakin / Rutin"

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
                
                st.markdown("---")
                st.subheader("👥 Otomatik Hacim & Oyuncu Akış Analizi")
                st.write(f"**Tahta Hacim Durumu:** {balina_durum}")
                st.info(balina_notu)

            with sag_kolon:
                st.subheader("🎯 Otomatik Oyun Planı Raporu")
                st.info(strateji)
                st.write(f"**🏹 Otomatik Pusu Fiyatı (Ana Destek):** {destek_ana:.2f} TL")
                st.write(f"**🦅 Çıkman Gereken Fiyat (Ana Direnç):** {direnc_ana:.2f} TL")
                st.write(f"**🛡️ Risk Yönetimi (Stop-Loss):** {stop_loss:.2f} TL")
                
                st.markdown(f"##### 📋 {vade_turu} İçin Broker Notu")
                if vade_turu == "Kısa Vade (Trade)":
                    st.warning("⚠️ **Trade Notu:** RSI seviyesine, hacim patlamasına ve MA20 ortalamasına sadık kal. Stop-loss altında nakde geç.")
                elif vade_turu == "Orta Vade":
                    st.info("📅 **Orta Vade Notu:** MA50 ana kalendir. Hacimli kırılımlarda pusu fiyatına yakın kademeli maliyetlenilebilir.")
                else:
                    st.success("💎 **Uzun Vade Notu:** Kısa vadeli fiyat dalgalanmalarını ve günlük hacim çıkışlarını önemseme. Aylık dip bölgeleri toplama alanıdır.")

    except Exception as e:
        st.error(f"Sistem hesaplama yaparken bir hata oluştu: {e}")