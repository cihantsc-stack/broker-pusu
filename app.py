# 🎯 3 NET RAKAM KARTI - HİZALAMALI VE RENKLENDİRİLMİŞ
            st.markdown("### 🎯 Net İşlem Talimatları")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="instruction-card" style="height: 140px;">', unsafe_allow_html=True)
                st.write("<p style='color:#ffffff !important; font-weight:bold; margin-bottom:10px;'>📥 ALIM DURUMU</p>", unsafe_allow_html=True)
                if islem_durumu == "al":
                    st.markdown('<div style="font-size: 26px !important; font-weight: 900 !important; color: #22c55e !important;">ALINIR</div>', unsafe_allow_html=True)
                elif islem_durumu == "alma":
                    st.markdown('<div style="font-size: 26px !important; font-weight: 900 !important; color: #ef4444 !important;">ALINMAZ</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="font-size: 26px !important; font-weight: 900 !important; color: #fbbf24 !important;">BEKLE</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="instruction-card" style="height: 140px;">', unsafe_allow_html=True)
                st.write("<p style='color:#ffffff !important; font-weight:bold; margin-bottom:10px;'>🛡️ KOL KESME (STOP)</p>", unsafe_allow_html=True)
                st.markdown(f'<div style="font-size: 26px !important; font-weight: 900 !important; color: #ef4444 !important;">{stop_loss:.2f} TL</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col3:
                st.markdown('<div class="instruction-card" style="height: 140px;">', unsafe_allow_html=True)
                st.write("<p style='color:#ffffff !important; font-weight:bold; margin-bottom:10px;'>🦅 HEDEF FİYAT</p>", unsafe_allow_html=True)
                st.markdown(f'<div style="font-size: 26px !important; font-weight: 900 !important; color: #22c55e !important;">{direnc_ana:.2f} TL</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)