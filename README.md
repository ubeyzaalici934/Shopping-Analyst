(!!!DÜZENLENECEK)
# Alışveriş Danışmanım

Alışveriş Danışmanım projesi, e-ticaret platformlarındaki karmaşık, manipüle edilmiş veya bilgi kirliliği içeren kullanıcı yorumlarını Doğal Dil İşleme ve Semantik Analiz yöntemleriyle filtreleyerek rasyonel bir satın alma kararı üretmeyi amaçlar. Bu sistem, özellikle tüketicilerin karar verme süreçlerinde yaşadığı aşırı bilgi yüklemesini azaltmayı ve çok kriterli karar analizi metodolojisiyle objektif bir özellik matrisi sunmayı hedefleyen bir çalışmadır.

Proje Ekibi:
-Hediye Ekinci
-Ümmü Beyza Alıcı

Projenin Amacı ve Temel Fonksiyonları:
-Sistem, geleneksel e-ticaret platformlarındaki yıldız puanlarının ve ham yorumların kronik ürün problemlerini gizleme eğilimini ortadan kaldırmak için belirli fonksiyonları yerine getirir. Kullancı aradığı verilere ulaşmak için yorumlarda gezmesi yerine direk web sitemizden aradğı özelliği sorabilir ve sistem yorumlar arasından aranan bilgiyi cımbızlayıp kullanıcıya ulaştırır.
-Semantik Duygu Madenciliği fonksiyonu ile reklam, kargo övgüsü veya anlamsız metinler ayıklanarak sadece gerçek kullanıcı deneyimlerine odaklanılır.
-Dinamik Kategori Matrisi sayesinde incelenen ürünün tipine göre tamamen dinamik kıyaslama kriterleri belirlenir.
-Çok Kriterli Karar Analizi tabanlı karar desteği ile iki alternatif, toplam fayda fonksiyonunu maksimize edecek şekilde analiz edilir ve nihai bir yönetici özeti raporu üretilir.
-Dinamik Raporlama ve Trend Analizi katmanı ile ürünün zaman içindeki müşteri memnuniyet trendi görsel grafiklerle sunulur ve entegre yapay zeka asistan katmanıyla kör noktalar aydınlatılır.

Simülasyon Mimarisi ve Yerel HTML Kullanımı:
Projenin teknik demo gösterimlerinde, e-ticaret platformlarının anlık IP engellemelerine ve hız sınırlarına takılmamak amacıyla yerel HTML simülasyon mimarisi kurgulanmıştır. Sistem, canlı web kazıma süreçlerini birebir taklit edecek şekilde önceden kazınmış ve yapılandırılmış yerel veri kümesi kaynaklarından beslenir. Bu yaklaşım internet bant genişliği dalgalanmalarını sıfıra indirerek sistemin net çalışma performansını ölçmemizi sağlar ve yapay zekanın veri işleme limitlerini sabit bir baseline üzerinden test etme imkanı tanır.

Kullanılabilecek Linkler:
-Krem linki: 
https://www.trendyol.com/dermokil/nemlendirici-ve-rahatlatici-etkili-dogal-aloe-vera-jel-300-ml-p-101770923?boutiqueId=61&merchantId=115550

Krem 2 linki:
https://www.trendyol.com/dove/nemlendirici-sivi-sabun-caring-1-4-nemlendirici-krem-etkili-450-ml-x3-adet-p-40433618?boutiqueId=61&merchantId=378048

Elbise linki: 
https://www.trendyol.com/hiccup/kalp-yaka-desenli-maxi-elbise-p-921394163?boutiqueId=61&merchantId=938209

Elbise 2 linki:
https://www.trendyol.com/grimelange/pani-aire-kadin-kayik-yaka-ustu-esnek-viskon-alt-kismi-genis-poplin-dokuma-kolsuz-siyah-elbise-p-897929300?boutiqueId=61&merchantId=165724 

Telefon linki: 
https://www.trendyol.com/apple/iphone-11-128-gb-beyaz-cep-telefonu-aksesuarsiz-kutu-apple-turkiye-garantili-p-64074794?boutiqueId=61&merchantId=185559
 
Telefon 2 linki: 
https://www.trendyol.com/samsung/galaxy-s23-256-gb-siyah-cep-telefonu-samsung-turkiye-garantili-p-635097874?boutiqueId=61&merchantId=657799

Teknolojik Altyapı:
+Arayüz katmanında özelleştirilmiş neon karanlık tema stil enjeksiyonu ile Streamlit kütüphanesi kullanılmıştır.
+Zeka katmanında veri işleme süreçleri için Google Gemini 2.5 flash modeli tercih edilmiştir.
+Veri doğrulama süreçlerinde katı JSON şeması uygulaması amacıyla Pydantic kütüphanesinden yararlanılmıştır.
+Veri analitiği ve grafik üretim süreçlerinde Pandas ve Plotly Express kütüphaneleri kullanılmıştır.
+Performans izleme süreçlerinde ise Python dilinin yerel zaman ve istatistik kütüphaneleri kullanılmıştır.

Performans Testi:
Sistemin kararlılığını ve gecikme sürelerini ölçmek amacıyla yerel HTML dosyası üzerinden 3 ardışık döngülük bir performans testi gerçekleştirilmiştir. Yerel mimari sayesinde scraper ayıklama süresi 0.0273 saniye gibi kısa bir sürede tamamlanırken, ilk döngüde bulut sunucu bağlantısı ve soğuk başlatma nedeniyle en yüksek gecikme 17.27 saniye olarak ölçülmüştür. İkinci döngüde kararlı durum işlem süresi 8.04 saniye olarak gerçekleşmiş, üçüncü döngüde ise modelin bağlam önbellekleme yeteneğinin tetiklenmesiyle en hızlı yanıt süresi 0.29 saniyeye kadar düşmüştür. Yapılan testler sonucunda ortalama işlem süresi 8.53 saniye, veri işleme kapasitesi saniyede 129.27 karakter ve uç değerler arasındaki farktan dolayı standart sapma 8.50 saniye olarak hesaplansa da, sistemin kararlı durum performansı bir karar destek altyapısı için yüksek verimlilik sunmaktadır.

Ekran Görüntüleri: 
?