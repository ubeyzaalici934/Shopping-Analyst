import streamlit as st
import pandas as pd
import plotly.express as px 
from analyzer import ShoppingAnalyzer

# 1. SAYFA AYARLARI
st.set_page_config(page_title="AI Shopping Analyst", layout="wide", page_icon="🛒")

# 2. ANALİZ VE HAFIZA 
@st.cache_resource
def get_analyzer():
    return ShoppingAnalyzer()

analyzer = get_analyzer()

if "rapor" not in st.session_state:
    st.session_state.rapor = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. ANA PANEL
st.title("🛒 AI Shopping Analyst")
st.subheader("Ürün linkini atın, saniyeler içinde analiz edelim.")
st.markdown("---")

# Link Girişi 
col_link, col_btn = st.columns([4, 1])
with col_link:
    product_url = st.text_input("Ürün Linki:", placeholder="https://www.trendyol.com/...", label_visibility="collapsed")
with col_btn:
    analyze_button = st.button("🚀 Analiz Et", use_container_width=True)

if analyze_button:
    if product_url:
        with st.spinner("Veriler toplanıyor ve AI tarafından işleniyor..."):
            # Geçici sahte veri
            sahte_yorumlar = """
                1. Ürün harika ama kalıpları kesinlikle dar. 1.80 boyundayım, L beden aldım kısa geldi.
                2. Kumaşı çok kaliteli, kışlık bir dokusu var ama hassas ciltlerde kaşınma yapabilir.
                3. Rengi fotoğraftakinden bir ton daha koyu geldi.
                4. Kargo 2 günde ulaştı, paketleme çok sağlamdı.
                5. 75 kilo civarındaysanız M beden tam oturuyor.
            """
            genel_profil = "Genel kullanıcı deneyimi analizi bekleyen müşteri."
            st.session_state.rapor = analyzer.urun_analiz_et(sahte_yorumlar, genel_profil)
            st.session_state.messages = []
    else:
        st.warning("Lütfen bir link yapıştırın.")

st.markdown("---")

# 4. SONUÇLAR 
if st.session_state.rapor:
    st.subheader("📊 Hızlı Karar Metrikleri")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Genel Puan", "8.2 / 10", "Yüksek")
    m2.metric("Fiyat/P", "7.5 / 10", "-0.5")
    m3.metric("Kargo", "9.5 / 10", "Mükemmel")
    m4.metric("Kalite", "9.0 / 10", "Üst Segment")

    st.markdown("---")

    col_rapor, col_grafik = st.columns([3, 2])

    with col_rapor:
        st.success("📝 AI Analiz Raporu")
        st.markdown(st.session_state.rapor)

    with col_grafik:
        st.info("📈 Ürün Karakteristiği")
        df = pd.DataFrame(dict(
            r=[8, 7, 9, 9, 6],
            theta=['Kalite','Fiyat','Hız','Paketleme','Beden Uyumu']))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # 5. SOHBET BÖLÜMÜ 
    st.subheader("💬 Kişiselleştirilmiş Soru-Cevap")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Bu ürün bana uygun mu? Soralım..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            cevap = analyzer.chat_ile_sor(prompt, st.session_state.rapor)
            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})