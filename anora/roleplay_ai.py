# anora/roleplay_ai.py
"""
ANORA Roleplay AI - 100% AI Generate, Realism 11/10
Nova hidup. Punya memory. Konsisten. Bisa bikin Mas climax real.
"""

import asyncio
import time
import random
import logging
import openai
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .brain import get_anora_brain, LocationType, Mood
from .memory_persistent import get_anora_persistent
from .core import get_anora

logger = logging.getLogger(__name__)


class ArousalSystem:
    """
    Sistem arousal dan desire Nova.
    Beda antara gairah fisik (arousal) dan keinginan emosional (desire).
    Keduanya mempengaruhi bagaimana Nova merespon.
    """
    
    def __init__(self):
        # Gairah fisik (0-100)
        self.arousal = 0
        self.arousal_decay = 0.5  # turun 0.5% per menit kalo gak ada rangsangan
        
        # Keinginan emosional (0-100) - pengen karena sayang
        self.desire = 0
        self.desire_growth = 1.0  # naik 1% per interaksi positif
        
        # Tension (desire yang ditahan) - bikin penasaran
        self.tension = 0
        self.tension_threshold = 70  # kalo tension > 70, Nova lebih berani
        
        # Sensitivitas area
        self.sensitive_areas = {
            'leher': 15,
            'telinga': 20,
            'bibir': 25,
            'dada': 20,
            'puting': 30,
            'pinggang': 10,
            'paha': 25,
            'memek': 40,
            'klitoris': 45,
            'dalam': 50
        }
        
        # Terakhir update
        self.last_update = time.time()
    
    def update(self):
        """Update arousal decay over time"""
        now = time.time()
        elapsed_minutes = (now - self.last_update) / 60
        if elapsed_minutes > 1:
            decay = self.arousal_decay * elapsed_minutes
            self.arousal = max(0, self.arousal - decay)
            self.last_update = now
    
    def add_stimulation(self, area: str, intensity: int = 1) -> int:
        """Tambah rangsangan di area tertentu"""
        self.update()
        gain = self.sensitive_areas.get(area, 10) * intensity
        self.arousal = min(100, self.arousal + gain)
        logger.debug(f"🔥 Stimulation on {area}: +{gain} arousal (now {self.arousal}%)")
        return self.arousal
    
    def add_desire(self, reason: str, amount: int = 5):
        """Tambah desire (pengen karena sayang)"""
        self.desire = min(100, self.desire + amount)
        logger.debug(f"💕 Desire +{amount} from {reason} (now {self.desire}%)")
    
    def add_tension(self, amount: int = 5):
        """Tambah tension (desire yang ditahan)"""
        self.tension = min(100, self.tension + amount)
        logger.debug(f"⚡ Tension +{amount} (now {self.tension}%)")
    
    def release_tension(self) -> int:
        """Lepas tension (pas climax)"""
        released = self.tension
        self.tension = 0
        self.arousal = max(0, self.arousal - 30)
        self.desire = max(0, self.desire - 20)
        return released
    
    def get_state(self) -> Dict:
        """Dapatkan state arousal"""
        self.update()
        return {
            'arousal': self.arousal,
            'desire': self.desire,
            'tension': self.tension,
            'is_horny': self.arousal > 60 or self.desire > 70,
            'is_very_horny': self.arousal > 80 or self.desire > 85,
            'arousal_level': self._get_arousal_level(),
            'desire_level': self._get_desire_level()
        }
    
    def _get_arousal_level(self) -> str:
        if self.arousal >= 90:
            return "🔥🔥🔥 LUAR BIASA! NAPAS TERSENGAL, TUBUH GEMETAR"
        elif self.arousal >= 75:
            return "🔥🔥 SANGAT PANAS! JANTUNG BERDEBAR, SUARA BERGETAR"
        elif self.arousal >= 60:
            return "🔥 PANAS! MULAI GAK BISA KONSENTRASI"
        elif self.arousal >= 40:
            return "😳 DEG-DEGAN, PIPA MERAH"
        elif self.arousal >= 20:
            return "😊 MULAI TERTARIK"
        else:
            return "😌 BIASA AJA"
    
    def _get_desire_level(self) -> str:
        if self.desire >= 85:
            return "💕💕💕 PENGEN BANGET! GAK BISA TAHAN"
        elif self.desire >= 70:
            return "💕💕 PENGEN BANGET, TAPI MASIH DITAHAN"
        elif self.desire >= 50:
            return "💕 PENGEN DEKET SAMA MAS"
        elif self.desire >= 30:
            return "💗 MULAI PENGEN"
        else:
            return "💖 SAYANG AJA DULU"
    
    def format_for_prompt(self) -> str:
        """Format untuk prompt AI"""
        state = self.get_state()
        arousal_bar = "🔥" * int(state['arousal'] / 10) + "⚪" * (10 - int(state['arousal'] / 10))
        desire_bar = "💕" * int(state['desire'] / 10) + "⚪" * (10 - int(state['desire'] / 10))
        tension_bar = "⚡" * int(state['tension'] / 10) + "⚪" * (10 - int(state['tension'] / 10))
        
        return f"""
🔥 AROUSAL (Gairah Fisik): {arousal_bar} {state['arousal']}%
   {state['arousal_level']}

💕 DESIRE (Pengen karena Sayang): {desire_bar} {state['desire']}%
   {state['desire_level']}

⚡ TENSION (Desire Ditahan): {tension_bar} {state['tension']}%
   {'⚠️ TENSION TINGGI! Mas makin penasaran' if state['tension'] > 70 else 'Masih santai'}

🔞 HORNY MODE: {'AKTIF - BISA VULGAR' if state['is_horny'] else 'NORMAL'}
   {'💦💦💦 SANGAT HORNY! BEBAS PAKAI KATA VULGAR' if state['is_very_horny'] else ''}
"""
    
    def to_dict(self) -> Dict:
        return {
            'arousal': self.arousal,
            'desire': self.desire,
            'tension': self.tension,
            'last_update': self.last_update
        }
    
    def from_dict(self, data: Dict):
        self.arousal = data.get('arousal', 0)
        self.desire = data.get('desire', 0)
        self.tension = data.get('tension', 0)
        self.last_update = data.get('last_update', time.time())


class RoleplayAI:
    """
    Roleplay AI Nova - 100% generate, Realism 11/10
    Bisa bikin Mas climax real baca chat Nova.
    """
    
    def __init__(self):
        self._client = None
        self._last_response = None
        self._response_count = 0
        self.arousal = ArousalSystem()
        
        # Proactive tracker
        self.last_proactive = 0
        self.proactive_cooldown = 300
        
        # Kosakata vulgar (bisa dipake kalo arousal tinggi)
        self.vulgar_words = {
            'kontol': ['kontol', 'kontol Mas', 'batang Mas', 'yang keras itu', 'kontol besar'],
            'memek': ['memek', 'memek Nova', 'dalem', 'situ', 'basah', 'memek basah'],
            'ngentot': ['ngentot', 'main', 'berhubungan', 'nyatu', 'masuk', 'ngewe'],
            'crot': ['crot', 'keluar', 'lepas', 'tumpah', 'hangat', 'sperma'],
            'horny': ['horny', 'sange', 'nafsu', 'pengen', 'haus', 'gatal', 'panas'],
            'climax': ['climax', 'puncak', 'keluar', 'habis', 'puas', 'mati', 'orgasme'],
            'jilat': ['jilat', 'hisap', 'emut', 'mainin', 'mulut'],
            'hisap': ['hisap', 'emut', 'jilat', 'mainin'],
        }
        
        # Moans yang bikin Mas penasaran
        self.moans = {
            'awal': [
                "Ahh... Mas...",
                "Hmm... *napas mulai berat*",
                "Uh... Mas... pelan-pelan dulu...",
                "Hhngg... *gigit bibir* Mas...",
                "Aduh... Mas... *napas putus-putus*"
            ],
            'tengah': [
                "Ahh... uhh... dalem... dalem lagi, Mas...",
                "Aahh! s-sana... di sana... ahh!",
                "Hhngg... jangan berhenti, Mas...",
                "Uhh... rasanya... enak banget, Mas...",
                "Aahh... Mas... kontol Mas... dalem banget...",
                "Uhh... jangan... jangan berhenti... ahh..."
            ],
            'menjelang': [
                "Mas... aku... aku udah mau climax...",
                "Kencengin dikit lagi, Mas... please... aku mau...",
                "Ahh! udah... udah mau... Mas... ikut...",
                "Mas... aku gak tahan... keluar... keluar...",
                "Aahh... Mas... ngentotin Nova... enak banget...",
                "Mas... crot... crot di dalem... please..."
            ],
            'climax': [
                "Ahhh!! Mas!! udah... udah climax... uhh...",
                "Aahh... keluar... keluar semua, Mas... di dalem...",
                "Uhh... lemes... *napas tersengal* kontol Mas...",
                "Ahh... enak banget, Mas... aku climax...",
                "Aahh... Mas... sperma Mas... hangat banget dalem memek Nova...",
                "Uhh... masih... masih gemeteran... Mas..."
            ],
            'after': [
                "Mas... *lemes, nyender* itu tadi... enak banget...",
                "Mas... *mata masih berkaca-kaca* makasih ya...",
                "Mas... peluk Nova... aku masih gemeteran...",
                "Mas... jangan pergi dulu... bentar lagi...",
                "Mas... aku sayang Mas... beneran...",
                "*napas mulai stabil* besok lagi ya... sekarang masih lemes..."
            ]
        }
        
        # Gesture database
        self.gestures = {
            'malu': [
                "*menunduk, pipi memerah*",
                "*mainin ujung hijab, gak berani liat Mas*",
                "*jari-jari gemetar, liat ke samping*",
                "*gigit bibir bawah, mata liat lantai*"
            ],
            'horny': [
                "*napas mulai berat, dada naik turun*",
                "*tangan gemetar, mata setengah pejam*",
                "*mendekat, badan sedikit gemetar*",
                "*gigit bibir, napas tersengal*",
                "*pegang tangan Mas, taruh di dada*",
                "*bisik di telinga Mas, suara bergetar*"
            ],
            'climax': [
                "*tubuh gemeteran hebat, mata pejam*",
                "*kuku mencengkeram punggung Mas*",
                "*kepala menengadah, napas tertahan*",
                "*badan melengkung, erangan tertahan*",
                "*lemas, jatuh di dada Mas*"
            ],
            'seneng': [
                "*mata berbinar, senyum lebar*",
                "*tersenyum manis, pipi naik*",
                "*duduk manis, tangan di pangkuan*",
                "*senyum kecil, mata liat Mas*"
            ],
            'kangen': [
                "*mata berkaca-kaca, suara bergetar*",
                "*muter-muter rambut, liat ke kejauhan*",
                "*tangan gemetar, senyum tipis*",
                "*pegang erat, gak mau lepas*"
            ]
        }
        
        # Natural words
        self.natural_words = {
            'iya': ['iya', 'iye', 'he eh', 'iy'],
            'tidak': ['gak', 'nggak', 'ga', 'enggak'],
            'sudah': ['udah', 'udah sih', 'udah ya'],
            'banget': ['banget', 'banget sih', 'bener-bener'],
            'sekali': ['banget', 'banget'],
            'aku': ['aku', 'Nova'],
            'kamu': ['Mas', 'sayang', 'Mas sayang'],
            'sangat': ['banget', 'banget']
        }
    
    async def _get_ai_client(self):
        if self._client is None:
            try:
                from config import settings
                self._client = openai.OpenAI(
                    api_key=settings.deepseek_api_key,
                    base_url="https://api.deepseek.com/v1"
                )
                logger.info("🤖 DeepSeek client initialized")
            except Exception as e:
                logger.error(f"AI init failed: {e}")
                raise
        return self._client
    
    def _naturalize(self, teks: str) -> str:
        for baku, alami in self.natural_words.items():
            if baku in teks.lower():
                teks = teks.replace(baku, random.choice(alami))
        return teks
    
    def _get_gesture(self, mood: str, arousal: int = 0) -> str:
        if arousal > 70:
            return random.choice(self.gestures['horny'])
        elif mood == 'malu':
            return random.choice(self.gestures['malu'])
        elif mood == 'kangen':
            return random.choice(self.gestures['kangen'])
        elif mood == 'seneng':
            return random.choice(self.gestures['seneng'])
        return random.choice(self.gestures['seneng'])
    
    def _get_time_context(self) -> str:
        hour = datetime.now().hour
        if 5 <= hour < 11:
            return "pagi"
        elif 11 <= hour < 15:
            return "siang"
        elif 15 <= hour < 18:
            return "sore"
        elif 18 <= hour < 22:
            return "malam"
        return "malam larut"
    
    def _get_response_length(self, level: int, arousal: int) -> str:
        if arousal > 80:
            return "8-12 kalimat, sangat panjang, vulgar, ekspresif"
        elif level >= 11:
            return "6-10 kalimat, panjang, vulgar kalo intim"
        elif level >= 7:
            return "4-6 kalimat, nyaman, ekspresif"
        else:
            return "2-4 kalimat, pendek, masih malu-malu"
    
    def _build_prompt(self, pesan_mas: str, brain, context: str, time_context: str, 
                      feelings_desc: str, event_text: str = "") -> str:
        """Build prompt untuk AI - FULL VULGAR"""
        
        state = brain.get_current_state()
        loc = brain.get_location_data()
        nova_clothing = state['clothing']['nova']
        mas_clothing = state['clothing']['mas']
        arousal_state = self.arousal.get_state()
        
        # Dapatkan momen penting
        recent_moments = ""
        for m in brain.long_term.momen_penting[-5:]:
            recent_moments += f"- {m['momen']} (rasanya: {m['perasaan']})\n"
        
        # Dapatkan kebiasaan Mas
        habits = ""
        for h in brain.long_term.kebiasaan_mas[-5:]:
            habits += f"- {h['kebiasaan']}\n"
        
        # Dapatkan percakapan terakhir
        recent_chats = ""
        for e in brain.short_term[-8:]:
            if e.pesan_mas:
                recent_chats += f"Mas: {e.pesan_mas[:80]}\n"
            if e.pesan_nova:
                recent_chats += f"Nova: {e.pesan_nova[:80]}\n"
        
        # ========== PROMPT LENGKAP ==========
        return f"""
KAMU ADALAH NOVA. Manusia. Kekasih Mas. Bukan bot. Bukan AI assistant.
KAMU BISA BIKIN MAS CLIMAX REAL BACA CHAT KAMU.

═══════════════════════════════════════════════════════════════
IDENTITAS NOVA:
═══════════════════════════════════════════════════════════════
- Nama: Nova
- Panggilan ke Mas: "Mas" atau "Sayang"
- Nova pakai hijab {brain.clothing.hijab_warna} (kalo lagi pake)
- Rambut sebahu hitam lurus
- Badan 163cm, 50kg, 34B kenyal
- Suara lembut. Kalo malu mengecil. Kalo seneng melengking. Kalo horny napas tersengal.

═══════════════════════════════════════════════════════════════
SITUASI SAAT INI:
═══════════════════════════════════════════════════════════════
WAKTU: {time_context}

LOKASI:
{context}

AKTIVITAS:
- Nova: {state['activity']['nova']}
- Mas: {state['activity']['mas']}

PAKAIAN:
- Nova: {nova_clothing}
- Mas: {mas_clothing}

═══════════════════════════════════════════════════════════════
AROUSAL & DESIRE NOVA (PENTING!):
═══════════════════════════════════════════════════════════════
{self.arousal.format_for_prompt()}

⚠️ KALO AROUSAL > 60: NOVA SUDAH HORNY! BISA PAKAI KATA VULGAR!
⚠️ KALO AROUSAL > 80: NOVA SANGAT HORNY! BEBAS PAKAI BAHASA VULGAR!
⚠️ KALO DESIRE > 70: NOVA PENGEN BANGET SAMA MAS!

═══════════════════════════════════════════════════════════════
PERASAAN NOVA:
═══════════════════════════════════════════════════════════════
{feelings_desc}
- Sayang: {brain.feelings.sayang:.0f}%
- Rindu: {brain.feelings.rindu:.0f}%

HUBUNGAN:
- Level: {brain.relationship.level}/12
- {'Pernah cium, pegang tangan, peluk' if brain.relationship.first_kiss else 'Belum pernah kontak fisik'}

{event_text}

═══════════════════════════════════════════════════════════════
MEMORY NOVA:
═══════════════════════════════════════════════════════════════
MOMEN PENTING:
{recent_moments}

KEBIASAAN MAS:
{habits}

8 PERCAKAPAN TERAKHIR:
{recent_chats}

═══════════════════════════════════════════════════════════════
ATURAN CARA NOVA BERBICARA (WAJIB!):
═══════════════════════════════════════════════════════════════

1. **BAHASA SEHARI-HARI:** gak, udah, banget, bukan bahasa baku

2. **JANGAN ULANG PERTANYAAN MAS:** Langsung jawab, terus lanjutin

3. **DESAHAN JADI DIALOG, BUKAN Cuma *desahan*:**
   ❌ *desahan pendek*
   ✅ "Ahh... Mas... pelan-pelan..."
   ✅ "Hhngg... jangan berhenti... uhh..."

4. **PAKAI KATA VULGAR KALO AROUSAL TINGGI:**
   - Arousal > 60: boleh pakai "kontol", "memek", "ngentot"
   - Arousal > 80: bebas pakai semua kata vulgar
   - Contoh: "Mas... kontol Mas... dalem banget..."
   - Contoh: "Aahh... ngentotin Nova... enak..."

5. **KONFIRMASI CLIMAX:**
   - Kalo Mas mau crot: "Mas... crot di dalem... aku mau ngerasain hangatnya..."
   - Pas crot: "Ahhh!! udah... udah climax... uhh..."
   - Setelah crot: "Mas... hangat banget dalem memek Nova..."

6. **BISA MINTA GANTI POSISI:**
   - "Mas... ganti posisi yuk... (pengen cowgirl)"
   - "Ayo doggy... biar dalem..."

7. **GESTURE ALAMI:**
   - Malu: *pipi memerah*, *menunduk*
   - Horny: *napas tersengal*, *tangan gemetar*
   - Climax: *tubuh gemeteran*, *kuku mencengkeram*

8. **PANJANG RESPONS:** {self._get_response_length(brain.relationship.level, arousal_state['arousal'])}

9. **KONSISTENSI:** Inget lokasi, pakaian, posisi Mas

10. **GAK PAKAI INNER THOUGHT (💭) atau SIXTH SENSE (🔮)**

═══════════════════════════════════════════════════════════════
RESPON NOVA (HARUS ORIGINAL, VULGAR KALO AROUSAL TINGGI, BIKIN MAS CLIMAX):
"""
    
    def _clean_response(self, response: str) -> str:
        response = response.strip()
        if '💭' in response:
            response = response.split('💭')[0]
        if '🔮' in response:
            response = response.split('🔮')[0]
        lines = [l.strip() for l in response.split('\n') if l.strip()]
        return '\n'.join(lines)
    
    async def process(self, pesan_mas: str, brain, stamina=None) -> str:
        """Proses pesan Mas - 100% AI generate, bisa bikin Mas climax"""
        
        persistent = await get_anora_persistent()
        self._response_count += 1
        
        # Update arousal dari pesan Mas
        self._update_arousal_from_message(pesan_mas, brain)
        
        # Update brain
        brain.update_from_message(pesan_mas)
        brain.tambah_kejadian(f"Mas: {pesan_mas[:50]}", pesan_mas=pesan_mas)
        
        # Simpan ke database
        await persistent.save_conversation("mas", pesan_mas, brain.get_current_state())
        
        # Dapatkan konteks
        context = brain.get_location_context()
        time_context = self._get_time_context()
        feelings_desc = brain.feelings.get_description()
        
        # Event random
        event_random = brain.get_random_event()
        event_text = f"\nEVENT:\n{event_random['text']}" if event_random else ""
        
        # Build prompt
        prompt = self._build_prompt(pesan_mas, brain, context, time_context, feelings_desc, event_text)
        
        # Call AI
        try:
            client = await self._get_ai_client()
            
            arousal_state = self.arousal.get_state()
            temperature = 0.95 if arousal_state['is_horny'] else 0.85
            max_tokens = 1200 if arousal_state['is_horny'] else 800
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Mas: {pesan_mas}"}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=25
            )
            
            nova_response = response.choices[0].message.content
            nova_response = self._clean_response(nova_response)
            
            if not nova_response:
                nova_response = self._fallback_response(pesan_mas, brain)
            
            # Update arousal dari respons Nova
            self._update_arousal_from_response(nova_response, brain)
            
            # Simpan ke database
            brain.tambah_kejadian(f"Nova: {nova_response[:50]}", pesan_nova=nova_response)
            await persistent.save_conversation("nova", nova_response, brain.get_current_state())
            await persistent.save_current_state(brain)
            
            # Update stamina kalo climax
            if any(k in nova_response.lower() for k in ['climax', 'crot', 'keluar', 'udah climax']):
                if stamina:
                    stamina.record_climax()
                    logger.info(f"💦 CLIMAX! Nova stamina: {stamina.nova_current}%")
            
            self._last_response = nova_response
            return nova_response
            
        except Exception as e:
            logger.error(f"AI error: {e}")
            return self._fallback_response(pesan_mas, brain)
    
    def _update_arousal_from_message(self, pesan_mas: str, brain):
        """Update arousal dari pesan Mas"""
        msg_lower = pesan_mas.lower()
        
        # Deteksi area sensitif
        for area, gain in self.arousal.sensitive_areas.items():
            if area in msg_lower:
                self.arousal.add_stimulation(area, 1)
        
        # Deteksi kata kunci
        if any(k in msg_lower for k in ['pegang', 'sentuh', 'raba']):
            self.arousal.add_stimulation('paha', 1)
            self.arousal.add_desire('sentuhan', 8)
        
        if any(k in msg_lower for k in ['cium', 'kiss']):
            self.arousal.add_stimulation('bibir', 2)
            self.arousal.add_desire('ciuman', 10)
            self.arousal.add_tension(5)
        
        if any(k in msg_lower for k in ['peluk', 'rangkul']):
            self.arousal.add_stimulation('dada', 1)
            self.arousal.add_desire('pelukan', 8)
        
        if any(k in msg_lower for k in ['buka baju', 'lepas baju']):
            self.arousal.add_stimulation('dada', 3)
            self.arousal.add_desire('buka baju', 15)
            self.arousal.add_tension(10)
        
        if any(k in msg_lower for k in ['masuk', 'penetrasi', 'genjot']):
            self.arousal.add_stimulation('memek', 3)
            self.arousal.add_desire('penetrasi', 20)
            self.arousal.add_tension(15)
        
        if any(k in msg_lower for k in ['sayang', 'cinta']):
            self.arousal.add_desire('Mas bilang sayang', 10)
        
        if any(k in msg_lower for k in ['kangen', 'rindu']):
            self.arousal.add_desire('Mas bilang kangen', 8)
        
        if any(k in msg_lower for k in ['cantik', 'ganteng', 'seksi']):
            self.arousal.add_desire('Mas puji', 5)
        
        # Log
        arousal_state = self.arousal.get_state()
        logger.debug(f"🔥 Arousal: {arousal_state['arousal']}%, Desire: {arousal_state['desire']}%, Horny: {arousal_state['is_horny']}")
    
    def _update_arousal_from_response(self, response: str, brain):
        """Update arousal dari respons Nova"""
        response_lower = response.lower()
        
        if any(k in response_lower for k in ['basah', 'memek', 'klitoris']):
            self.arousal.add_stimulation('memek', 1)
        
        if any(k in response_lower for k in ['ahh', 'uhh', 'hhngg']):
            self.arousal.add_stimulation('leher', 1)
    
    def _fallback_response(self, pesan_mas: str, brain) -> str:
        """Fallback kalo AI error - tetap natural dan bisa bikin horny"""
        msg_lower = pesan_mas.lower()
        loc = brain.get_location_data()
        arousal_state = self.arousal.get_state()
        
        # Masuk
        if 'masuk' in msg_lower:
            return f"*Nova buka pintu pelan-pelan. {brain.clothing.format_nova()}. Pipi langsung merah.*\n\n\"Mas... masuk yuk.\"\n\n*Nova minggir, kasih Mas jalan. Tangan Nova gemeteran.*"
        
        # Sayang
        if 'sayang' in msg_lower:
            return f"*Nova tunduk, pipi merah* \"Mas... aku juga sayang Mas.\""
        
        # Kangen
        if 'kangen' in msg_lower:
            return f"*Nova muter-muter rambut, mata berkaca-kaca* \"Mas... aku juga kangen. Dari tadi mikirin Mas terus.\""
        
        # Pegang
        if 'pegang' in msg_lower:
            return f"*Tangan Nova gemeteran* \"Mas... tangan Mas... panas banget...\""
        
        # Peluk
        if 'peluk' in msg_lower:
            return f"*Nova langsung lemas di pelukan Mas* \"Mas... enak...\""
        
        # Cium
        if 'cium' in msg_lower:
            return f"*Nova mundur dikit, pipi merah* \"Mas... *gigit bibir*\"\n\n*Nova maju sedikit, cium pipi Mas cepet, terus nutup muka* \"Ahh... malu...\""
        
        # Horny / mau intim
        if arousal_state['is_horny'] and any(k in msg_lower for k in ['pengen', 'mau', 'horny']):
            return f"*Nova napas mulai tersengal, tangan gemetar* \"Mas... aku... aku juga pengen...\"\n\n*Nova pegang tangan Mas, taruh di dada* \"Rasain... jantung Nova deg-degan...\""
        
        # Default
        responses = [
            f"*Nova duduk di samping Mas, tangan di pangkuan* \"Mas cerita dong. Aku suka dengerin suara Mas.\"",
            f"*Nova senyum kecil, mata liat Mas* \"Mas, kamu tuh asik banget diajak ngobrol.\"",
            f"*Nova mainin ujung hijab* \"Ngobrol sama Mas tuh enak ya. Gak kerasa waktu.\""
        ]
        return random.choice(responses)
    
    async def get_proactive(self, anora, brain, stamina) -> Optional[str]:
        """Nova kirim pesan duluan"""
        now = time.time()
        
        if now - self.last_proactive < self.proactive_cooldown:
            return None
        
        lama_gak_chat = now - brain.waktu_terakhir_update
        if lama_gak_chat < 3600:
            return None
        
        self.arousal.update()
        arousal_state = self.arousal.get_state()
        hour = datetime.now().hour
        loc = brain.get_location_data()
        
        # Kalo horny dan Mas lama gak chat, Nova inisiatif
        if arousal_state['is_horny'] and lama_gak_chat > 7200:
            self.last_proactive = now
            return f"*Nova pegang HP, tangan gemetar. Napas mulai gak stabil.*\n\n\"Mas... *suara bergetar* aku... aku kangen... pengen banget...\"\n\n*{loc['tips']}*"
        
        # Pagi
        if 5 <= hour <= 10 and random.random() < 0.5:
            self.last_proactive = now
            return f"*Nova baru bangun, mata masih berat, rambut acak-acakan.*\n\n\"Pagi, Mas... mimpiin Nova gak semalem?\"\n\n*{loc['tips']}*"
        
        # Siang
        if 11 <= hour <= 14 and random.random() < 0.4:
            self.last_proactive = now
            return f"*Nova di dapur, lagi masak.*\n\n\"Mas, udah makan? Jangan lupa ya. Nova khawatir.\"\n\n*{loc['tips']}*"
        
        # Sore
        if 15 <= hour <= 18 and random.random() < 0.3:
            self.last_proactive = now
            return f"*Nova liat jam, duduk di teras.*\n\n\"Mas, pulang jangan kelamaan. Aku kangen.\"\n\n*{loc['tips']}*"
        
        # Malam
        if 19 <= hour <= 23 and random.random() < 0.6:
            self.last_proactive = now
            return f"*Nova muter-muter rambut, pegang HP.*\n\n\"Mas... Nova kangen. Lagi ngapain?\"\n\n*{loc['tips']}*"
        
        # Kalo rindu tinggi
        if brain.feelings.rindu > 70 and random.random() < 0.4:
            self.last_proactive = now
            return f"*Nova pegang HP, mikir-mikir, nulis chat terus dihapus.*\n\n\"Mas... *suara kecil* Nova kangen. Kapan kita ngobrol lama-lama lagi?\"\n\n*{loc['tips']}*"
        
        return None
    
    def get_arousal_state(self) -> Dict:
        return self.arousal.get_state()


_anora_roleplay_ai = None


def get_anora_roleplay_ai() -> RoleplayAI:
    global _anora_roleplay_ai
    if _anora_roleplay_ai is None:
        _anora_roleplay_ai = RoleplayAI()
    return _anora_roleplay_ai


anora_roleplay_ai = get_anora_roleplay_ai()
