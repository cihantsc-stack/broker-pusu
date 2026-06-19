import streamlit as st
import yfinance as yf
import pandas as pd

# Sayfa Tasarımı
st.set_page_config(page_title="Broker Otomatik Pusu Terminali", layout="centered")
st.title("🦅 Broker Otomatik Pusu & Karar Terminali")
st.write("Sadece hisse kodunu yazın; fiyat, hacim, destek, direnç ve pusu seviyeleri otomatik hesaplansın.")
st.divider()

# Kullanıcı Girişi
hisse_girdi = st.text_input("Hisse Kodu Yazın (Örn: ASELS, THYAO, PASEU, BASCM):", value="ASELS").upper().strip()

# BIST için sonuna .IS ekleme mekanizması
if not hisse_girdi.endswith(".IS"):
    ticker_kod = f"{hisse_girdi}.IS"
else:
    ticker_kod = hisse_girdi

if hisse_girdi:
    try:
        with st.spinner("Piyasa verileri canlı çekiliyor..."):
            # Verileri Yahoo Finance üzerinden çekiyoruz
            hisse = yf.Ticker(ticker_kod)
            hist = hisse.history(period="1mo") # Son 1 aylık canlı veri paneli
            
        if not hist.empty:
            # Canlı Verileri Ayıklama
            guncel_fiyat = hist['Close'].iloc[-1]
            dunku_fiyat = hist['Close'].iloc[-2]
            gunluk_degisim = ((guncel_fiyat - dunku_fiyat) / dunku_fiyat) * 100
            son_hacim = hist['Volume'].iloc[-1]
            ortalama_hacim = hist['Volume'].mean()
            
            # Otomatik Destek / Direnç Hesaplama Motoru (Son 20 Günün Verisiyle)
            oto_destek = hist['Low'].tail(20).min()   # En güçlü pusu fiyatı
            oto_direnc = hist['High'].tail(20).max()  # En güçlü çıkış fiyatı
            
            # Ekranda Canlı Bilgi Kartları
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Güncel Fiyat", f"{guncel_fiyat:.2f} TL", f"{gunluk_degisim:.2f}%")
            with col2:
                # Hacim Durumu Kontrolü
                if son_hacim > ortalama_hacim:
                    hacim_durumu = "🔥 Hacim Yüksek"
                else:
                    hacim_durumu = "💤 Hacim Düşük"
                st.metric("Son Günlük Hacim", f"{son_hacim:,.0f}", hacim_durumu)
            with col3:
                # Pusu Durum Göstergesi
                if guncel_fiyat <= oto_destek * 1.05:
                    gosterge = "🍏 Pusu Bölgesinde"
                elif guncel_fiyat >= oto_direnc * 0.95:
                    gosterge = "🚨 Zirve / Tepede"
                else:
                    gosterge = "⏳ Dengeli Bölge"
                st.write(f"**Tahta Durumu:**\n\n {gosterge}")

            st.divider()
            
            # 🎯 OTOMATİK SİNYAL VE STRATEJİ RAPORU
            st.subheader("🎯 OTOMATİK OYUN PLANI RAPORU")
            
            # Karar Algoritması
            if guncel_fiyat <= oto_destek * 1.05:
                st.success(f"**STRATEJİ: 🍏 KUMBARAYA LOT ATMA GÜNÜ**\n\n{hisse_girdi} şu an ana destek hattına çok yakın. Güçlü kurumsallar buralardan mal toplar.")
            elif guncel_fiyat >= oto_direnc * 0.95:
                st.error(f"**STRATEJİ: 🚨 DİKKATLİ OL / ALMA!**\n\n{hisse_girdi} zirve direncine dayanmış durumda. Buradan atlamak risklidir, düzeltme bekle.")
            else:
                st.warning(f"**STRATEJİ: ⏳ PUSUDA BEKLE / İZLE**\n\nKağıt destek ile direnç arasında dengeleniyor. Acele etmeden pusu fiyatına yaklaşması beklenmeli.")
                
            # Otomatik Fiyat Seviyeleri Paneli
            st.write(f"📌 **Otomatik Pusu Fiyatı (Ana Destek):** {oto_destek:.2f} TL")
            st.write(f"📌 **Çıkman Gereken Fiyat (Ana Direnç):** {oto_direnc:.2f} TL")
            st.write(f"🛡️ **Risk Yönetimi (Stop-Loss - Destek %2 Altı):** {oto_destek * 0.98:.2f} TL")
            
        else:
            st.error("Hisse verileri çekilemedi. Kodun doğruluğunu kontrol edin (Örn: ASELS, THYAO).")
            
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")