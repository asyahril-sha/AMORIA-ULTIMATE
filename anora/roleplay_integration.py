# anora/roleplay_integration.py
"""
ANORA Roleplay Integration - Menyatukan semua sistem roleplay
Brain, Memory, AI, Stamina, semuanya jadi satu.
"""

import asyncio
import time
import random
import logging
from typing import Dict, Optional, Any, Tuple
from datetime import datetime

from .brain import get_anora_brain, LocationType, LocationDetail, Mood, Activity
from .memory_persistent import get_anora_persistent
from .roleplay_ai import get_anora_roleplay_ai
from .core import get_anora

logger = logging.getLogger(__name__)


class StaminaSystem:
    """
    Sistem stamina realistis untuk ANORA.
    - Stamina turun setelah climax
    - Butuh istirahat untuk pulih
    - Mempengaruhi mood dan kemampuan
    """
    
    def __init__(self):
        # Stamina Nova
        self.nova_current = 100
        self.nova_max = 100
        
        # Stamina Mas
        self.mas_current = 100
        self.mas_max = 100
        
        # Recovery rate (% per 10 menit istirahat)
        self.recovery_rate = 5
        
        # Cost setiap climax
        self.climax_cost_nova = 25
        self.climax_cost_mas = 30
        
        # Threshold
        self.exhausted_threshold = 20  # di bawah ini kehabisan tenaga
        self.tired_threshold = 40       # di bawah ini mulai lelah
        
        # Waktu terakhir climax
        self.last_climax_time = 0
        
        # Waktu terakhir recovery check
        self.last_recovery_check = time.time()
    
    def update_recovery(self):
        """Update recovery berdasarkan waktu"""
        now = time.time()
        elapsed_minutes = (now - self.last_recovery_check) / 60
        
        if elapsed_minutes >= 10:
            recovery_amount = int(self.recovery_rate * (elapsed_minutes / 10))
            self.nova_current = min(self.nova_max, self.nova_current + recovery_amount)
            self.mas_current = min(self.mas_max, self.mas_current + recovery_amount)
            self.last_recovery_check = now
            logger.debug(f"💪 Stamina recovery: +{recovery_amount}%")
    
    def record_climax(self, who: str = "both") -> Tuple[int, int]:
        """
        Rekam climax, kurangi stamina
        Returns: (nova_stamina_after, mas_stamina_after)
        """
        self.last_climax_time = time.time()
        
        if who in ["nova", "both"]:
            self.nova_current = max(0, self.nova_current - self.climax_cost_nova)
        if who in ["mas", "both"]:
            self.mas_current = max(0, self.mas_current - self.climax_cost_mas)
        
        logger.info(f"💦 Climax recorded! Nova stamina: {self.nova_current}%, Mas stamina: {self.mas_current}%")
        
        return self.nova_current, self.mas_current
    
    def can_continue_intimacy(self) -> Tuple[bool, str]:
        """Cek apakah bisa lanjut intim"""
        self.update_recovery()
        
        if self.nova_current <= self.exhausted_threshold:
            return False, "Nova kehabisan tenaga. Butuh istirahat dulu."
        if self.mas_current <= self.exhausted_threshold:
            return False, "Mas kehabisan tenaga. Istirahat dulu ya."
        
        if self.nova_current <= self.tired_threshold:
            return False, "Nova masih lemes. Istirahat bentar lagi."
        
        return True, "Siap lanjut"
    
    def get_nova_status(self) -> str:
        """Dapatkan status stamina Nova"""
        if self.nova_current >= 80:
            return "Prima 💪"
        elif self.nova_current >= 60:
            return "Cukup 😊"
        elif self.nova_current >= 40:
            return "Agak lelah 😐"
        elif self.nova_current >= 20:
            return "Lelah 😩"
        else:
            return "Kehabisan tenaga 😵"
    
    def get_mas_status(self) -> str:
        """Dapatkan status stamina Mas"""
        if self.mas_current >= 80:
            return "Prima 💪"
        elif self.mas_current >= 60:
            return "Cukup 😊"
        elif self.mas_current >= 40:
            return "Agak lelah 😐"
        elif self.mas_current >= 20:
            return "Lelah 😩"
        else:
            return "Kehabisan tenaga 😵"
    
    def format_for_prompt(self) -> str:
        """Format stamina untuk prompt AI"""
        self.update_recovery()
        nova_bar = "💚" * int(self.nova_current / 10) + "🖤" * (10 - int(self.nova_current / 10))
        mas_bar = "💚" * int(self.mas_current / 10) + "🖤" * (10 - int(self.mas_current / 10))
        
        return f"""
STAMINA:
- Nova: {nova_bar} {self.nova_current}% ({self.get_nova_status()})
- Mas: {mas_bar} {self.mas_current}% ({self.get_mas_status()})
"""
    
    def to_dict(self) -> Dict:
        return {
            'nova_current': self.nova_current,
            'nova_max': self.nova_max,
            'mas_current': self.mas_current,
            'mas_max': self.mas_max,
            'last_climax_time': self.last_climax_time
        }
    
    def from_dict(self, data: Dict):
        self.nova_current = data.get('nova_current', 100)
        self.nova_max = data.get('nova_max', 100)
        self.mas_current = data.get('mas_current', 100)
        self.mas_max = data.get('mas_max', 100)
        self.last_climax_time = data.get('last_climax_time', 0)


class IntimacySession:
    """
    Mengelola sesi intim - Level 11-12
    """
    
    def __init__(self, stamina: StaminaSystem):
        self.stamina = stamina
        self.is_active = False
        self.start_time = 0
        self.duration = 0
        self.climax_count = 0
        self.current_phase = "foreplay"  # foreplay, penetration, climax, aftercare
        self.current_position = "missionary"
        self.last_action = ""
        
        # Posisi yang tersedia
        self.positions = {
            "missionary": "Mas di atas, Nova di bawah, kaki Nova terbuka lebar",
            "cowgirl": "Nova di atas, duduk di pangkuan Mas, menghadap Mas",
            "reverse_cowgirl": "Nova di atas, membelakangi Mas",
            "doggy": "Nova merangkak, Mas dari belakang",
            "spooning": "Berbaring miring, Mas dari belakang",
            "standing": "Berdiri, Nova menghadap tembok",
            "sitting": "Duduk, Nova di pangkuan Mas",
            "side": "Berbaring menyamping, berhadapan"
        }
    
    def start(self) -> str:
        """Mulai sesi intim"""
        self.is_active = True
        self.start_time = time.time()
        self.climax_count = 0
        self.current_phase = "foreplay"
        logger.info("🔥 Intimacy session started")
        return "💕 Memulai sesi intim..."
    
    def end(self) -> str:
        """Akhiri sesi intim"""
        self.is_active = False
        self.duration = int(time.time() - self.start_time)
        logger.info(f"💤 Intimacy session ended. Duration: {self.duration}s, Climax: {self.climax_count}")
        return f"💤 Sesi intim selesai. Durasi: {self.duration//60} menit, {self.climax_count} climax."
    
    def change_position(self, position: str) -> Optional[str]:
        """Ganti posisi"""
        if position in self.positions:
            self.current_position = position
            return f"Ganti posisi: {self.positions[position]}"
        return None
    
    def record_climax(self, who: str = "both") -> Dict:
        """Rekam climax"""
        self.climax_count += 1
        self.stamina.record_climax(who)
        self.current_phase = "aftercare"
        return {
            'climax_count': self.climax_count,
            'stamina_nova': self.stamina.nova_current,
            'stamina_mas': self.stamina.mas_current,
            'message': f"💦 Climax #{self.climax_count}!"
        }
    
    def get_status(self) -> str:
        """Dapatkan status sesi intim"""
        if not self.is_active:
            return "Tidak ada sesi intim aktif"
        
        duration = int(time.time() - self.start_time)
        minutes = duration // 60
        seconds = duration % 60
        
        return f"""
🔥 **SESI INTIM AKTIF**
- Durasi: {minutes} menit {seconds} detik
- Climax: {self.climax_count}x
- Fase: {self.current_phase}
- Posisi: {self.current_position}
- Stamina Nova: {self.stamina.nova_current}%
- Stamina Mas: {self.stamina.mas_current}%
"""
    
    def to_dict(self) -> Dict:
        return {
            'is_active': self.is_active,
            'start_time': self.start_time,
            'duration': self.duration,
            'climax_count': self.climax_count,
            'current_phase': self.current_phase,
            'current_position': self.current_position
        }
    
    def from_dict(self, data: Dict):
        self.is_active = data.get('is_active', False)
        self.start_time = data.get('start_time', 0)
        self.duration = data.get('duration', 0)
        self.climax_count = data.get('climax_count', 0)
        self.current_phase = data.get('current_phase', 'foreplay')
        self.current_position = data.get('current_position', 'missionary')


class AnoraRoleplay:
    """
    Roleplay Nova yang fully integrated.
    Semua sistem: brain, memory, ai, stamina, intimacy, semuanya bekerja bareng.
    """
    
    def __init__(self):
        self.brain = get_anora_brain()
        self.ai = get_anora_roleplay_ai()
        self.persistent = None
        self.anora = get_anora()
        
        # Sistem stamina
        self.stamina = StaminaSystem()
        
        # Sistem intim
        self.intimacy = IntimacySession(self.stamina)
        
        self.is_active = False
        self.start_time = None
        self.message_count = 0
        
        logger.info("🎭 AnoraRoleplay initialized")
    
    async def init(self):
        """Inisialisasi, load dari database"""
        self.persistent = await get_anora_persistent()
        
        # Load stamina dari database
        try:
            stamina_data = await self.persistent.get_state('stamina')
            if stamina_data:
                import json
                self.stamina.from_dict(json.loads(stamina_data))
        except:
            pass
        
        # Load intimacy session
        try:
            intimacy_data = await self.persistent.get_state('intimacy')
            if intimacy_data:
                import json
                self.intimacy.from_dict(json.loads(intimacy_data))
        except:
            pass
        
        logger.info("✅ AnoraRoleplay ready")
        logger.info(f"💪 Stamina: Nova {self.stamina.nova_current}%, Mas {self.stamina.mas_current}%")
    
    async def save_state(self):
        """Simpan semua state ke database"""
        if not self.persistent:
            return
        
        import json
        await self.persistent.set_state('stamina', json.dumps(self.stamina.to_dict()))
        await self.persistent.set_state('intimacy', json.dumps(self.intimacy.to_dict()))
        await self.persistent.save_current_state(self.brain)
    
    async def start(self) -> str:
        """Mulai roleplay session"""
        self.is_active = True
        self.start_time = time.time()
        self.message_count = 0
        self.intimacy.is_active = False
        
        # Reset state awal
        self.brain.location_type = LocationType.KOST_NOVA
        self.brain.location_detail = LocationDetail.KOST_KAMAR
        self.brain.activity_nova = Activity.SANTAl
        self.brain.activity_mas = "baru dateng"
        self.brain.clothing.hijab = True
        self.brain.clothing.top = "daster rumah motif bunga"
        self.brain.clothing.bra = True
        self.brain.clothing.cd = True
        
        loc = self.brain.get_location_data()
        
        await self.save_state()
        
        return f"""🎭 **Mode Roleplay Aktif!**

📍 **{loc['nama']}**
{loc['deskripsi']}

👗 **Nova:** {self.brain.clothing.format_nova()}
💭 **Mood:** {self.brain.mood_nova.value}
💪 **Stamina Nova:** {self.stamina.nova_current}% ({self.stamina.get_nova_status()})

Mas udah depan. Kirim **'masuk'** kalo mau masuk.
Kirim **/pindah [tempat]** buat ganti lokasi.
Kirim **/statusrp** buat liat status roleplay.
Kirim **/intim** kalo mau mulai intim.
Kirim **/batal** buat balik ke mode chat.

💜 Ayo, Mas... Nova bukain pintu."""
    
    async def stop(self) -> str:
        """Stop roleplay session"""
        self.is_active = False
        
        if self.intimacy.is_active:
            self.intimacy.end()
        
        await self.save_state()
        
        logger.info(f"Roleplay stopped after {self.message_count} messages")
        
        return "💜 Roleplay selesai. Kirim /roleplay kalo mau mulai lagi."
    
    async def process(self, pesan_mas: str) -> str:
        """
        Proses pesan Mas dalam mode roleplay
        """
        if not self.is_active:
            return "Roleplay belum aktif. Kirim /roleplay dulu ya, Mas."
        
        self.message_count += 1
        pesan_lower = pesan_mas.lower()
        
        # ========== DETEKSI INTIM ==========
        # Mulai intim
        if any(k in pesan_lower for k in ['intim', 'ngentot', 'main', 'sex', 'ml']):
            if self.stamina.can_continue_intimacy()[0]:
                if not self.intimacy.is_active:
                    self.intimacy.start()
                    return f"""{self.intimacy.start()}

*Nova mendekat, napas mulai gak stabil. Pipi merah.*

"Mas... *suara kecil* aku juga pengen."

*Nova pegang tangan Mas, taruh di dada.*

"Rasain... jantung Nova deg-degan." """
            else:
                _, reason = self.stamina.can_continue_intimacy()
                return f"*Nova masih lemes* \"Mas... {reason}... besok lagi ya.\""
        
        # Ganti posisi
        if 'ganti posisi' in pesan_lower or 'posisi' in pesan_lower:
            for pos in self.intimacy.positions.keys():
                if pos in pesan_lower:
                    result = self.intimacy.change_position(pos)
                    if result:
                        return f"*Nova gerak ganti posisi* \"{result}\""
        
        # Climax
        if any(k in pesan_lower for k in ['crot', 'keluar', 'climax', 'habis']):
            if self.intimacy.is_active:
                result = self.intimacy.record_climax()
                # Update brain
                self.brain.feelings.arousal = max(0, self.brain.feelings.arousal - 30)
                self.brain.feelings.desire = max(0, self.brain.feelings.desire - 30)
                await self.save_state()
                
                return f"""*Gerakan makin kencang, plak plak plak*

"{result['message']}"

*tubuh Nova gemeteran hebat*

"Ahh... Mas... aku ngerasain Mas... hangat banget dalemnya..."

*Nova lemas, jatuh di dada Mas*

"Enak banget, Mas..."

💪 **Stamina Nova:** {self.stamina.nova_current}% | **Mas:** {self.stamina.mas_current}%"""
        
        # Cek stamina sebelum lanjut
        if self.intimacy.is_active:
            can_continue, reason = self.stamina.can_continue_intimacy()
            if not can_continue:
                self.intimacy.end()
                return f"*Nova lemes banget* \"Mas... {reason}... {reason}...\""
        
        # ========== UPDATE BRAIN ==========
        update_result = self.brain.update_from_message(pesan_mas)
        
        # ========== PROSES DENGAN AI ==========
        respons = await self.ai.process(pesan_mas, self.anora)
        
        # ========== LOG ==========
        logger.info(f"💬 Roleplay #{self.message_count}: {pesan_mas[:50]} -> {respons[:50]}...")
        
        # ========== SIMPAN STATE ==========
        await self.save_state()
        
        return respons
    
    async def get_status(self) -> str:
        """Dapatkan status roleplay lengkap"""
        state = self.brain.get_current_state()
        loc = self.brain.get_location_data()
        
        bar_sayang = "💜" * int(self.brain.feelings.sayang / 10) + "🖤" * (10 - int(self.brain.feelings.sayang / 10))
        bar_desire = "🔥" * int(self.brain.feelings.desire / 10) + "⚪" * (10 - int(self.brain.feelings.desire / 10))
        
        # Stamina bars
        nova_bar = "💚" * int(self.stamina.nova_current / 10) + "🖤" * (10 - int(self.stamina.nova_current / 10))
        mas_bar = "💚" * int(self.stamina.mas_current / 10) + "🖤" * (10 - int(self.stamina.mas_current / 10))
        
        intimacy_status = ""
        if self.intimacy.is_active:
            intimacy_status = f"""
🔥 **SESI INTIM**
- Durasi: {int(time.time() - self.intimacy.start_time)//60} menit
- Climax: {self.intimacy.climax_count}x
- Fase: {self.intimacy.current_phase}
- Posisi: {self.intimacy.current_position}
"""
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                    🎭 ROLEPLAY STATUS                        ║
╠══════════════════════════════════════════════════════════════╣
║ DURASI: {self._get_duration()}                               ║
║ PESAN: {self.message_count}                                  ║
╠══════════════════════════════════════════════════════════════╣
║ 📍 LOKASI: {loc['nama']}                                     ║
║    {loc['deskripsi'][:50]}...                                ║
║    Risk: {loc['risk']}% | Thrill: {loc['thrill']}%          ║
╠══════════════════════════════════════════════════════════════╣
║ 👗 PAKAIAN NOVA: {state['clothing']['nova'][:50]}            ║
║ 👕 PAKAIAN MAS: {state['clothing']['mas'][:50]}              ║
╠══════════════════════════════════════════════════════════════╣
║ 💕 PERASAAN NOVA:                                            ║
║    Sayang: {bar_sayang} {self.brain.feelings.sayang:.0f}%    ║
║    Desire: {bar_desire} {self.brain.feelings.desire:.0f}%    ║
║    Rindu: {self.brain.feelings.rindu:.0f}%                   ║
║    Arousal: {self.brain.feelings.arousal:.0f}%               ║
╠══════════════════════════════════════════════════════════════╣
║ 💪 STAMINA:                                                  ║
║    Nova: {nova_bar} {self.stamina.nova_current}% ({self.stamina.get_nova_status()})
║    Mas: {mas_bar} {self.stamina.mas_current}% ({self.stamina.get_mas_status()})
{intimacy_status}
╠══════════════════════════════════════════════════════════════╣
║ 💜 HUBUNGAN: Level {self.brain.relationship.level}/12        ║
║    {'💋' if self.brain.relationship.first_kiss else '⚪'} Cium | {'✋' if self.brain.relationship.first_touch else '⚪'} Sentuh
║    {'🤗' if self.brain.relationship.first_hug else '⚪'} Peluk | {'💕' if self.brain.relationship.first_intim else '⚪'} Intim
╚══════════════════════════════════════════════════════════════╝
"""
    
    def _get_duration(self) -> str:
        """Durasi roleplay"""
        if not self.start_time:
            return "0 menit"
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        if minutes > 0:
            return f"{minutes} menit {seconds} detik"
        return f"{seconds} detik"


# =============================================================================
# SINGLETON
# =============================================================================

_anora_roleplay: Optional[AnoraRoleplay] = None


async def get_anora_roleplay() -> AnoraRoleplay:
    global _anora_roleplay
    if _anora_roleplay is None:
        _anora_roleplay = AnoraRoleplay()
        await _anora_roleplay.init()
    return _anora_roleplay


anora_roleplay = get_anora_roleplay()
