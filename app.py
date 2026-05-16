import streamlit as st
import pandas as pd
import plotly.express as px
from analyzer import ShoppingAnalyzer

st.set_page_config(page_title="Alışveriş Danışmanım Pro", layout="wide", page_icon="💎")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Arka planı ve genel yazıları tamamen koyu moda kilitliyoruz */
    .stApp {
        background-color: #0e1117 !important;
        font-family: 'Inter', sans-serif;
        color: #ffffff !important;
    }
    
    /* Ortalanmış Başlık (Karanlıkta Parlayan Saf Beyaz) */
    .hero-container {
        text-align: center;
        padding-top: 50px;
        margin-bottom: 40px;
    }
    .hero-title {
        font-size: 44px;
        font-weight: 800;
        color: #ffffff !important;
        letter-spacing: -1px;
    }
    
    /* Sekme (Tab) Başlıkları */
    [data-baseweb="tab"] * {
        color: #9aa0a6 !important; /* Aktif olmayan sekmeler gri */
    }
    [data-baseweb="tab"][aria-selected="true"] * {
        color: #FF4B4B !important; /* Aktif sekme kırmızı */
    }
    
    /* Koyu Mod Uyumlu Giriş Kutusu */
    div[data-testid="stTextInput"] input {
        background-color: #1a1c23 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 15px !important;
        height: 3em !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #888888 !important;
    }
    
    /* Grafit Siyahı Premium Kart Tasarımı */
    .metric-card {
        background-color: #161b22 !important; /* Arka plandan hafifçe ayrışan grafit tonu */
        padding: 26px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3); 
        border: 1px solid #30363d;
        text-align: center;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-title {
        font-size: 14px;
        color: #8b949e !important; /* Soft gri başlık */
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 36px;
        color: #FF4B4B !important; /* Kırmızı neon puanlar */
        font-weight: 800;
        margin-bottom: 12px;
    }
    .metric-desc {
        font-size: 13px;
        color: #c9d1d9 !important; /* Net okunan beyaz/gri alt metin */
        line-height: 1.5;
        margin: 0;
    }
    
    /* Koyu Mod Buton Tasarımı */
    .stButton>button { 
        border-radius: 25px; 
        background-color: #FF4B4B; 
        color: white; 
        font-weight: bold; 
        height: 3.5em; 
        box-shadow: 0 4px 12px rgba(255,75,75,0.3);
        border: none;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_init(): return ShoppingAnalyzer()
analyzer = get_init()

if "analiz_sonucu" not in st.session_state: st.session_state.analiz_sonucu = None
if "sohbet_gecmisi" not in st.session_state: st.session_state.sohbet_gecmisi = []

st.markdown('<div class="hero-container"><h1 class="hero-title">🛍️ Alışveriş Danışmanım Pro</h1></div>', unsafe_allow_html=True)

tab_single, tab_bench = st.tabs(["🔍 Ürün Analiz Raporu", "⚔️ Ürünleri Karşılaştır"])

with tab_single:
    col_space1, col_main, col_space2 = st.columns([1, 4, 1])
    with col_main:
        url = st.text_input("Linki Yapıştır", placeholder="Analiz edilecek ürünün linkini buraya bırakın...", label_visibility="collapsed")
        analiz_btn = st.button("🚀 Yorumları Derinlemesine Analiz Et", use_container_width=True)

    if st.session_state.analiz_sonucu or analiz_btn:
        if analiz_btn and url:
            with st.spinner("Yorum geçmişi taranıyor..."):
                comments = "Kalıp dar, kumaş iyi."
                st.session_state.analiz_sonucu = analyzer.urun_analiz_et(comments)
                st.session_state.sohbet_gecmisi = [] 
        
        if st.session_state.analiz_sonucu:
            res = st.session_state.analiz_sonucu
            st.divider()
            
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f'<div class="metric-card"><p class="metric-title">⭐ Genel Not</p><p class="metric-value">{res["puanlar"]["Genel Not"]["skor"]}/10</p><p class="metric-desc">{res["puanlar"]["Genel Not"]["neden"]}</p></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-card"><p class="metric-title">👔 Kumaş & Kalite</p><p class="metric-value">{res["puanlar"]["Kumaş & Kalite"]["skor"]}/10</p><p class="metric-desc">{res["puanlar"]["Kumaş & Kalite"]["neden"]}</p></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-card"><p class="metric-title">🚚 Kargo & Paket</p><p class="metric-value">{res["puanlar"]["Kargo & Paket"]["skor"]}/10</p><p class="metric-desc">{res["puanlar"]["Kargo & Paket"]["neden"]}</p></div>', unsafe_allow_html=True)
            with m4:
                st.markdown(f'<div class="metric-card"><p class="metric-title">💰 Fiyat & Performans</p><p class="metric-value">{res["puanlar"]["Fiyat & Performans"]["skor"]}/10</p><p class="metric-desc">{res["puanlar"]["Fiyat & Performans"]["neden"]}</p></div>', unsafe_allow_html=True)

            st.divider()

            st.markdown("### 📝 Özet Karar")
            st.info(res['ozet'])
            st.warning(f"⚠️ **Almadan Önce Bilmeniz Gereken:** {res['dikkat_edilmesi_gereken']}")

            st.divider()

            col_sol, col_sag = st.columns(2)
            with col_sol:
                st.success("### ✅ Neleri Sevdik?")
                for a in res['artilar']: st.markdown(f"• {a}")
                st.error("### ❌ Neleri Sevmedik?")
                for e in res['eksiler']: st.markdown(f"• {e}")
                
            with col_sag:
                st.markdown("### 📈 12 Aylık Memnuniyet Trendi")
                df = pd.DataFrame(res["zamanla_degisim"])
                fig_line = px.line(df, x="ay", y="skor", markers=True, color_discrete_sequence=['#FF4B4B'])
                
                fig_line.update_layout(
                    yaxis_range=[0, 10], 
                    template="plotly_dark", 
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(fixedrange=True, title="Aylar"),
                    yaxis=dict(fixedrange=True, title="Memnuniyet Skoru")
                )
                st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})

            st.divider()

            st.markdown("### 💬 Ürün Hakkında Yapay Zekaya Sor")
            for mesaj in st.session_state.sohbet_gecmisi:
                with st.chat_message(mesaj["role"]): st.write(mesaj["content"])
            
            if soru := st.chat_input("Örn: Boyum 1.80, L beden bana olur mu?"):
                st.session_state.sohbet_gecmisi.append({"role": "user", "content": soru})
                with st.chat_message("user"): st.write(soru)
                
                with st.chat_message("assistant"):
                    with st.spinner("Düşünüyorum..."):
                        cevap = analyzer.chat_ile_sor(soru, res['ozet'])
                        st.write(cevap)
                        st.session_state.sohbet_gecmisi.append({"role": "assistant", "content": cevap})
                st.rerun()

with tab_bench:
    st.subheader("⚔️ İki Ürünü Yan Yana Kıyasla")
    col_a, col_b = st.columns(2)
    with col_a: link_a = st.text_input("1. Ürünün Linki", placeholder="İlk linki yapıştırın...")
    with col_b: link_b = st.text_input("2. Ürünün Linki", placeholder="İkinci linki yapıştırın...")
    
    if st.button("🏆 Hangisi Daha Mantıklı?", use_container_width=True):
        if link_a and link_b:
            with st.spinner("Farklar hesaplanıyor..."):
                rapor = analyzer.kiyasla("Ürün A", "Ürün B")
                st.success("### 🧠 Hangisini Almalı?")
                st.write(rapor)
        else:
            st.warning("Lütfen iki linki de girin.")