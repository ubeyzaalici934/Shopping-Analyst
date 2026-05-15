import os
from dotenv import load_dotenv
from google import genai 

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("HATA: .env dosyasında GEMINI_API_KEY bulunamadı! Lütfen kontrol edin.")

class ShoppingAnalyzer:
    def chat_ile_sor(self, soru, context):
        """
        Kullanıcının ürünle ilgili özel sorularını, analiz raporunu 
        baz alarak yanıtlar.
        """
        chat_prompt = f"""
        Aşağıdaki ürün analiz raporuna dayanarak kullanıcının sorusunu yanıtla. 
        Eğer raporun içinde cevap yoksa, genel bilginle değil, 'Bu konuda yeterli yorum bulamadım' şeklinde dürüstçe yanıt ver.

        [ANALİZ RAPORU]:
        {context}

        [KULLANICI SORUSU]: 
        {soru}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=chat_prompt
            )
            return response.text
        except Exception as e:
            return f"Sohbet sırasında bir hata oluştu: {str(e)}"
    
    def __init__(self, model_name='gemini-2.5-flash'): # Daha güncel bir model
        self.client = genai.Client(api_key=API_KEY)
        self.model_name = model_name

    def urun_analiz_et(self, yorumlar, profil):
        """
        Ham veriyi işleyip mühendislik odaklı bir rapor sunar.
        """
        prompt = f"""
        Sen profesyonel bir Alışveriş Analisti ve Karar Destek Uzmanısın. 
        Aşağıdaki verileri kullanarak tarafsız ve rasyonel bir rapor oluştur.

        [KULLANICI PROFİLİ]: {profil}
        [ÜRÜN YORUMLARI]: {yorumlar}

        RAPOR FORMATI:
        1. Özet Analiz: Ürün vaadini karşılıyor mu?
        2. SWOT Analizi: Güçlü/Zayıf Yanlar, Fırsatlar, Tehditler.
        3. Kullanıcı Uyumu: Bu profil için ne kadar uygun?
        4. Skorlama (0-10): Fiyat/Performans, Malzeme, Hız.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Analiz sırasında bir hata oluştu: {str(e)}"
        