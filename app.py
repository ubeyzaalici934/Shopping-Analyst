import streamlit as st
import pandas as pd
import plotly.express as px
import re  
from analyzer import ShoppingAnalyzer
from scraper import ham_metin_ayıkla

st.set_page_config(page_title="Alışveriş Danışmanım", layout="wide", page_icon="🛒", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');
    
    /* Genel tasarım ayarlamaları*/
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
    /* Sekmeler ve Link Giriş Kutusu */
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
    /* Puan kartları tasarım ve ayarları */
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
    /* Analiz butonu tasarım */            
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
    .custom-badge-pos {
        background-color: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        color: #10b981 !important;
        padding: 10px 16px;
        border-radius: 12px;
        margin-bottom: 8px;
        font-size: 14px;
    }
    .custom-badge-neg {
        background-color: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
        color: #ef4444 !important;
        padding: 10px 16px;
        border-radius: 12px;
        margin-bottom: 8px;
        font-size: 14px;
    }
    /* Yan Panel Emniyet ve Sıkıştırma Kodları */
    [data-testid="stSidebarResizer"] {
        display: none !important;
        pointer-events: none !important;
    } 
    .st-emotion-cache-kgp69n, .st-emotion-cache-1wrcr25 {
        cursor: default !important;
    }  
    [data-testid="stSidebarUserContent"] {
        padding-top: 1.5rem !important;
        padding-bottom: 0rem !important;
    } 
    [data-testid="stSidebarUserContent"] div.element-container {
        margin-bottom: 4px !important;
    }    
    [data-testid="stSidebarUserContent"] hr {
        margin-top: 8px !important;
        margin-bottom: 8px !important;
    }
    [data-testid="stSidebar"] h2 {
        margin-top: 0px !important;
        padding-top: 0px !important;
        font-size: 24px !important; 
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 0px !important;
        margin-top: -30px !important; 
    }
    div[data-testid="stSidebarBlockContainer"] {
        padding-top: 0px !important;
        margin-top: 0px !important;
    }
    [data-testid="stSidebar"] h2:first-of-type {
        margin-top: 0px !important;
        padding-top: 0px !important;
    }
    /* yan panel ok butonu tasarım */
    @keyframes neonPulse {
        0% { box-shadow: 0 0 8px rgba(99, 102, 241, 0.5); border-color: #6366f1; }
        50% { box-shadow: 0 0 22px rgba(99, 102, 241, 1); border-color: #818cf8; }
        100% { box-shadow: 0 0 8px rgba(99, 102, 241, 0.5); border-color: #6366f1; }
    }
    [data-testid="stSidebarCollapseButton"] button, 
    div[data-testid="collapsedControl"] button,
    [data-testid="collapsedControl"] {
        background-color: #1e1b4b !important; /* Koyu mor çekirdek */
        border: 2px solid #6366f1 !important; /* Kalınlaştırılmış parlak çerçeve */
        color: #ffffff !important; /* Oku bembeyaz yapar */
        border-radius: 50% !important; /* Tam yuvarlak yapı */
        animation: neonPulse 2s infinite ease-in-out !important; /* 💥 Durmaksızın parlar! */
        transition: all 0.3s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover, 
    div[data-testid="collapsedControl"] button:hover {
        transform: scale(1.15) !important;
        background-color: #4f46e5 !important;
        box-shadow: 0 0 30px rgba(99, 102, 241, 1) !important;
        animation: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Yan Panel
with st.sidebar:
    st.markdown("## Sistem Tanımı ")
    # Veri Kaynağı Seçici
    ops_mode = st.selectbox("Veri Kaynağı Seçimi:", ["Simülasyon Modu (Yerel HTML)", "Canlı Veri Modu (API Gateway)"])
    if ops_mode == "Canlı Veri Modu (API Gateway)":
        st.markdown("""
            <div style="text-align: justify; background-color: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.15); color: #60a5fa; padding: 14px; border-radius: 14px; font-size: 13px; line-height: 1.5; margin-top: 10px; margin-bottom: 10px;">
                🌐 <b>Üretim Aşamasında:</b> Sistem API Gateway üzerinden anlık veri çekmeye hazır mimariye geçer. Sunum stabilitesi ve teknik demo güvenliği için şu an yerel veri kümesi simülasyonu aktiftir.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Metodoloji:**")
    st.caption("Doğal Dil İşleme (NLP) Tabanlı Duygu Madenciliği & Karar Destek Sistemleri (DSS).")
    st.markdown("---")
    st.markdown("**Teknoloji:**")
    st.caption("Gemini 2.5 Flash LLM, Pydantic Veri Doğrulama, Streamlit Cloud Altyapısı.")
    st.markdown("---")
    st.markdown("**👥 Proje Ekibi:**")
    st.caption("* Hediye Ekinci  \n* Ümmü Beyza Alıcı")

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
if "kiyas_sonucu" not in st.session_state: st.session_state.kiyas_sonucu = None

st.markdown('<div class="brand-container"><h1 class="brand-title">ALIŞVERİŞ DANIŞMANIM</h1><p class="brand-subtitle">Ürün Analizi</p></div>', unsafe_allow_html=True)

tab_single, tab_bench = st.tabs(["📊 Analiz Raporu", "⚔️ Karşılaştırma Motoru"])

with tab_single:
    col_space1, col_main, col_space2 = st.columns([1, 4, 1])
    with col_main:
        url = st.text_input("Linki Yapıştır", placeholder="Trendyol ürün linkini buraya bırakın...", label_visibility="collapsed")
        analiz_btn = st.button("Ürünü Analiz Et", use_container_width=True)

    if analiz_btn and url:
        if api_hata_durumu:
            st.error("**Sistem Hatası:** `GEMINI_API_KEY` yüklenemedi!")
        else:
            with st.spinner("Yorum verileri analiz ediliyor..."):
                url_lower = url.lower()
                
                # 🚀 DÜZELTİLDİ: '1' ekleri tamamen temizlendi ve kontrol önceliği 2. dosyalara verildi
                if "krem2" in url_lower: hedef_dosya = "krem2.html"
                elif "krem" in url_lower: hedef_dosya = "krem.html"
                elif "elbise2" in url_lower: hedef_dosya = "elbise2.html"
                elif "elbise" in url_lower: hedef_dosya = "elbise.html"
                elif "telefon2" in url_lower: hedef_dosya = "telefon2.html"
                else: hedef_dosya = "telefon.html"

                scraper_sonuc = ham_metin_ayıkla(hedef_dosya)
                
                if scraper_sonuc["durum"] == "Başarılı":
                    zenginlestirilmis_metin = yorumlari_kurtar_ve_birlestir(hedef_dosya, scraper_sonuc["saf_metin"])
                    
                    if len(zenginlestirilmis_metin.strip()) == 0:
                        st.error(f"Dosya İçeriği Boş: '{hedef_dosya}' dosyasında okunabilir metin veya yorum yok.")
                    else:
                        st.session_state.analiz_sonucu = analyzer.urun_analiz_et(zenginlestirilmis_metin)
                        st.session_state.sohbet_gecmisi = []
                else:
                    st.error(f"Dosya Hatası: Sunum için gerekli '{hedef_dosya}' yerel veri kaynağı bulunamadı!")
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
                st.markdown(f'<div class="metric-card"><p class="metric-title">Genel</p><p class="metric-value">{res["puanlar"]["Genel"]["skor"]}</p><p class="metric-desc">{res["puanlar"]["Genel"]["neden"]}</p></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-card"><p class="metric-title">Kalite</p><p class="metric-value">{res["puanlar"]["Kalite"]["skor"]}</p><p class="metric-desc">{res["puanlar"]["Kalite"]["neden"]}</p></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-card"><p class="metric-title">Kargo</p><p class="metric-value">{res["puanlar"]["Kargo"]["skor"]}</p><p class="metric-desc">{res["puanlar"]["Kargo"]["neden"]}</p></div>', unsafe_allow_html=True)
            with m4:
                st.markdown(f'<div class="metric-card"><p class="metric-title">Fiyat & Performans</p><p class="metric-value">{res["puanlar"]["Fiyat & Performans"]["skor"]}</p><p class="metric-desc">{res["puanlar"]["Fiyat & Performans"]["neden"]}</p></div>', unsafe_allow_html=True)

            st.divider()

            st.markdown("### 📝 Özet Karar")
            st.info(res['ozet'])
            st.warning(f"⚠️ **Almadan Önce Bilmeniz Gereken:** {res['dikkat_edilmesi_gereken']}")

            st.divider()

            col_sol, col_sag = st.columns(2)
            with col_sol:
                st.success("### ✅ Olumlu Özellikler")
                for a in res.get('artilar', []):                
                    st.markdown(f'<div class="custom-badge-pos">✨ {a}</div>', unsafe_allow_html=True)
                st.error("### ❌ Olumsuz Özellikler")
                for e in res.get('eksiler', []): 
                    st.markdown(f'<div class="custom-badge-neg">⚠️ {e}</div>', unsafe_allow_html=True)                
           
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
                        st.info("Zaman trendi sütun yapısı çözümlenemedi.")
                else:
                    st.info("Anlamlı bir zaman trendi çıkarılamadı.")

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
                        cevap = analyzer.chat_ile_sor(soru, res)
                        st.write(cevap)
                        st.session_state.sohbet_gecmisi.append({"role": "assistant", "content": cevap})
                st.rerun()

with tab_bench:
    st.markdown('<h3 style="text-align: center; font-family: \'Space Grotesk\', sans-serif; color: #ffffff; margin-bottom: 20px;">⚔️ İki Farklı Ürünü Karşılaştır</h3>', unsafe_allow_html=True)    
    col_a, col_b = st.columns(2)
    with col_a: link_a = st.text_input("1. Ürünün Linki", placeholder="İlk linki bırakın...", key="bench_url_a")
    with col_b: link_b = st.text_input("2. Ürünün Linki", placeholder="İkinci linki bırakın...", key="bench_url_b")
    
    if st.button("Ürünleri Kıyasla", use_container_width=True):
        if link_a and link_b:
            if api_hata_durumu:
                st.error("**Sistem Hatası:** API yapılandırması eksik.")
            else:
                with st.spinner("İki ürünün farkları hesaplanıyor..."):
                    la_lower = link_a.lower()
                    
                    if "krem2" in la_lower: dosya_a = "krem2.html"
                    elif "krem" in la_lower: dosya_a = "krem.html"
                    elif "elbise2" in la_lower: dosya_a = "elbise2.html"
                    elif "elbise" in la_lower: dosya_a = "elbise.html"
                    elif "telefon2" in la_lower: dosya_a = "telefon2.html"
                    else: dosya_a = "telefon.html"
                    
                    lb_lower = link_b.lower()
                    if "krem2" in lb_lower: dosya_b = "krem2.html"
                    elif "krem" in lb_lower: dosya_b = "krem.html"
                    elif "elbise2" in lb_lower: dosya_b = "elbise2.html"
                    elif "elbise" in lb_lower: dosya_b = "elbise.html"
                    elif "telefon2" in lb_lower: dosya_b = "telefon2.html"
                    else: dosya_b = "telefon.html"
                    
                    sc_a = ham_metin_ayıkla(dosya_a)
                    sc_b = ham_metin_ayıkla(dosya_b)
                    
                    if sc_a["durum"] == "Başarılı" and sc_b["durum"] == "Başarılı":
                        zengin_metin_a = yorumlari_kurtar_ve_birlestir(dosya_a, sc_a["saf_metin"])
                        zengin_metin_b = yorumlari_kurtar_ve_birlestir(dosya_b, sc_b["saf_metin"])
                        
                        st.session_state.kiyas_sonucu = analyzer.kiyasla(str(zengin_metin_a), str(zengin_metin_b))
                    else:
                        st.error("Karşılaştırma için gerekli kaynak HTML dosyaları bulunamadı. Lütfen klasörde telefon.html/telefon2.html vb. dosyaların olduğundan emin olun.")
        else:
            st.warning("Lütfen iki ürünün de link alanlarını doldurun.")

    if st.session_state.kiyas_sonucu:
        bench_res = st.session_state.kiyas_sonucu
        
        if "hata" in bench_res:
            st.error(bench_res["hata"])
        else:
            st.markdown("### Ürün Kıyaslama Analizi")
            st.caption("Seçilen iki ürünün özellik matrisi üzerinden karşılaştırılması:")

            rows_html = ""
            for item in bench_res.get("matris", []):
                bg_a = "rgba(16, 185, 129, 0.08)" if item.get("urun_a_durum") == "pozitif" else "rgba(239, 68, 68, 0.08)"
                color_a = "#10b981" if item.get("urun_a_durum") == "pozitif" else "#ef4444"
                
                bg_b = "rgba(16, 185, 129, 0.08)" if item.get("urun_b_durum") == "pozitif" else "rgba(239, 68, 68, 0.08)"
                color_b = "#10b981" if item.get("urun_b_durum") == "pozitif" else "#ef4444"
                
                rows_html += f'<tr style="border-bottom: 1px solid #1f2335;"><td style="padding: 14px; font-weight: 600; color: #9ca3af;">{item.get("kriter_adi")}</td><td style="padding: 14px; background-color: {bg_a}; color: {color_a}; font-weight: bold;">{item.get("urun_a_deger")}</td><td style="padding: 14px; background-color: {bg_b}; color: {color_b}; font-weight: bold;">{item.get("urun_b_deger")}</td></tr>'

            comparison_table_html = f'<div style="overflow-x:auto;"><table style="width:100%; table-layout: fixed; border-collapse: collapse; background-color: #11131e; border: 1px solid #1f2335; border-radius: 16px; overflow: hidden; font-family: \'Inter\', sans-serif; color: #ffffff; font-size: 14px;"><thead><tr style="background-color: #1e1b4b; border-bottom: 2px solid #4338ca; text-align: left;"><th style="padding: 16px; font-family: \'Space Grotesk\', sans-serif; font-weight: 600; color: #a5b4fc; width: 20%;">Kıyaslama Kriterleri</th><th style="padding: 16px; font-family: \'Space Grotesk\', sans-serif; font-weight: 600; color: #ffffff; width: 40%;">Ürün 1 (Hedef Ürün)</th><th style="padding: 16px; font-family: \'Space Grotesk\', sans-serif; font-weight: 600; color: #ffffff; width: 40%;">Ürün 2 (Rakip Ürün)</th></tr></thead><tbody>{rows_html}</tbody></table></div>'
            st.markdown(comparison_table_html, unsafe_allow_html=True)
            
            st.markdown("#### 📌 Karşılaştırma Sonucu")
            col1, col2 = st.columns(2)

            with col1:
                for b_sol in bench_res.get('bulgular_sol', []):
                    st.markdown(f"* {b_sol}")

            with col2:
                for b_sag in bench_res.get('bulgular_sag', []):
                    st.markdown(f"* {b_sag}")

            report_html = f'<div style="background: linear-gradient(135deg, #1e1b4b 0%, #11131e 100%); border: 1px solid #4338ca; padding: 20px; border-radius: 18px; margin-top: 15px;"><h4 style="margin-top: 0px; font-family: \'Space Grotesk\', sans-serif; color: #a5b4fc; font-size: 15px;">🔮 REVIEWMIND NİHAİ KARAR DESTEK RAPORU</h4><p style="text-align: justify; color: #e5e7eb; font-size: 13.5px; line-height: 1.6; margin-bottom: 0px;"><b>Analitik Öneri:</b> {bench_res.get("nihai_oneri")}</p></div>'
            st.markdown(report_html, unsafe_allow_html=True)