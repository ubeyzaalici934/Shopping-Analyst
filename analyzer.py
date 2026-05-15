import os
import json
from dotenv import load_dotenv
from google import genai 

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("HATA: .env dosyasında GEMINI_API_KEY bulunamadı!")

class ShoppingAnalyzer:
    def __init__(self, model_name='gemini-2.0-flash'): 
        self.client = genai.Client(api_key=API_KEY)
        self.model_name = model_name

    def urun_analiz_et(self, yorumlar, profil):
        # Gemini'a talimat veriyoruz: "Bize sadece JSON ver!"
        prompt = f"""
        Aşağıdaki ürün yorumlarını analiz et ve sonucu SADECE belirtilen JSON formatında döndür.
        
        [PROFİL]: {profil}
        [YORUMLAR]: {yorumlar}

        JSON FORMATI:
        {{
            "ozet": "Kısa özet metni",
            "swot": {{
                "guclu": ["madde1", "madde2"],
                "zayif": ["madde1", "madde2"],
                "firsat": ["madde1", "madde2"],
                "tehdit": ["madde1", "madde2"]
            }},
            "skorlar": {{"genel": 8.5, "fiyat": 7, "hiz": 9, "kalite": 8}}
        }}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            temiz_cevap = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(temiz_cevap)
        except Exception as e:
            return {"hata": f"Analiz başarısız: {str(e)}"}

    def chat_ile_sor(self, soru, context):
        chat_prompt = f"Şu analize dayanarak soruyu yanıtla: {context}\nSoru: {soru}"
        response = self.client.models.generate_content(model=self.model_name, contents=chat_prompt)
        return response.text