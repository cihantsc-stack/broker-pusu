# 🎯 3 NET RAKAM KARTI - YÜKSEK GÖRÜNÜRLÜKLÜ VE HİZALAMALI
st.markdown("### 🎯 Net İşlem Talimatları")

col1, col2, col3 = st.columns(3)

# 1. ALIM DURUMU KARTI
with col1:
    st.markdown('<div class="instruction-card" style="height: 140px; background-color: #25252b; border: 1px solid #4b5563; padding: 15px; border-radius: 12px;">', unsafe_allow_html=True)
    st.markdown("<p style='color:#ffffff !important; font-weight:bold; font-size:14px; margin-bottom:10px;'>📥 ALIM DURUMU</p>", unsafe_allow_html=True)
    if islem_durumu == "al":
        st.markdown('<div style="font-size: 24px !important; font-weight: 900 !important; color: #22c55e !important;">ALINIR</div>', unsafe_allow_html=True)
    elif islem_durumu == "alma":
        st.markdown('<div style="font-size: 24px !important; font-weight: 900 !important; color: #ef4444 !important;">ALINMAZ</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size: 24px !important; font-weight: 900 !important; color: #fbbf24 !important;">BEKLE</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 2. STOP KARTI
with col2:
    st.markdown('<div class="instruction-card" style="height: 140px; background-color: #25252b; border: 1px solid #4b5563; padding: 15px; border-radius: 12px;">', unsafe_allow_html=True)
    st.markdown("<p style='color:#ffffff !important; font-weight:bold; font-size:14px; margin-bottom:10px;'>🛡️ KOL KESME (STOP)</p>", unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 24px !important; font-weight: 900 !important; color: #ef4444 !important;">{stop_loss:.2f} TL</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 3. HEDEF KARTI
with col3:
    st.markdown('<div class="instruction-card" style="height: 140px; background-color: #25252b; border: 1px solid #4b5563; padding: 15px; border-radius: 12px;">', unsafe_allow_html=True)
    st.markdown("<p style='color:#ffffff !important; font-weight:bold; font-size:14px; margin-bottom:10px;'>🦅 HEDEF FİYAT</p>", unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 24px !important; font-weight: 900 !important; color: #22c55e !important;">{direnc_ana:.2f} TL</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)