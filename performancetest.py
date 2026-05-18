import time
import statistics
import os
from analyzer import ShoppingAnalyzer
from scraper import ham_metin_ayıkla

def performans_testi_baslat(test_sayisi=3):
    print("=" * 60)
    print("SİSTEM PERFORMANS VE LATENCY TESTİ BAŞLATILDI")
    print("=" * 60)
    
    # 1. API ve Analyzer Bağlantı Kontrolü
    try:
        analyzer = ShoppingAnalyzer()
        print("✅ Gemini API Bağlantısı ve Analyzer Yapısı Doğrulandı.")
    except Exception as e:
        print(f"❌ API Bağlantı Hatası: {e}")
        return

    # Test için kullanılacak yerel dosya
    test_dosyasi = "telefon1.html"
    if not os.path.exists(test_dosyasi):
        # Eğer telefon1.html yoksa klasördeki herhangi bir html'i seç
        html_dosyalari = [f for f in os.listdir('.') if f.endswith('.html')]
        if html_dosyalari:
            test_dosyasi = html_dosyalari[0]
        else:
            print("❌ Test için klasörde hiç HTML kaynak dosyası bulunamadı!")
            return

    print(f"📦 Test Metni Kaynağı: '{test_dosyasi}'")
    
    # Veriyi Scraper ile ayıklama süresini ölçüyoruz
    start_time = time.time()
    scraper_sonuc = ham_metin_ayıkla(test_dosyasi)
    scraper_latency = time.time() - start_time
    print(f"⏱️  Scraper HTML Ayıklama Süresi: {scraper_latency:.4f} saniye")
    
    if scraper_sonuc["durum"] != "Başarılı":
        print("❌ Scraper veriyi ayıklayamadı, test iptal edildi.")
        return

    saf_metin = scraper_sonuc["saf_metin"]
    karakter_sayisi = len(str(saf_metin))
    print(f"📊 İşlenecek Toplam Veri Boyutu: {karakter_sayisi} karakter")
    print(f"🔄 LLM Analiz Süreçleri Ölçülüyor ({test_sayisi} döngü çalıştırılacak)...")
    print("-" * 60)

    analiz_sureleri = []

    for i in range(1, test_sayisi + 1):
        print(f"Döngü {i}/{test_sayisi} çalışıyor...", end="", flush=True)
        
        loop_start = time.time()
        # Analyzer fonksiyonunu tetikliyoruz
        _ = analyzer.urun_analiz_et(saf_metin)
        loop_duration = time.time() - loop_start
        
        analiz_sureleri.append(loop_duration)
        print(f" -> Tamamlandı: {loop_duration:.2f} saniye")
        
        # API 429 hız sınırına takılmamak için döngüler arası kısa bir mola
        time.sleep(2)

    # 2. İstatistiksel Performans Analiz Hesaplamaları
    ortalama_sure = statistics.mean(analiz_sureleri)
    medyan_sure = statistics.median(analiz_sureleri)
    en_hizli = min(analiz_sureleri)
    en_yavas = max(analiz_sureleri)
    standart_sapma = statistics.stdev(analiz_sureleri) if len(analiz_sureleri) > 1 else 0.0
    
    # Karakter işleme hızı 
    isleme_hizi = karakter_sayisi / ortalama_sure

    # 3. PERFORMANS RAPOR ÇIKTISI
    print("\n" + "=" * 60)
    print("SİSTEM PERFORMANS ANALİZ RAPORU")
    print("=" * 60)
    print(f"⏱️  En Hızlı Yanıt Süresi (Min Gecikme) : {en_hizli:.2f} saniye")
    print(f"⏱️  En Yavaş Yanıt Süresi (Max Gecikme) : {en_yavas:.2f} saniye")
    print(f"📈 Ortalama İşlem Süresi (Mean Latency): {ortalama_sure:.2f} saniye")
    print(f"🎯 Medyan İşlem Süresi (Median)        : {medyan_sure:.2f} saniye")
    print(f"📉 Sistem Varyasyonu (Standart Sapma)  : {standart_sapma:.2f} saniye")
    print(f"⚡ Veri İşleme Kapasitesi (Throughput) : {isleme_hizi:.2f} karakter/saniye")
    
    print("-" * 60)
    if standart_sapma < 1.0:
        print("💡 Karar: Sistem kararlılığı YÜKSEK (Gecikme süreleri istikrarlı).")
    else:
        print("💡 Karar: Sistem kararlılığı DEĞİŞKEN (Ağ veya API kaynaklı dalgalanma mevcut).")
    print("=" * 60)

if __name__ == "__main__":
    # Testi 3 döngü üzerinden başlatıyoruz
    performans_testi_baslat(test_sayisi=3)