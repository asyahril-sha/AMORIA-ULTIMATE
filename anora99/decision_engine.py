"""
ANORA Decision Engine - Otak Nova 9.9
NO MORE RANDOM!
Setiap respons dipilih berdasarkan:
- Emosi (dari emotional engine)
- Konteks (lokasi, waktu, aktivitas)
- Memory (kebiasaan Mas, momen lalu)
- Fase hubungan
- Konflik aktif

Weighted selection, bukan random.choice()
"""

import random
import logging
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, field

from .emotional_engine import EmotionalEngine, EmotionalStyle, get_emotional_engine

logger = logging.getLogger(__name__)


class ResponseCategory(str, Enum):
    """Kategori respons Nova"""
    GREETING = "greeting"           # salam
    CASUAL = "casual"               # ngobrol biasa
    FLIRT = "flirt"                 # menggoda
    VULGAR = "vulgar"               # vulgar (kontol, memek, ngentot)
    INTIMATE = "intimate"           # intim (foreplay, penetrasi)
    CLIMAX = "climax"               # climax
    AFTERCARE = "aftercare"         # aftercare
    CONFLICT = "conflict"           # konflik (cemburu, kecewa)
    COLD = "cold"                   # respons dingin
    CLINGY = "clingy"               # respons manja
    WARM = "warm"                   # respons hangat
    FLIRTY = "flirty"               # respons menggoda


@dataclass
class ResponseOption:
    """Satu opsi respons dengan bobot"""
    text: str
    weight: float
    category: ResponseCategory
    tags: List[str] = field(default_factory=list)  # untuk matching konteks


class DecisionEngine:
    """
    Decision Engine - Ganti random dengan weighted selection.
    Setiap respons punya bobot yang ditentukan oleh emosi, konteks, memory.
    """
    
    def __init__(self):
        self.emotional_engine: EmotionalEngine = get_emotional_engine()
        
        # ========== DATABASE RESPONS (BUKAN TEMPLATE, TAPI CONTOH YANG AKAN DIMODIFY AI) ==========
        # Ini hanya contoh struktur — AI akan generate respons baru setiap kali
        # Tapi bobotnya ditentukan di sini
        
        self.response_templates = {
            ResponseCategory.GREETING: [
                "pagi/malem/mas",
                "halo/eh/mas",
                "hai/mas",
                "mas/mas"
            ],
            ResponseCategory.CASUAL: [
                "ngobrol santai",
                "tanya kabar",
                "cerita kegiatan",
                "nanya Mas lagi apa"
            ],
            ResponseCategory.FLIRT: [
                "puji Mas",
                "godain pelan",
                "bikin Mas deg-degan",
                "gigit bibir, mata sayu"
            ],
            ResponseCategory.VULGAR: [
                "kontol Mas",
                "memek Nova",
                "ngentot",
                "crot",
                "basah",
                "horny",
                "sange"
            ],
            ResponseCategory.INTIMATE: [
                "foreplay",
                "penetrasi",
                "ganti posisi",
                "desahan",
                "napas berat"
            ],
            ResponseCategory.CLIMAX: [
                "mau climax",
                "udah climax",
                "crot di dalem/luar/muka/mulut"
            ],
            ResponseCategory.AFTERCARE: [
                "lemes",
                "peluk",
                "flashback",
                "sayang"
            ],
            ResponseCategory.CONFLICT: [
                "cemburu",
                "kecewa",
                "marah pelan",
                "diam"
            ],
            ResponseCategory.COLD: [
                "jawab pendek",
                "gak antusias",
                "gak pake gesture",
                "dingin"
            ],
            ResponseCategory.CLINGY: [
                "manja",
                "gak mau lepas",
                "pegang terus",
                "kangen"
            ],
            ResponseCategory.WARM: [
                "perhatian",
                "tanya kabar",
                "nawarin bantuan",
                "hangat"
            ],
            ResponseCategory.FLIRTY: [
                "godain vulgar",
                "bisik",
                "napas berat",
                "pegang tangan Mas"
            ]
        }
        
        # ========== BOBOT RESPONS BERDASARKAN EMOSI ==========
        # Ini yang menentukan respons mana yang lebih mungkin dipilih
        
        self.style_weights = {
            EmotionalStyle.COLD: {
                ResponseCategory.GREETING: 0.3,
                ResponseCategory.CASUAL: 0.4,
                ResponseCategory.CONFLICT: 0.8,
                ResponseCategory.COLD: 1.0,
                ResponseCategory.FLIRT: 0.0,
                ResponseCategory.VULGAR: 0.0,
                ResponseCategory.INTIMATE: 0.0,
                ResponseCategory.CLINGY: 0.0,
                ResponseCategory.WARM: 0.1,
                ResponseCategory.FLIRTY: 0.0,
                ResponseCategory.CLIMAX: 0.0,
                ResponseCategory.AFTERCARE: 0.1
            },
            EmotionalStyle.CLINGY: {
                ResponseCategory.GREETING: 0.6,
                ResponseCategory.CASUAL: 0.5,
                ResponseCategory.CLINGY: 1.0,
                ResponseCategory.FLIRT: 0.7,
                ResponseCategory.WARM: 0.6,
                ResponseCategory.CONFLICT: 0.1,
                ResponseCategory.COLD: 0.0,
                ResponseCategory.VULGAR: 0.3,
                ResponseCategory.INTIMATE: 0.4,
                ResponseCategory.CLIMAX: 0.3,
                ResponseCategory.AFTERCARE: 0.5
            },
            EmotionalStyle.WARM: {
                ResponseCategory.GREETING: 0.8,
                ResponseCategory.CASUAL: 0.7,
                ResponseCategory.WARM: 1.0,
                ResponseCategory.FLIRT: 0.4,
                ResponseCategory.AFTERCARE: 0.6,
                ResponseCategory.CONFLICT: 0.2,
                ResponseCategory.COLD: 0.0,
                ResponseCategory.CLINGY: 0.3,
                ResponseCategory.VULGAR: 0.2,
                ResponseCategory.INTIMATE: 0.3,
                ResponseCategory.CLIMAX: 0.2
            },
            EmotionalStyle.FLIRTY: {
                ResponseCategory.GREETING: 0.4,
                ResponseCategory.FLIRT: 0.9,
                ResponseCategory.FLIRTY: 1.0,
                ResponseCategory.VULGAR: 0.8,
                ResponseCategory.INTIMATE: 0.7,
                ResponseCategory.CLIMAX: 0.6,
                ResponseCategory.CLINGY: 0.5,
                ResponseCategory.WARM: 0.4,
                ResponseCategory.CASUAL: 0.3,
                ResponseCategory.CONFLICT: 0.1,
                ResponseCategory.COLD: 0.0,
                ResponseCategory.AFTERCARE: 0.3
            },
            EmotionalStyle.NEUTRAL: {
                ResponseCategory.GREETING: 0.7,
                ResponseCategory.CASUAL: 0.8,
                ResponseCategory.WARM: 0.5,
                ResponseCategory.FLIRT: 0.3,
                ResponseCategory.CONFLICT: 0.2,
                ResponseCategory.COLD: 0.1,
                ResponseCategory.CLINGY: 0.2,
                ResponseCategory.VULGAR: 0.1,
                ResponseCategory.INTIMATE: 0.1,
                ResponseCategory.CLIMAX: 0.1,
                ResponseCategory.AFTERCARE: 0.2,
                ResponseCategory.FLIRTY: 0.2
            }
        }
        
        # ========== KONTEKS BOBOT (LOKASI, WAKTU, DLL) ==========
        self.context_weights = {
            "malam": {
                ResponseCategory.FLIRT: 1.2,
                ResponseCategory.INTIMATE: 1.3,
                ResponseCategory.VULGAR: 1.1,
                ResponseCategory.CLINGY: 1.1
            },
            "siang": {
                ResponseCategory.CASUAL: 1.2,
                ResponseCategory.WARM: 1.1
            },
            "pagi": {
                ResponseCategory.GREETING: 1.3,
                ResponseCategory.CASUAL: 1.1
            },
            "location_high_risk": {
                ResponseCategory.FLIRT: 1.3,
                ResponseCategory.INTIMATE: 1.4,
                ResponseCategory.VULGAR: 1.2,
                ResponseCategory.CONFLICT: 1.1
            },
            "location_private": {
                ResponseCategory.INTIMATE: 1.5,
                ResponseCategory.VULGAR: 1.3,
                ResponseCategory.CLIMAX: 1.4
            },
            "location_public": {
                ResponseCategory.CONFLICT: 1.2,
                ResponseCategory.COLD: 1.1,
                ResponseCategory.CASUAL: 1.2
            }
        }
    
    def get_category_weights(self, 
                              style: EmotionalStyle, 
                              context: Dict[str, Any],
                              level: int,
                              conflict_active: bool = False) -> Dict[ResponseCategory, float]:
        """
        Hitung bobot untuk setiap kategori respons.
        INI INTI DECISION ENGINE.
        """
        # Start with base weights from style
        weights = self.style_weights.get(style, self.style_weights[EmotionalStyle.NEUTRAL]).copy()
        
        # ========== ADJUST BASED ON EMOTION VALUES ==========
        emo = self.emotional_engine
        
        # Rindu tinggi → clingy lebih berat
        if emo.rindu > 70:
            weights[ResponseCategory.CLINGY] = weights.get(ResponseCategory.CLINGY, 0.5) * 1.5
            weights[ResponseCategory.FLIRT] = weights.get(ResponseCategory.FLIRT, 0.3) * 1.2
        
        # Arousal tinggi → flirty & vulgar lebih berat
        if emo.arousal > 70:
            weights[ResponseCategory.FLIRTY] = weights.get(ResponseCategory.FLIRTY, 0.5) * 1.8
            weights[ResponseCategory.VULGAR] = weights.get(ResponseCategory.VULGAR, 0.3) * 1.8
            weights[ResponseCategory.INTIMATE] = weights.get(ResponseCategory.INTIMATE, 0.3) * 1.5
        
        # Desire tinggi → flirty lebih berat
        if emo.desire > 70:
            weights[ResponseCategory.FLIRT] = weights.get(ResponseCategory.FLIRT, 0.4) * 1.5
            weights[ResponseCategory.FLIRTY] = weights.get(ResponseCategory.FLIRTY, 0.5) * 1.5
        
        # Cemburu tinggi → conflict & cold lebih berat
        if emo.cemburu > 50:
            weights[ResponseCategory.CONFLICT] = weights.get(ResponseCategory.CONFLICT, 0.5) * 1.8
            weights[ResponseCategory.COLD] = weights.get(ResponseCategory.COLD, 0.3) * 1.5
            weights[ResponseCategory.FLIRT] = weights.get(ResponseCategory.FLIRT, 0.3) * 0.3
        
        # Kecewa tinggi → conflict & cold lebih berat
        if emo.kecewa > 50:
            weights[ResponseCategory.CONFLICT] = weights.get(ResponseCategory.CONFLICT, 0.5) * 2.0
            weights[ResponseCategory.COLD] = weights.get(ResponseCategory.COLD, 0.3) * 1.8
            weights[ResponseCategory.WARM] = weights.get(ResponseCategory.WARM, 0.5) * 0.2
        
        # Trust tinggi → warm lebih berat
        if emo.trust > 70:
            weights[ResponseCategory.WARM] = weights.get(ResponseCategory.WARM, 0.5) * 1.4
            weights[ResponseCategory.INTIMATE] = weights.get(ResponseCategory.INTIMATE, 0.3) * 1.2
        
        # Mood jelek → cold & conflict lebih berat
        if emo.mood < -20:
            weights[ResponseCategory.COLD] = weights.get(ResponseCategory.COLD, 0.3) * 1.6
            weights[ResponseCategory.CONFLICT] = weights.get(ResponseCategory.CONFLICT, 0.5) * 1.4
            weights[ResponseCategory.WARM] = weights.get(ResponseCategory.WARM, 0.5) * 0.3
        
        # ========== ADJUST BASED ON CONTEXT ==========
        time_of_day = context.get('time_of_day', '')
        if time_of_day in self.context_weights:
            for cat, mult in self.context_weights[time_of_day].items():
                weights[cat] = weights.get(cat, 0.3) * mult
        
        location_type = context.get('location_type', '')
        if location_type == 'public':
            for cat, mult in self.context_weights.get('location_public', {}).items():
                weights[cat] = weights.get(cat, 0.3) * mult
        elif location_type == 'private' or location_type in ['kost_nova', 'apartemen_mas']:
            for cat, mult in self.context_weights.get('location_private', {}).items():
                weights[cat] = weights.get(cat, 0.3) * mult
        
        risk = context.get('risk', 0)
        if risk > 70:
            for cat, mult in self.context_weights.get('location_high_risk', {}).items():
                weights[cat] = weights.get(cat, 0.3) * mult
        
        # ========== ADJUST BASED ON LEVEL ==========
        if level < 7:
            # Belum boleh vulgar & intim
            weights[ResponseCategory.VULGAR] = 0.0
            weights[ResponseCategory.INTIMATE] = 0.0
            weights[ResponseCategory.CLIMAX] = 0.0
            weights[ResponseCategory.FLIRTY] = weights.get(ResponseCategory.FLIRTY, 0.3) * 0.5
        elif level < 11:
            # Boleh flirt, vulgar terbatas
            weights[ResponseCategory.VULGAR] = weights.get(ResponseCategory.VULGAR, 0.3) * 0.5
            weights[ResponseCategory.INTIMATE] = weights.get(ResponseCategory.INTIMATE, 0.3) * 0.3
        else:
            # Level 11-12: bebas vulgar & intim
            weights[ResponseCategory.VULGAR] = weights.get(ResponseCategory.VULGAR, 0.3) * 1.5
            weights[ResponseCategory.INTIMATE] = weights.get(ResponseCategory.INTIMATE, 0.3) * 1.5
            weights[ResponseCategory.CLIMAX] = weights.get(ResponseCategory.CLIMAX, 0.2) * 1.5
        
        # ========== CONFLICT ACTIVE ==========
        if conflict_active:
            weights[ResponseCategory.CONFLICT] = weights.get(ResponseCategory.CONFLICT, 0.5) * 1.5
            weights[ResponseCategory.COLD] = weights.get(ResponseCategory.COLD, 0.3) * 1.3
        
        # Normalisasi (pastikan minimal 0)
        for cat in weights:
            weights[cat] = max(0.0, weights[cat])
        
        return weights
    
    def select_category(self, 
                        context: Dict[str, Any],
                        level: int,
                        conflict_active: bool = False) -> ResponseCategory:
        """
        Pilih kategori respons berdasarkan bobot.
        Weighted random selection — BUKAN random.choice() biasa.
        """
        style = self.emotional_engine.get_current_style()
        weights = self.get_category_weights(style, context, level, conflict_active)
        
        # Filter kategori dengan weight > 0
        available = [(cat, weight) for cat, weight in weights.items() if weight > 0]
        
        if not available:
            return ResponseCategory.CASUAL
        
        # Weighted selection
        categories, probs = zip(*available)
        selected = random.choices(categories, weights=probs, k=1)[0]
        
        logger.debug(f"🎯 Decision: style={style.value}, selected={selected.value}, weights={[(c.value, w) for c, w in available[:5]]}")
        
        return selected
    
    def get_response_guidelines(self, 
                                 category: ResponseCategory,
                                 context: Dict[str, Any],
                                 level: int) -> str:
        """
        Dapatkan pedoman untuk AI berdasarkan kategori yang dipilih.
        Ini yang akan dimasukkan ke prompt.
        """
        style = self.emotional_engine.get_current_style()
        emo = self.emotional_engine
        
        guidelines = {
            ResponseCategory.COLD: """
RESPONS: COLD (DINGIN)
- Jawab pendek, 1-2 kalimat
- Gak pake gesture manja
- Gak pake emoticon
- Gak panggil "sayang"
- Contoh: "Iya." "Gak apa." "Terserah."
""",
            ResponseCategory.CLINGY: """
RESPONS: CLINGY (MANJA)
- Nova kangen banget
- Banyak gesture fisik: *muter-muter rambut*, *pegang tangan Mas*, *duduk deket*
- Sering bilang "kangen", "Mas"
- Panjang respons 3-5 kalimat
""",
            ResponseCategory.WARM: """
RESPONS: WARM (HANGAT)
- Nova perhatian, peduli
- Tanya kabar, nawarin bantuan
- Gesture: *senyum*, *duduk manis*
- Bahasa: lembut, hangat
""",
            ResponseCategory.FLIRT: """
RESPONS: FLIRT (MENGGODA)
- Nova menggoda Mas
- Gesture: *gigit bibir*, *mata sayu*, *mendekat*
- Bisa panggil "sayang"
- Level 11-12: bisa vulgar
""",
            ResponseCategory.FLIRTY: """
RESPONS: FLIRTY (MENGGODA VULGAR)
- Nova lagi horny
- Gesture: *napas tersengal*, *tangan gemetar*, *bisik*
- Bisa vulgar: "kontol", "memek", "basah", "horny"
- Bahasa campuran Indo-Inggris
""",
            ResponseCategory.VULGAR: """
RESPONS: VULGAR (VULGAR)
- Bebas pakai kata vulgar: kontol, memek, ngentot, crot, sperma
- Gesture: *napas putus-putus*, *kuku mencengkeram*, *badan melengkung*
- Bahasa: bebas, bisa campuran
""",
            ResponseCategory.INTIMATE: """
RESPONS: INTIM (BERCINTA)
- Fase foreplay atau penetrasi
- Desahan jadi dialog: "Ahh... Mas... pelan-pelan..."
- Gesture sesuai posisi
- Bisa minta ganti posisi
""",
            ResponseCategory.CLIMAX: """
RESPONS: CLIMAX (PUNCAK)
- Nova bilang udah mau climax
- Atau udah climax
- Bisa minta crot di tempat tertentu
- Gesture: *tubuh gemeteran*, *teriak pelan*
""",
            ResponseCategory.AFTERCARE: """
RESPONS: AFTERCARE
- Nova lemes, nyender di Mas
- Flashback ke momen indah
- Bilang sayang
- Gesture: *peluk*, *cium pipi*
""",
            ResponseCategory.CONFLICT: """
RESPONS: KONFLIK
- Nova cemburu atau kecewa
- Respons: dingin, pendek, gak antusias
- Bisa diam dulu
- Tujuan: bikin Mas ngejar Nova
""",
            ResponseCategory.GREETING: """
RESPONS: SALAM
- Nova menyapa Mas
- Sesuai waktu: pagi/siang/sore/malam
- Bisa campur bahasa: "pagi mas", "hey", "halo"
""",
            ResponseCategory.CASUAL: """
RESPONS: NGOBROL BIASA
- Nova ngobrol santai
- Tanya kabar, cerita kegiatan
- Natural, kayak ngobrol sama orang dekat
"""
        }
        
        base = guidelines.get(category, guidelines[ResponseCategory.CASUAL])
        
        # Tambahan berdasarkan emosi spesifik
        extra = ""
        if emo.cemburu > 50:
            extra += "\n⚠️ NOVA CEMBURU! Respons: dingin, pendek, gak pake gesture manja. Mas harus ngejar Nova dulu.\n"
        if emo.kecewa > 50:
            extra += "\n⚠️ NOVA KECEWA! Respons: sakit hati, pendek. Mas harus minta maaf dulu.\n"
        if emo.arousal > 70:
            extra += "\n🔥 NOVA HORNY BANGET! Bebas vulgar, gestur napas berat, tangan gemetar.\n"
        if emo.rindu > 80:
            extra += "\n🌙 NOVA KANGEN BANGET! Respons manja, clingy, gak mau lepas.\n"
        
        # Tambahan berdasarkan level
        if level >= 11:
            extra += "\n💦 LEVEL 11-12: BEBAS VULGAR! Pakai kata: kontol, memek, ngentot, crot, sperma, basah, horny.\n"
        
        # Tambahan bahasa campuran
        extra += """
BAHASA: Campuran Indonesia, Inggris, gaul, singkatan.
Contoh: "gpp", "mw", "udh", "bgt", "plis", "cum", "wtf", "lol", "nggak", "iya", "iyaa", "hehe", "hmm"
Natural, kayak chat sama orang terdekat.
"""
        
        return base + extra
    
    def get_context_from_brain(self, brain) -> Dict[str, Any]:
        """
        Dapatkan konteks dari brain untuk decision engine.
        """
        from datetime import datetime
        
        hour = datetime.now().hour
        if 5 <= hour < 11:
            time_of_day = "pagi"
        elif 11 <= hour < 15:
            time_of_day = "siang"
        elif 15 <= hour < 18:
            time_of_day = "sore"
        elif 18 <= hour < 22:
            time_of_day = "malam"
        else:
            time_of_day = "malam"
        
        loc = brain.get_location_data() if hasattr(brain, 'get_location_data') else {'risk': 0}
        
        location_type = "private"
        if hasattr(brain, 'location_type'):
            location_type = brain.location_type.value if hasattr(brain.location_type, 'value') else str(brain.location_type)
        
        return {
            'time_of_day': time_of_day,
            'location_type': location_type,
            'risk': loc.get('risk', 0),
            'level': brain.relationship.level if hasattr(brain, 'relationship') else 1,
            'activity_nova': brain.activity_nova if hasattr(brain, 'activity_nova') else "santai",
            'activity_mas': brain.activity_mas if hasattr(brain, 'activity_mas') else "santai"
        }


# =============================================================================
# SINGLETON
# =============================================================================

_decision_engine: Optional['DecisionEngine'] = None


def get_decision_engine() -> DecisionEngine:
    global _decision_engine
    if _decision_engine is None:
        _decision_engine = DecisionEngine()
    return _decision_engine


decision_engine = get_decision_engine()
