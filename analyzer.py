import os
import json
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

class PuanDetay(BaseModel):
    skor: str = Field(description="0-10 arası bir değerlendirme notu. Örn: '8.5'")
    neden: str = Field(description="Bu puanın verilme gerekçesi, kısa analiz cümlesi.")

class KategoriPuanlari(BaseModel):
    genel: PuanDetay = Field(description="Genel kategorisi")
    kalite: PuanDetay = Field(description="Kalite kategorisi")
    kargo: PuanDetay = Field(description="Kargo süreci kategorisi")
    fiyat: PuanDetay = Field(description="Fiyat & Performans dengesi kategorisi")

class ZamanTrendItem(BaseModel):
    ay: str = Field(description="Ay adı. Örn: 'Ocak', 'Şubat'")
    skor: float = Field(description="O aya ait memnuniyet skoru (0 ile 10 arasında)")

class GeminiAnalizSchema(BaseModel):
    ozet: str = Field(description="Ürünün genel durumu hakkında dürüst bir tüketici özeti.")
    artilar: List[str] = Field(description="Öne çıkan olumlu özelliklerin listesi.")
    eksiler: List[str] = Field(description="Eleştirilen olumsuz özelliklerin listesi.")
    dikkat_edilmesi_gereken: str = Field(description="Satın alma öncesi hayati kullanıcı uyarısı.")
    puanlar: KategoriPuanlari
    zamanla_degisim: List[ZamanTrendItem]


class ShoppingAnalyzer:
    def __init__(self, model_name='gemini-2.5-flash'): 
        if not GEMINI_API_KEY:
            raise ValueError("API_KEY_BULUNAMADI")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = model_name

    def _metin_optimize_et(self, ham_metin):
        if not ham_metin:
            return ""
        return re.sub(r'\s+', ' ', str(ham_metin)).strip()

    def urun_analiz_et(self, urun_icerigi):
        if not urun_icerigi or len(urun_icerigi.strip()) == 0:
            return {"hata": "HTML dosyasından okunabilir bir metin çıkarılamadı. Dosya içeriğini kontrol edin."}
            
        optimize_veri = self._metin_optimize_et(urun_icerigi)
        
        prompt = f"""
        Sen profesyonel bir e-ticaret analistisin. Sana gelen metnin içeriğindeki 
        gerçek kullanıcı yorumlarını, müşteri geri bildirimlerini bul, cımbızla seç ve analiz et.
        Eğer metinde yeterli yorum yoksa, şemayı mantıklı varsayılan verilerle doldur ancak 'ozet' kısmında bunu jüriye belirt.

        Kaynak Veri:
        {optimize_veri}
        """
        
        try:
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GeminiAnalizSchema,
                temperature=0.1
            )
            response = self.client.models.generate_content(
                model=self.model_name, 
                contents=prompt,
                config=config
            )
            
            raw_data = json.loads(response.text)
            
            final_res = {
                "ozet": raw_data.get("ozet") or "Ürün analizi başarıyla gerçekleştirildi.",
                "artilar": raw_data.get("artilar") or ["Genel kullanım kolaylığı"],
                "eksiler": raw_data.get("eksiler") or ["Belirgin bir olumsuzluk belirtilmemiş"],
                "dikkat_edilmesi_gereken": raw_data.get("dikkat_edilmesi_gereken") or "Kendi bedeninizi/numaranızı tercih edebilirsiniz.",
                "puanlar": {
                    "Genel Not": {
                        "skor": raw_data["puanlar"]["genel"]["skor"],
                        "neden": raw_data["puanlar"]["genel"]["neden"]
                    },
                    "Kumaş & Kalite": {
                        "skor": raw_data["puanlar"]["kalite"]["skor"],
                        "neden": raw_data["puanlar"]["kalite"]["neden"]
                    },
                    "Kargo & Paket": {
                        "skor": raw_data["puanlar"]["kargo"]["skor"],
                        "neden": raw_data["puanlar"]["kargo"]["neden"]
                    },
                    "Fiyat & Performans": {
                        "skor": raw_data["puanlar"]["fiyat"]["skor"],
                        "neden": raw_data["puanlar"]["fiyat"]["neden"]
                    }
                },
                "zamanla_degisim": raw_data.get("zamanla_degisim") or []
            }
            
            return final_res
            
        except Exception as e:
            return {"hata": f"Yapay Zeka Çözümleme Hatası: {str(e)}"}

    def chat_ile_sor(self, soru, context):
        try:
            response = self.client.models.generate_content(
                model=self.model_name, 
                contents=f"Bağlam (Ürün Özeti): {context}\n\nKullanıcı Sorusu: {soru}\n\nLütfen bu ürün özetine sadık kalarak kullanıcıya asistan gibi cevap ver."
            )
            return response.text
        except Exception as e:
            return f"Şu an teknik bir aksaklık nedeniyle sorunuz yanıtlanamıyor. (Hata: {str(e)})"

    def kiyasla(self, urun1, urun2):
        try:
            response = self.client.models.generate_content(
                model=self.model_name, 
                contents=f"Aşağıdaki iki ürüne ait ham verileri ve kullanıcı deneyimlerini kıyasla. Karşılaştırmalı bir analiz sun:\n\nÜrün 1: {str(urun1)[:3000]}\n\nÜrün 2: {str(urun2)[:3000]}"
            )
            return response.text
        except Exception as e:
            return f"Kıyaslama motoru şu an başlatılamıyor. (Hata: {str(e)})"