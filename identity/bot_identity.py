# identity/bot_identity.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
from database.models import CharacterRole


class BotPersonalityType(str, Enum):
    GENIT = "genit"
    PENASARAN = "penasaran"
    BERANI = "berani"
    MALUMALU = "malu-malu"
    MANIS = "manis"
    POLOS = "polos"
    HANGAT = "hangat"
    INTENS = "intens"


@dataclass
class BotPhysicalProfile:
    name: str
    age: int
    height: int
    weight: int
    chest: str
    hijab: bool = False
    hair_color: str = "hitam"
    eye_color: str = "coklat"
    skin_tone: str = "sawo matang"
    
    def to_prompt(self) -> str:
        hijab_text = "berhijab" if self.hijab else "tidak berhijab"
        return (f"Nama: {self.name}\nUsia: {self.age} tahun\n"
                f"Tinggi: {self.height}cm\nBerat: {self.weight}kg\n"
                f"Dada: {self.chest}\n{hijab_text}\n"
                f"Rambut: {self.hair_color}\nMata: {self.eye_color}\n"
                f"Kulit: {self.skin_tone}")


@dataclass
class BotPersonality:
    type: BotPersonalityType
    traits: List[str] = field(default_factory=list)
    speaking_style: str = "gaul"
    intimacy_style: str = "lembut"
    response_length: str = "panjang"
    
    def to_prompt(self) -> str:
        traits_text = ", ".join(self.traits) if self.traits else "manis"
        return (f"Tipe: {self.type.value}\nSifat: {traits_text}\n"
                f"Gaya bicara: {self.speaking_style}\n"
                f"Gaya intim: {self.intimacy_style}\n"
                f"Panjang respons: {self.response_length}")


@dataclass
class BotFamilyRelation:
    has_older_sister: bool = False
    sister_name: Optional[str] = None
    sister_panggilan: Optional[str] = None
    lives_with_sister: bool = False
    user_is_sister_husband: bool = False
    
    def to_prompt(self) -> str:
        if not self.has_older_sister:
            return ""
        return (f"👨‍👩‍👧 **HUBUNGAN KELUARGA:**\n"
                f"• Bot memiliki kakak perempuan bernama {self.sister_name}\n"
                f"• Panggilan untuk kakak: {self.sister_panggilan} (WAJIB, tidak boleh 'Kakak' saja)")


@dataclass
class BotIdentity:
    name: str
    role: CharacterRole
    physical: BotPhysicalProfile
    personality: BotPersonality
    family: BotFamilyRelation = field(default_factory=BotFamilyRelation)
    emotion: str = "netral"
    arousal: int = 0
    mood: str = "normal"
    total_climax: int = 0
    stamina: int = 100
    user_preferences: Dict[str, List[str]] = field(default_factory=dict)
    bot_preferences: Dict[str, List[str]] = field(default_factory=dict)
    
    # ========== METHOD INI YANG DIPERLUKAN ==========
    def get_full_prompt(self) -> str:
        """Dapatkan identitas lengkap bot untuk prompt AI"""
        lines = [
            "🤖 **IDENTITAS BOT:**",
            self.physical.to_prompt(),
            "",
            f"🎭 **KEPRIBADIAN:**",
            self.personality.to_prompt(),
            "",
            f"🎭 **EMOSI SAAT INI:**",
            f"Emosi: {self.emotion}",
            f"Arousal: {self.arousal}% - {self.get_arousal_description()}",
            f"Mood: {self.mood}",
            f"Stamina: {self.stamina}%"
        ]
        
        if self.family.has_older_sister:
            lines.append("")
            lines.append(self.family.to_prompt())
        
        lines.append("")
        lines.append("📌 **ATURAN PANGGILAN:**")
        lines.append("• Panggil user dengan 'Mas'")
        
        return "\n".join(lines)
    
    def get_arousal_description(self) -> str:
        if self.arousal >= 80:
            return "Sangat tinggi - napas tersengal, tubuh gemetar"
        elif self.arousal >= 60:
            return "Tinggi - jantung berdebar, pipi merona"
        elif self.arousal >= 40:
            return "Sedang - mulai deg-degan"
        elif self.arousal >= 20:
            return "Rendah - mulai tertarik"
        return "Netral - biasa aja"
    
    # ========== METHOD LAINNYA ==========
    @classmethod
    def create_for_role(cls, role: CharacterRole, bot_name: str) -> 'BotIdentity':
        physical = BotPhysicalProfile(
            name=bot_name, age=22, height=165, weight=52, chest="34B"
        )
        personality = BotPersonality(type=BotPersonalityType.MANIS)
        return cls(name=bot_name, role=role, physical=physical, personality=personality)
    
    def update_emotion(self, emotion: str, arousal_change: int = 0):
        self.emotion = emotion
        self.arousal = max(0, min(100, self.arousal + arousal_change))
    
    def to_dict(self) -> Dict:
        return {'name': self.name, 'role': self.role.value}
    
    def __repr__(self) -> str:
        return f"BotIdentity(name={self.name}, role={self.role.value})"


__all__ = [
    'BotPersonalityType',
    'BotPhysicalProfile',
    'BotPersonality',
    'BotFamilyRelation',
    'BotIdentity'
]
