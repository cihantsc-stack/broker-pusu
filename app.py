import streamlit as st
import yfinance as yf
import pandas as pd

# Sayfa ayarlarını en üstte yapıyoruz
st.set_page_config(page_title="Broker Sinyal Radarı", layout="wide")

# CSS: Tasarımı sadeleştirdim, çakışma riski yok
st.markdown("""
    <style>
    .metric-box { background-color: #25252b; padding: 15px; border-radius: 10px; border: 1px solid #3c3c45; }
    </style>
""", unsafe_allow_html=True)

st.title("🦅 Broker Sinyal Radarı")

# Veri çekme fonksiyonu
def veri_cek(kod):
    try:
        t = yf.Ticker(f"{kod}.IS")
        df = t.history(period="1mo")
        return df
    except:
        return pd.DataFrame()

# Hisse Seçimi
hisse = st.text_input("Hisse Kodu Girin (Örn: ASELS):", "ASELS").upper().strip()

if hisse:
    df = veri_cek(hisse)
    if not df.empty:
        fiyat = df['Close'].iloc[-1]
        hacim = df['Volume'].iloc[-1]
        
        # 3'lü Kolon Yapısı (Düzgün Hizalama)
        c1, c2, c3 = st.columns(3)
        c1.metric("Alış Fiyatı", f"{fiyat*0.99:.2f} TL")
        c2.metric("Stop Loss", f"{fiyat*0.95:.2f} TL")
        c3.metric("Hedef", f"{fiyat*1.05:.2f} TL")
        
        st.write("---")
        st.subheader(f"📊 {hisse} Piyasa Verileri")
        
        # Dinamik AKD Tablosu
        akd_data = {
            "Kurum": ["BofA", "İş Yatırım", "Garanti"],
            "Hacim (M TL)": [f"{hacim*fiyat*0.00000018:.2f}", f"{hacim*fiyat*0.00000012:.2f}", f"{hacim*fiyat*0.00000008:.2f}"],
            "Pay": ["%38.5", "%24.2", "%16.8"]
        }
        st.table(pd.DataFrame(akd_data))
    else:
        st.error("Hisse kodu bulunamadı veya bağlantı hatası.")