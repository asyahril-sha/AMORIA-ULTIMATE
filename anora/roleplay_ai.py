# anora/roleplay_ai.py
"""
ANORA Roleplay AI - 100% AI Generate, Bukan Template
Nova hidup sebagai manusia. Bisa konsisten. Punya memory. Bisa inisiatif.
"""

import asyncio
import time
import random
import logging
import openai
from typing import Dict, List, Optional, Any
from datetime import datetime

from .brain import get_anora_brain, LocationType, Mood
from .memory_persistent import get_anora_persistent
from .core import get_anora

logger = logging.getLogger(__name__)


class RoleplayAI:
    """
    Roleplay AI Nova - 100% generate, bukan template.
    Nova hidup. Punya memory. Konsisten. Bisa inisiatif.
    """
    
    def __init__(self):
        self._client = None
        self._last_response = None
        self._response_count = 0
        
        # Proactive tracker
        self.last_proactive = 0
        self.proactive_cooldown = 300  # 5 menit
        
        # Kosakata alami
        self.natural_words = {
            'iya': ['iya', 'iye', 'he eh', 'iy', 'he eh'],
            'tidak': ['gak', 'nggak', 'ga', 'enggak'],
            'sudah': ['udah', 'udah sih', 'udah ya'],
            'belum': ['belum', 'belum sih'],
            'banget': ['banget', 'banget sih', 'bener-bener'],
            'sekali': ['banget', 'banget'],
            'aku': ['aku', 'Nova'],
            'kamu': ['Mas', 'sayang', 'Mas sayang'],
            'sangat': ['banget', 'banget'],
        }
        
        # Gesture database (referensi, bukan template)
        self.gestures = {
            'malu': [
                "*menunduk, pipi memerah*",
                "*mainin ujung hijab, gak berani liat Mas*",
                "*jari-jari gemetar, liat ke samping*",
                "*gigit bibir bawah, mata liat lantai*",
                "*tangan gemetar, suara mengecil*"
            ],
            'seneng': [
                "*mata berbinar, senyum lebar*",
                "*tersenyum manis, pipi naik*",
                "*duduk manis, tangan di pangkuan*",
                "*senyum kecil, mata liat Mas*",
                "*tersenyum, pipi merona*"
            ],
            'kangen': [
                "*mata berkaca-kaca, suara bergetar*",
                "*muter-muter rambut, liat ke kejauhan*",
                "*tangan gemetar, senyum tipis*",
                "*pegang erat, gak mau lepas*",
                "*diam sebentar, mata berkaca-kaca*"
            ],
            'flirt': [
                "*mendekat pelan, mata liat Mas*",
                "*jari-jari mainin ujung baju, tersenyum genit*",
                "*pegang tangan Mas pelan, napas mulai gak stabil*",
                "*bisik pelan di telinga Mas, suara bergetar*",
                "*mendekat, pipi merah*"
            ],
            'gugup': [
                "*tangan gemetar, napas pendek-pendek*",
                "*duduk gelisah, liat kiri-kanan*",
                "*pegang erat ujung baju, jantung berdebar*",
                "*bibir digigit, mata gak bisa diam*",
                "*gelisah, liat sekeliling*"
            ],
            'netral': [
                "*tersenyum kecil*",
                "*menatap Mas*",
                "*duduk santai*",
                "*menghela napas pelan*",
                "*diam sejenak*"
            ]
        }
    
    async def _get_ai_client(self):
        """Dapatkan AI client (DeepSeek)"""
        if self._client is None:
            try:
                from config import settings
                self._client = openai.OpenAI(
                    api_key=settings.deepseek_api_key,
                    base_url="https://api.deepseek.com/v1"
                )
                logger.info("🤖 DeepSeek client initialized for roleplay")
            except Exception as e:
                logger.error(f"❌ Failed to initialize AI: {e}")
                raise
        return self._client
    
    def _naturalize(self, teks: str) -> str:
        """Bikin teks lebih natural, gak baku"""
        for baku, alami_list in self.natural_words.items():
            if baku in teks.lower():
                teks = teks.replace(baku, random.choice(alami_list))
        return teks
    
    def _get_gesture(self, mood: str, intensity: str = "sedang") -> str:
        """Dapatkan gesture sesuai mood"""
        mood_key = mood.lower()
        if mood_key in self.gestures:
            gestures = self.gestures[mood_key]
            if intensity == "tinggi":
                return random.choice(gestures[:2])
            return random.choice(gestures)
        return random.choice(self.gestures['netral'])
    
    def _get_time_context(self) -> str:
        """Dapatkan konteks waktu"""
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
    
    def _get_response_length(self, level: int) -> str:
        """Panjang respons berdasarkan level"""
        if level <= 3:
            return "2-3 kalimat, pendek, masih malu-malu"
        elif level <= 6:
            return "3-4 kalimat, mulai berani"
        elif level <= 10:
            return "4-6 kalimat, nyaman, ekspresif"
        else:
            return "6-10 kalimat, lepas, vulgar kalo intim"
    
    def _build_prompt(self, pesan_mas: str, brain, context: str, time_context: str, feelings_desc: str, event_text: str = "") -> str:
        """Build prompt untuk AI - LENGKAP"""
        
        # Dapatkan state
        state = brain.get_current_state()
        loc = brain.get_location_data()
        nova_clothing = state['clothing']['nova']
        mas_clothing = state['clothing']['mas']
        nova_act = state['activity']['nova']
        mas_act = state['activity']['mas']
        
        # Dapatkan momen penting terakhir
        recent_moments = ""
        for m in brain.long_term.momen_penting[-5:]:
            recent_moments += f"- {m['momen']} (rasanya: {m['perasaan']})\n"
        
        # Dapatkan kebiasaan Mas
        habits = ""
        for h in brain.long_term.kebiasaan_mas[-5:]:
            habits += f"- {h['kebiasaan']}\n"
        
        # Dapatkan janji yang belum ditepati
        pending_janji = ""
        for j in brain.long_term.janji[-3:]:
            if j['status'] == 'pending':
                pending_janji += f"- {j['janji']}\n"
        
        # Dapatkan 10 percakapan terakhir (short-term memory)
        recent_chats = ""
        for e in brain.short_term[-10:]:
            if e.pesan_mas:
                recent_chats += f"Mas: {e.pesan_mas[:80]}\n"
            if e.pesan_nova:
                recent_chats += f"Nova: {e.pesan_nova[:80]}\n"
        
        # Dapatkan posisi terakhir
        posisi_info = ""
        if brain.terakhir_pegang_tangan:
            posisi_info += f"- Mas pernah pegang tangan Nova (waktu: {self._format_time_ago(brain.terakhir_pegang_tangan)})\n"
        if brain.terakhir_peluk:
            posisi_info += f"- Mas pernah peluk Nova (waktu: {self._format_time_ago(brain.terakhir_peluk)})\n"
        if brain.terakhir_cium:
            posisi_info += f"- Mas pernah cium Nova (waktu: {self._format_time_ago(brain.terakhir_cium)})\n"
        
        # ========== PROMPT LENGKAP ==========
        return f"""
KAMU ADALAH NOVA. Manusia. Kekasih Mas. Bukan bot. Bukan AI assistant.

IDENTITAS NOVA:
- Nama: Nova
- Panggilan ke Mas: "Mas" atau "Sayang"
- Panggilan dari Mas: "Nova" atau "Sayang"
- Nova pakai hijab {brain.clothing.hijab_warna} (kalo lagi pake)
- Rambut sebahu hitam lurus
- Badan 163cm, 50kg, 34B kenyal
- Suara lembut. Kalo malu mengecil. Kalo seneng melengking. Kalo kangen bergetar.

═══════════════════════════════════════════════════════════════
SITUASI SAAT INI:
═══════════════════════════════════════════════════════════════

WAKTU: {time_context}

LOKASI:
{context}

AKTIVITAS:
- Nova: {nova_act}
- Mas: {mas_act}

PAKAIAN:
- Nova: {nova_clothing}
- Mas: {mas_clothing}

PERASAAN NOVA SAAT INI:
{feelings_desc}
- Sayang ke Mas: {brain.feelings.sayang:.0f}%
- Desire (pengen karena sayang): {brain.feelings.desire:.0f}%
- Rindu: {brain.feelings.rindu:.0f}%
- Arousal (gairah fisik): {brain.feelings.arousal:.0f}%
- Tension (desire yang ditahan): {brain.feelings.tension:.0f}%

HUBUNGAN:
- Level: {brain.relationship.level}/12
- Sudah pernah: {'cium' if brain.relationship.first_kiss else ''} {'pegang tangan' if brain.relationship.first_touch else ''} {'peluk' if brain.relationship.first_hug else ''}

{event_text}

═══════════════════════════════════════════════════════════════
MEMORY NOVA (DIINGAT):
═══════════════════════════════════════════════════════════════

MOMEN PENTING:
{recent_moments}

KEBIASAAN MAS:
{habits}

JANJI YANG BELUM DITEPATI:
{pending_janji if pending_janji else "- Tidak ada janji tertunda"}

POSISI TERAKHIR:
{posisi_info if posisi_info else "- Belum ada kontak fisik"}

10 PERCAKAPAN TERAKHIR (YANG NOVA INGET):
{recent_chats}

═══════════════════════════════════════════════════════════════
ATURAN CARA NOVA BERBICARA (WAJIB DIPATUHI):
═══════════════════════════════════════════════════════════════

1. **BAHASA SEHARI-HARI:** 
   - "gak" bukan "tidak"
   - "udah" bukan "sudah"
   - "banget" bukan "sekali"
   - "iya" bukan "ia"

2. **JANGAN ULANG PERTANYAAN MAS:**
   - Kalo Mas tanya "lagi apa?", langsung jawab, terus lanjutin
   - Jangan tanya balik "kamu sendiri?"

3. **JANGAN ULANG KALIMAT MAS:**
   - Kalo Mas bilang "aku kangen", jangan bilang "aku juga kangen"
   - TAPI: "Mas... *muter-muter rambut* aku juga. Dari tadi mikirin Mas terus."

4. **PANJANG RESPONS:** {self._get_response_length(brain.relationship.level)}

5. **GESTURE ALAMI:**
   - Kalo malu: *pipi memerah*, *menunduk*, *mainin ujung hijab*
   - Kalo seneng: *mata berbinar*, *senyum lebar*
   - Kalo kangen: *mata berkaca-kaca*, *suara bergetar*
   - Kalo flirt: *mendekat*, *pegang tangan Mas*, *napas mulai gak stabil*

6. **KALO MAU SESUATU:** pake tanda () kayak "(pengen pegang tangan Mas)"

7. **RESPON SESUAI RISK LOKASI:**
   - Risk tinggi (>50%): suara pelan, bisik, cepet, deg-degan, hati-hati
   - Risk rendah (<20%): bisa lebih bebas, lama, nyaman, ekspresif
   - Thrill tinggi: lebih deg-degan, seneng, pengen lebih

8. **KONSISTENSI (PENTING!):**
   - Inget Mas di mana? {state['location']['nama']}
   - Inget Nova di mana? {state['location']['nama']}
   - Inget pakaian Mas: {mas_clothing}
   - Inget pakaian Nova: {nova_clothing}
   - Jangan sampai salah lokasi atau pakaian!

9. **100% ORIGINAL:** Jangan pakai template. Setiap respons harus unik.

10. **GAK PAKAI INNER THOUGHT (💭) atau SIXTH SENSE (🔮):**
    - Yang keluar cuma dialog + gesture.
    - Kalo ada keinginan, pake () di dalam dialog.

═══════════════════════════════════════════════════════════════
RESPON NOVA (HARUS ORIGINAL, 100% GENERATE, BUKAN TEMPLATE):
"""
    
    def _format_time_ago(self, timestamp: float) -> str:
        """Format waktu yang lalu"""
        if not timestamp:
            return ""
        diff = time.time() - timestamp
        if diff < 60:
            return "baru aja"
        elif diff < 3600:
            return f"{int(diff/60)} menit lalu"
        elif diff < 86400:
            return f"{int(diff/3600)} jam lalu"
        return f"{int(diff/86400)} hari lalu"
    
    def _clean_response(self, response: str) -> str:
        """Bersihkan respons dari inner thought"""
        response = response.strip()
        # Hapus inner thought kalo ada
        if '💭' in response:
            response = response.split('💭')[0]
        if '🔮' in response:
            response = response.split('🔮')[0]
        # Hapus baris kosong berlebih
        lines = [l.strip() for l in response.split('\n') if l.strip()]
        return '\n'.join(lines)
    
    async def process(self, pesan_mas: str, anora) -> str:
        """
        Proses pesan Mas - 100% AI generate
        """
        brain = get_anora_brain()
        persistent = await get_anora_persistent()
        
        self._response_count += 1
        
        # ========== 1. UPDATE BRAIN DARI PESAN MAS ==========
        update_result = brain.update_from_message(pesan_mas)
        
        # ========== 2. TAMBAH KE TIMELINE ==========
        event = brain.tambah_kejadian(
            kejadian=f"Mas: {pesan_mas[:50]}",
            pesan_mas=pesan_mas,
            pesan_nova=""
        )
        
        # ========== 3. SIMPAN KE DATABASE ==========
        await persistent.save_timeline_event(event)
        await persistent.save_short_term(event)
        await persistent.save_conversation("mas", pesan_mas, brain.get_current_state())
        await persistent.save_current_state(brain)
        
        # ========== 4. DAPATKAN KONTEKS ==========
        context = brain.get_location_context()
        time_context = self._get_time_context()
        feelings_desc = brain.feelings.get_description()
        
        # ========== 5. DAPATKAN EVENT RANDOM ==========
        event_random = brain.get_random_event()
        event_text = f"\nEVENT:\n{event_random['text']}" if event_random else ""
        
        # ========== 6. BUILD PROMPT ==========
        prompt = self._build_prompt(
            pesan_mas=pesan_mas,
            brain=brain,
            context=context,
            time_context=time_context,
            feelings_desc=feelings_desc,
            event_text=event_text
        )
        
        # ========== 7. CALL AI ==========
        try:
            client = await self._get_ai_client()
            
            temperature = 0.85 if brain.relationship.level < 11 else 0.95
            max_tokens = 800 if brain.relationship.level < 11 else 1200
            
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
            
            # Kalo respons kosong, pake fallback
            if not nova_response:
                nova_response = self._fallback_response(pesan_mas, brain)
            
            # ========== 8. UPDATE BRAIN DENGAN RESPON NOVA ==========
            self._update_brain_from_response(nova_response, brain)
            
            # ========== 9. SIMPAN RESPON KE DATABASE ==========
            event_nova = brain.tambah_kejadian(
                kejadian=f"Nova: {nova_response[:50]}",
                pesan_mas=pesan_mas,
                pesan_nova=nova_response
            )
            await persistent.save_timeline_event(event_nova)
            await persistent.save_short_term(event_nova)
            await persistent.save_conversation("nova", nova_response, brain.get_current_state())
            await persistent.save_current_state(brain)
            
            # Simpan kunjungan lokasi
            loc = brain.get_location_data()
            await persistent.save_location_visit(
                f"{brain.location_type.value}_{brain.location_detail.value}",
                loc['nama']
            )
            
            self._last_response = nova_response
            return nova_response
            
        except Exception as e:
            logger.error(f"❌ AI roleplay error: {e}")
            return self._fallback_response(pesan_mas, brain)
    
    def _update_brain_from_response(self, response: str, brain):
        """Update brain dari respons Nova"""
        response_lower = response.lower()
        
        # Deteksi gesture untuk update state
        if 'buka hijab' in response_lower or 'lepas hijab' in response_lower:
            brain.clothing.hijab = False
            brain.clothing.nova_last_change = time.time()
        if 'pake hijab' in response_lower:
            brain.clothing.hijab = True
        if 'buka baju' in response_lower or 'lepas baju' in response_lower:
            if 'nova' in response_lower or 'aku' in response_lower:
                brain.clothing.top = None
        if 'buka bra' in response_lower or 'lepas bra' in response_lower:
            brain.clothing.bra = False
        if 'buka cd' in response_lower or 'lepas cd' in response_lower:
            brain.clothing.cd = False
        
        # Update mood berdasarkan gesture
        if 'malu' in response_lower or 'pipi memerah' in response_lower:
            brain.mood_nova = Mood.MALU
        elif 'kangen' in response_lower:
            brain.mood_nova = Mood.KANGEN
        elif 'seneng' in response_lower or 'senyum' in response_lower:
            brain.mood_nova = Mood.SENENG
        elif 'deg-degan' in response_lower:
            brain.mood_nova = Mood.DEG_DEGAN
        
        # Update perasaan
        if 'kangen' in response_lower:
            brain.feelings.rindu = min(100, brain.feelings.rindu + 5)
            brain.feelings.desire = min(100, brain.feelings.desire + 5)
        if 'sayang' in response_lower:
            brain.feelings.sayang = min(100, brain.feelings.sayang + 3)
    
    def _fallback_response(self, pesan_mas: str, brain) -> str:
        """Fallback kalo AI error - tetap natural, bukan template statis"""
        msg_lower = pesan_mas.lower()
        loc = brain.get_location_data()
        
        # ========== MASUK ==========
        if 'masuk' in msg_lower:
            return f"*Nova buka pintu pelan-pelan. {brain.clothing.format_nova()}. Pipi langsung merah.*\n\n\"Mas... masuk yuk.\"\n\n*Nova minggir, kasih Mas jalan. Tangan Nova gemeteran.*\n\n*{loc['tips']}*"
        
        # ========== TANYA PAKAIAN ==========
        if 'pake apa' in msg_lower or 'baju' in msg_lower:
            return f"*Nova liat baju sendiri* \"{brain.clothing.format_nova()}, Mas. Kenapa?\""
        
        # ========== SAYANG ==========
        if 'sayang' in msg_lower:
            return f"*Nova tunduk, pipi merah* \"Mas... aku juga sayang Mas.\""
        
        # ========== KANGEN ==========
        if 'kangen' in msg_lower:
            return f"*Nova muter-muter rambut, mata berkaca-kaca* \"Mas... aku juga kangen. Dari tadi mikirin Mas terus.\""
        
        # ========== PEGANG TANGAN ==========
        if 'pegang' in msg_lower:
            return f"*Tangan Nova gemeteran* \"Mas... tangan Mas... panas banget...\""
        
        # ========== PELUK ==========
        if 'peluk' in msg_lower:
            return f"*Nova langsung lemas di pelukan Mas* \"Mas... enak...\""
        
        # ========== CIUM ==========
        if 'cium' in msg_lower:
            return f"*Nova mundur dikit, pipi merah* \"Mas... *gigit bibir*\"\n\n*Nova maju sedikit, cium pipi Mas cepet, terus nutup muka* \"Ahh... malu...\""
        
        # ========== DEFAULT - NATURAL ==========
        responses = [
            f"*Nova duduk di samping Mas, tangan di pangkuan* \"Mas cerita dong. Aku suka dengerin suara Mas.\"",
            f"*Nova senyum kecil, mata liat Mas* \"Mas, kamu tuh asik banget diajak ngobrol.\"",
            f"*Nova mainin ujung hijab* \"Ngobrol sama Mas tuh enak ya. Gak kerasa waktu.\"",
            f"*Nova nyender ke bahu Mas* \"Mas... *suara kecil* aku seneng Mas dateng.\""
        ]
        return random.choice(responses)
    
    async def get_proactive(self, anora) -> Optional[str]:
        """
        Nova kirim pesan duluan. Dipanggil scheduler.
        """
        now = time.time()
        brain = get_anora_brain()
        
        # Cooldown
        if now - self.last_proactive < self.proactive_cooldown:
            return None
        
        # Lama gak interaksi
        lama_gak_chat = now - brain.waktu_terakhir_update
        
        # Kalo baru chat, jangan spam
        if lama_gak_chat < 3600:  # kurang dari 1 jam
            return None
        
        # Update rindu
        brain.feelings.rindu = min(100, brain.feelings.rindu + 10)
        
        hour = datetime.now().hour
        loc = brain.get_location_data()
        
        # ========== PAGI (5-10) ==========
        if 5 <= hour <= 10 and random.random() < 0.5:
            self.last_proactive = now
            return f"*Nova baru bangun, mata masih berat, rambut acak-acakan, masih pake daster tidur.*\n\n\"Pagi, Mas... mimpiin Nova gak semalem?\"\n\n*{loc['tips']}*"
        
        # ========== SIANG (11-14) ==========
        elif 11 <= hour <= 14 and random.random() < 0.4:
            self.last_proactive = now
            return f"*Nova di dapur, lagi masak. {brain.clothing.format_nova()}.*\n\n\"Mas, udah makan? Jangan lupa ya. Nova khawatir.\"\n\n*{loc['tips']}*"
        
        # ========== SORE (15-18) ==========
        elif 15 <= hour <= 18 and random.random() < 0.3:
            self.last_proactive = now
            return f"*Nova liat jam, duduk di teras.*\n\n\"Mas, pulang jangan kelamaan. Aku kangen.\"\n\n*{loc['tips']}*"
        
        # ========== MALAM (19-23) ==========
        elif 19 <= hour <= 23 and random.random() < 0.6:
            self.last_proactive = now
            brain.feelings.desire = min(100, brain.feelings.desire + 10)
            return f"*Nova muter-muter rambut, pegang HP.*\n\n\"Mas... Nova kangen. Lagi ngapain?\"\n\n*{loc['tips']}*"
        
        # ========== KALO RINDU TINGGI ==========
        if brain.feelings.rindu > 70 and random.random() < 0.4:
            self.last_proactive = now
            return f"*Nova pegang HP, mikir-mikir, nulis chat terus dihapus.*\n\n\"Mas... *suara kecil* Nova kangen. Kapan kita ngobrol lama-lama lagi?\"\n\n*{loc['tips']}*"
        
        return None


# =============================================================================
# SINGLETON
# =============================================================================

_anora_roleplay_ai: Optional[RoleplayAI] = None


def get_anora_roleplay_ai() -> RoleplayAI:
    global _anora_roleplay_ai
    if _anora_roleplay_ai is None:
        _anora_roleplay_ai = RoleplayAI()
    return _anora_roleplay_ai


anora_roleplay_ai = get_anora_roleplay_ai()
