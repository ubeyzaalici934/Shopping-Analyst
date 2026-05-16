import os
from bs4 import BeautifulSoup

def ham_metin_ayıkla(dosya_adi):
    # Dosyanın bilgisayarda gerçekten var olup olmadığını kontrol ediyoruz
    if not os.path.exists(dosya_adi):
        return {"durum": "Hata", "mesaj": f"'{dosya_adi}' dosyası bulunamadı!"}
        
    try:
        with open(dosya_adi, "r", encoding="utf-8") as f:
            html_icerik = f.read()
            
        soup = BeautifulSoup(html_icerik, "html.parser")
        
        # Sayfadaki tüm gereksiz stil, script ve menü kodlarını siliyoruz (Gürültü Filtresi)
        for gereksiz in soup(["script", "style", "nav", "footer"]):
            gereksiz.decompose()
            
        # Sayfada kalan tüm düz yazıları (Metinleri) alt alta topluyoruz
        ham_metin = soup.get_text(separator="\n")
        
        # Satır aralarındaki gereksiz boşlukları temizliyoruz
        temiz_satirlar = [satir.strip() for satir in ham_metin.splitlines() if satir.strip()]
        saf_text = "\n".join(temiz_satirlar)
        
        return {
            "durum": "Başarılı",
            "saf_metin": saf_text,
            "karakter_sayisi": len(saf_text)
        }
            
    except Exception as e:
        return {"durum": "Hata", "mesaj": str(e)}


# --- TÜM DOSYALARI AYNI ANDA ÇALIŞTIRAN APARAT (TEST BÖLÜMÜ) ---
if __name__ == "__main__":
    print("==================================================")
    print("🚀 TOPLU AI VERİ HAZIRLAMA OPERASYONU BAŞLADI")
    print("==================================================")
    
    # İşlenecek tüm dosyaları bir liste haline getirdik
    hedef_dosyalar = ["telefon.html", "krem.html", "elbise.html"]
    
    # Python bu listenin içindeki dosyaları sırayla dönecek
    for dosya_adi in hedef_dosyalar:
        print(f"\n🔄 {dosya_adi} işleniyor...")
        
        sonuc = ham_metin_ayıkla(dosya_adi)
        
        if sonuc["durum"] == "Başarılı":
            print(f"✅ Başarılı! Veri Boyutu: {sonuc.get('karakter_sayisi')} karakter.")
            print("👇 Metinden İlk 3 Satır Örneği:")
            satirlar = sonuc["saf_metin"].split("\n")
            for i, satir in enumerate(satirlar[:3], 1):
                print(f"   {i}: {satir}")
        else:
            print(f"❌ Başarısız! Hata: {sonuc.get('mesaj')}")
            
    print("\n==================================================")
    print("🎉 Tüm veri setleri hazır! Arkadaşına pas atabilirsin.")
    print("==================================================")