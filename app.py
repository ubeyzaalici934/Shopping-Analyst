import streamlit as st
import pandas as pd
import plotly.express as px
import re  
from analyzer import ShoppingAnalyzer
from scraper import ham_metin_ayıkla

st.set_page_config(page_title="Alışveriş Danışmanım", layout="wide", page_icon="🛒")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background-color: #0b0d13 !important;
        font-family: 'Inter', sans-serif;
        color: #f3f4f6 !important;
    }
    
    .brand-container {
        text-align: center;
        padding-top: 50px;
        margin-bottom: 30px;
    }
    .brand-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 52px;
        font-weight: 700;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .brand-subtitle {
        font-size: 14px;
        color: #6366f1 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    div[data-testid="stTabs"] {
        background-color: transparent !important;
    }
    div[data-baseweb="tab-list"] {
        justify-content: center !important; 
        gap: 15px !important;
        border-bottom: 1px solid #1f2937 !important;
        padding-bottom: 10px;
    }
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #9ca3af !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        padding: 10px 24px !important;
        border-radius: 20px !important;
        transition: all 0.3s ease !important;
        border: 1px solid transparent !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        background-color: #1e1b4b !important; 
        border: 1px solid #4338ca !important; 
    }
    
    div[data-testid="stTextInput"] > div {
        background-color: #11131e !important;
        border: 1px solid #222538 !important;
        border-radius: 16px !important; 
        padding: 4px 12px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[data-testid="stTextInput"] > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }
    div[data-testid="stTextInput"] input {
        color: #ffffff !important;
        font-size: 15px !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #4b5563 !important;
    }
    
    .metric-card {
        background-color: #11131e !important;
        padding: 26px;
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2); 
        border: 1px solid #1f2335;
        text-align: center;
        min-height: 190px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
    }
    .metric-title {
        font-size: 13px;
        color: #6b7280 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 38px;
        color: #6366f1 !important;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .metric-desc {
        font-size: 13px;
        color: #9ca3af !important;
        line-height: 1.5;
        margin: 0;
    }
    
    .stButton>button { 
        border-radius: 16px; 
        background: linear-gradient(90deg, #4f46e5 0%, #6366f1 100%) !important;
        color: white !important; 
        font-weight: 600 !important; 
        font-family: 'Space Grotesk', sans-serif !important;
        height: 3.4em; 
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.25) !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: scale(1.01);
        box-shadow: 0 4px 25px rgba(99, 102, 241, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

def yorumlari_kurtar_ve_birlestir(dosya_adi, scraper_metni):
    """
    scraper.py <script> etiketlerini sildiği için kaybolan yorumları,
    orijinal dosyadan regex ile bulup scraper metninin sonuna ekler.
    """
    try:
        with open(dosya_adi, "r", encoding="utf-8") as f:
            raw_html = f.read()
            
        yorumlar = re.findall(r'"comment"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"', raw_html)
        
        if yorumlar:
            gecerli_yorumlar = [f"• {y}" for y in yorumlar if len(y) > 10]
            ek_metin = "\n\n--- GERÇEK MÜŞTERİ YORUMLARI ---\n" + "\n".join(gecerli_yorumlar)
            return str(scraper_metni) + ek_metin
    except Exception:
        pass
    
    return str(scraper_metni)

try:
    analyzer = ShoppingAnalyzer()
    api_hata_durumu = False
except ValueError:
    api_hata_durumu = True
    
if "analiz_sonucu" not in st.session_state: st.session_state.analiz_sonucu = None
if "sohbet_gecmisi" not in st.session_state: st.session_state.sohbet_gecmisi = []

st.markdown('<div class="brand-container"><h1 class="brand-title">ALIŞVERİŞ DANIŞMANIM</h1><p class="brand-subtitle">Ürün Analizi</p></div>', unsafe_allow_html=True)

tab_single, tab_bench = st.tabs(["📊 Analiz Raporu", "⚔️ Karşılaştırma Motoru"])

with tab_single:
    col_space1, col_main, col_space2 = st.columns([1, 4, 1])
    with col_main:
        url = st.text_input("Linki Yapıştır", placeholder="Trendyol ürün linkini buraya bırakın...", label_visibility="collapsed")
        analiz_btn = st.button("Ürünü Analiz Et", use_container_width=True)

    if analiz_btn and url:
        if api_hata_durumu:
            st.error("🚨 **Sistem Hatası:** `GEMINI_API_KEY` yüklenemedi!")
        else:
            with st.spinner("Yorum verileri işleniyor ve analiz ediliyor..."):
                url_lower = url.lower()
                if "krem" in url_lower or "nemlendirici" in url_lower:
                    hedef_dosya = "krem.html"
                elif "elbise" in url_lower or "giyim" in url_lower:
                    hedef_dosya = "elbise.html"
                else:
                    hedef_dosya = "telefon.html"

                scraper_sonuc = ham_metin_ayıkla(hedef_dosya)
                
                if scraper_sonuc["durum"] == "Başarılı":
                    # SCRAPER'DAN GELEN METNE YORUMLARI ENJEKTE EDİYORUZ
                    zenginlestirilmis_metin = yorumlari_kurtar_ve_birlestir(hedef_dosya, scraper_sonuc["saf_metin"])
                    
                    if len(zenginlestirilmis_metin.strip()) == 0:
                        st.error(f"🚨 Dosya İçeriği Boş: '{hedef_dosya}' dosyasında okunabilir metin veya yorum yok.")
                    else:
                        st.session_state.analiz_sonucu = analyzer.urun_analiz_et(zenginlestirilmis_metin)
                        st.session_state.sohbet_gecmisi = []
                else:
                    st.error(f"🚨 Dosya Hatası: Sunum için gerekli '{hedef_dosya}' yerel veri kaynağı bulunamadı!")
                    st.session_state.analiz_sonucu = None
        
    # Rapor Gösterim Alanı
    if st.session_state.analiz_sonucu:
        res = st.session_state.analiz_sonucu
        
        if "hata" in res:
            st.error(f"{res['hata']}")
        else:
            st.divider()
            
            # Kartlar Alanı
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f'<div class="metric-card"><p class="metric-title">Genel Not</p><p class="metric-value">{res["puanlar"]["Genel Not"]["skor"]}</p><p class="metric-desc">{res["puanlar"]["Genel Not"]["neden"]}</p></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-card"><p class="metric-title">Kumaş & Kalite</p><p class="metric-value">{res["puanlar"]["Kumaş & Kalite"]["skor"]}</p><p class="metric-desc">{res["puanlar"]["Kumaş & Kalite"]["neden"]}</p></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-card"><p class="metric-title">Kargo & Paket</p><p class="metric-value">{res["puanlar"]["Kargo & Paket"]["skor"]}</p><p class="metric-desc">{res["puanlar"]["Kargo & Paket"]["neden"]}</p></div>', unsafe_allow_html=True)
            with m4:
                st.markdown(f'<div class="metric-card"><p class="metric-title">Fiyat & Performans</p><p class="metric-value">{res["puanlar"]["Fiyat & Performans"]["skor"]}</p><p class="metric-desc">{res["puanlar"]["Fiyat & Performans"]["neden"]}</p></div>', unsafe_allow_html=True)

            st.divider()

            st.markdown("### 📝 Özet Karar")
            st.info(res['ozet'])
            st.warning(f"⚠️ **Almadan Önce Bilmeniz Gereken:** {res['dikkat_edilmesi_gereken']}")

            st.divider()

            # Detaylar ve Grafik Yan Yana
            col_sol, col_sag = st.columns(2)
            with col_sol:
                st.success("### ✅ Olumlu Özellikler")
                for a in res['artilar']: st.markdown(f"• {a}")
                st.error("### ❌ Olumsuz Özellikler")
                for e in res['eksiler']: st.markdown(f"• {e}")
                
            with col_sag:
                st.markdown("### 📈 Müşteri Memnuniyet Grafiği")
                trend_verisi = res.get("zamanla_degisim", [])
                
                if isinstance(trend_verisi, list) and len(trend_verisi) > 0:
                    df = pd.DataFrame(trend_verisi)
                    if "ay" in df.columns and "skor" in df.columns:
                        fig_line = px.line(df, x="ay", y="skor", markers=True, color_discrete_sequence=['#6366f1'])
                        fig_line.update_layout(
                            yaxis_range=[0, 10], 
                            template="plotly_dark", 
                            plot_bgcolor="rgba(0,0,0,0)",
                            paper_bgcolor="rgba(0,0,0,0)",
                            xaxis=dict(fixedrange=True, title="Aylar"),
                            yaxis=dict(fixedrange=True, title="Skor")
                        )
                        st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
                    else:
                        st.info("📊 Zaman trendi sütun yapısı çözümlenemedi.")
                else:
                    st.info("📊 Anlamlı bir zaman trendi çıkarılamadı.")

            st.divider()

            # LLM Chat Katmanı
            st.markdown("### 💬 Asistana Sor")
            for mesaj in st.session_state.sohbet_gecmisi:
                with st.chat_message(mesaj["role"]): st.write(mesaj["content"])
            
            if soru := st.chat_input("Ürün hakkında bir soru sorun..."):
                st.session_state.sohbet_gecmisi.append({"role": "user", "content": soru})
                with st.chat_message("user"): st.write(soru)
                
                with st.chat_message("assistant"):
                    with st.spinner("Düşünüyorum..."):
                        cevap = analyzer.chat_ile_sor(soru, res['ozet'])
                        st.write(cevap)
                        st.session_state.sohbet_gecmisi.append({"role": "assistant", "content": cevap})
                st.rerun()

# --- TAB 2: KARŞILAŞTIRMA MOTORU ---
with tab_bench:
    st.subheader("⚔️ İki Farklı Ürünü Karşılaştır")
    col_a, col_b = st.columns(2)
    with col_a: link_a = st.text_input("1. Ürünün Linki", placeholder="İlk linki bırakın...", key="bench_url_a")
    with col_b: link_b = st.text_input("2. Ürünün Linki", placeholder="İkinci linki bırakın...", key="bench_url_b")
    
    if st.button("🏆 Analitiği Kıyasla", use_container_width=True):
        if link_a and link_b:
            if api_hata_durumu:
                st.error("🚨 **Sistem Hatası:** API yapılandırması eksik.")
            else:
                with st.spinner("İki ürünün semantik farkları hesaplanıyor..."):
                    la_lower = link_a.lower()
                    dosya_a = "krem.html" if "krem" in la_lower else ("elbise.html" if "elbise" in la_lower else "telefon.html")
                    
                    lb_lower = link_b.lower()
                    dosya_b = "krem.html" if "krem" in lb_lower else ("elbise.html" if "elbise" in lb_lower else "telefon.html")
                    
                    sc_a = ham_metin_ayıkla(dosya_a)
                    sc_b = ham_metin_ayıkla(dosya_b)
                    
                    if sc_a["durum"] == "Başarılı" and sc_b["durum"] == "Başarılı":
                        # İKİ DOSYA İÇİN DE YORUMLARI KURTARIYORUZ
                        zengin_metin_a = yorumlari_kurtar_ve_birlestir(dosya_a, sc_a["saf_metin"])
                        zengin_metin_b = yorumlari_kurtar_ve_birlestir(dosya_b, sc_b["saf_metin"])
                        
                        rapor = analyzer.kiyasla(str(zengin_metin_a), str(zengin_metin_b))
                        st.success("### 🧠 Yapay Zeka Karşılaştırma Raporu")
                        st.write(rapor)
                    else:
                        st.error("🚨 Karşılaştırma için gerekli kaynak HTML dosyaları bulunamadı.")
        else:
            st.warning("Lütfen iki ürünün de link alanlarını doldurun.")