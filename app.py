# 🎯 3 NET RAKAM KARTLARI (GÜNCEL RENK STRATEJİSİ)
            st.markdown("### 🎯 Net İşlem Talimatları")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="instruction-card">', unsafe_allow_html=True)
                st.write("<p style='color:#ffffff !important; font-weight:bold; margin:0;'>📥 ALIM DURUMU</p>", unsafe_allow_html=True)
                
                if islem_durumu == "al":
                    st.markdown(f'<div class="price-style" style="color: #4ade80 !important;">ALINIR</div>', unsafe_allow_html=True)
                elif islem_durumu == "alma":
                    st.markdown(f'<div class="price-style" style="color: #f87171 !important;">ALINMAZ</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="price-style" style="color: #fbbf24 !important;">BEKLE</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="instruction-card">', unsafe_allow_html=True)
                st.write("<p style='color:#ffffff !important; font-weight:bold; margin:0;'>🛡️ KOL KESME (STOP)</p>", unsafe_allow_html=True)
                st.markdown(f'<div class="price-style" style="color: #f87171 !important;">{stop_loss:.2f} TL</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col3:
                st.markdown('<div class="instruction-card">', unsafe_allow_html=True)
                st.write("<p style='color:#ffffff !important; font-weight:bold; margin:0;'>🦅 HEDEF FİYAT</p>", unsafe_allow_html=True)
                st.markdown(f'<div class="price-style" style="color: #4ade80 !important;">{direnc_ana:.2f} TL</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)