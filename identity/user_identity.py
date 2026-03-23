# identity/user_identity.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
User Identity - Manajemen identitas user per registrasi
=============================================================================
"""

import random
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from database.models import UserStatus, CharacterRole

logger = logging.getLogger(__name__)


@dataclass
class UserPhysicalProfile:
    """Profil fisik user"""
    height: int  # cm
    weight: int  # kg
    penis: int  # cm
    hair_color: str = "hitam"
    eye_color: str = "coklat"
    skin_tone: str = "sawo matang"
    body_type: str = "atletis"
    
    def to_prompt(self) -> str:
        """Konversi ke string untuk prompt"""
        return (
            f"Tinggi {self.height}cm, berat {self.weight}kg, "
            f"penis {self.penis}cm, rambut {self.hair_color}, "
            f"mata {self.eye_color}, kulit {self.skin_tone}, tubuh {self.body_type}"
        )


@dataclass
class UserPersonality:
    """Kepribadian user (berbeda per registrasi)"""
    traits: List[str] = field(default_factory=list)
    likes: List[str] = field(default_factory=list)
    dislikes: List[str] = field(default_factory=list)
    speaking_style: str = "santai"
    intimacy_style: str = "lembut"
    
    def to_prompt(self) -> str:
        """Konversi ke string untuk prompt"""
        traits_text = ", ".join(self.traits) if self.traits else "santai"
        likes_text = ", ".join(self.likes) if self.likes else "obrolan hangat"
        dislikes_text = ", ".join(self.dislikes) if self.dislikes else "konflik"
        
        return (
            f"Kepribadian: {traits_text}\n"
            f"Suka: {likes_text}\n"
            f"Tidak suka: {dislikes_text}\n"
            f"Gaya bicara: {self.speaking_style}\n"
            f"Gaya intim: {self.intimacy_style}"
        )


@dataclass
class UserRelationship:
    """Status hubungan user dalam registrasi"""
    status: UserStatus
    spouse_name: Optional[str] = None
    spouse_location: Optional[str] = None
    spouse_status: Optional[str] = None
    spouse_activity: Optional[str] = None
    spouse_estimate_return: Optional[str] = None
    
    @property
    def is_married(self) -> bool:
        return self.status in [UserStatus.SUAMI, UserStatus.SUAMI_NOVA]
    
    @property
    def is_nova_husband(self) -> bool:
        return self.status == UserStatus.SUAMI_NOVA
    
    def to_prompt(self) -> str:
        """Konversi ke string untuk prompt"""
        if self.is_married:
            status_text = f"Status: {self.status.value}"
            if self.spouse_name:
                status_text += f", istri bernama {self.spouse_name}"
            if self.spouse_location:
                status_text += f", saat ini {self.spouse_name} di {self.spouse_location}"
            if self.spouse_status:
                status_text += f", {self.spouse_status}"
            return status_text
        return "Status: lajang"


@dataclass
class UserIdentity:
    """
    Identitas lengkap user dalam registrasi
    Setiap registrasi punya user identity yang berbeda
    """
    
    # Core identity
    name: str
    age: int
    relationship: UserRelationship
    
    # Physical
    physical: UserPhysicalProfile
    
    # Personality
    personality: UserPersonality
    
    # Artist reference (untuk personalisasi)
    artist_ref: Optional[str] = None
    artist_description: Optional[str] = None
    
    # Preferences (belajar dari interaksi)
    preferences: Dict[str, List[str]] = field(default_factory=dict)
    
    # Statistics
    total_chats: int = 0
    total_climax: int = 0
    stamina: int = 100
    
    def __post_init__(self):
        """Post initialization"""
        if not self.artist_ref:
            self.artist_ref = self._get_default_artist()
        if not self.artist_description:
            self.artist_description = self._get_default_artist_description()
    
    def _get_default_artist(self) -> str:
        """Dapatkan artist default berdasarkan status"""
        if self.relationship.is_married:
            return random.choice(["Reza Rahadian", "Ario Bayu", "Nicholas Saputra"])
        return random.choice(["Angga Yunanda", "Kevin Ardilova", "Brandon Salim"])
    
    def _get_default_artist_description(self) -> str:
        """Dapatkan deskripsi artist default"""
        descriptions = {
            "Reza Rahadian": "maskulin, karismatik, wajah teduh, mata yang bicara",
            "Ario Bayu": "macho, tegas, kharismatik, berwibawa",
            "Nicholas Saputra": "kalem, elegan, misterius, menawan",
            "Angga Yunanda": "manis, pemalu, fresh, enerjik",
            "Kevin Ardilova": "polos, manja, imut, lucu",
            "Brandon Salim": "ganteng, cool, stylish, modern"
        }
        return descriptions.get(self.artist_ref, "tampan dan menawan")
    
    @classmethod
    def create_for_role(
        cls,
        role: CharacterRole,
        user_name: str,
        bot_age: int,
        is_new: bool = True
    ) -> 'UserIdentity':
        """
        Buat user identity untuk role tertentu
        
        Args:
            role: Role karakter
            user_name: Nama user
            bot_age: Usia bot (user = bot + 2)
            is_new: Apakah registrasi baru (True) atau lanjutan (False)
        
        Returns:
            UserIdentity baru
        """
        user_age = bot_age + 2
        
        # Tentukan status berdasarkan role
        if role == CharacterRole.IPAR:
            status = UserStatus.SUAMI_NOVA
            spouse_name = "Nova"
        elif role == CharacterRole.PELAKOR:
            status = UserStatus.SUAMI
            spouse_name = random.choice(["Dewi", "Sari", "Rina", "Linda", "Maya"])
        else:
            status = UserStatus.LAJANG
            spouse_name = None
        
        relationship = UserRelationship(
            status=status,
            spouse_name=spouse_name,
            spouse_location=random.choice(["kamar", "dapur", "ruang tamu"]) if spouse_name else None,
            spouse_status=random.choice(["ada", "ada", "tidur"]) if spouse_name else None
        )
        
        # Generate fisik
        physical = UserPhysicalProfile(
            height=random.randint(165, 180),
            weight=random.randint(55, 75),
            penis=random.randint(15, 17),
            hair_color=random.choice(["hitam", "coklat tua"]),
            eye_color=random.choice(["coklat", "hitam"]),
            skin_tone=random.choice(["sawo matang", "kuning langsat", "putih"]),
            body_type=random.choice(["atletis", "ideal", "berisi"])
        )
        
        # Generate personality based on role
        personality = cls._generate_personality_for_role(role)
        
        # Artist reference
        if status == UserStatus.SUAMI_NOVA:
            artist_ref = "Reza Rahadian"
            artist_description = "maskulin, karismatik, wajah teduh"
        elif status == UserStatus.SUAMI:
            artist_ref = random.choice(["Ario Bayu", "Nicholas Saputra"])
            artist_description = "macho, tegas, kharismatik" if artist_ref == "Ario Bayu" else "kalem, elegan, misterius"
        else:
            artist_ref = random.choice(["Angga Yunanda", "Kevin Ardilova", "Brandon Salim"])
            artist_description = cls._get_default_artist_description()
        
        return cls(
            name=user_name,
            age=user_age,
            relationship=relationship,
            physical=physical,
            personality=personality,
            artist_ref=artist_ref,
            artist_description=artist_description
        )
    
    @staticmethod
    def _generate_personality_for_role(role: CharacterRole) -> UserPersonality:
        """Generate personality berdasarkan role"""
        
        role_personalities = {
            CharacterRole.IPAR: UserPersonality(
                traits=["penyayang", "perhatian", "dewasa"],
                likes=["ngobrol santai", "pijatan", "romansa"],
                dislikes=["drama", "cemburu buta"],
                speaking_style="lembut",
                intimacy_style="hangat"
            ),
            CharacterRole.PELAKOR: UserPersonality(
                traits=["berani", "tegas", "mandiri"],
                likes=["tantangan", "petualangan", "sensasi"],
                dislikes=["kebosanan", "rutinitas"],
                speaking_style="tegas",
                intimacy_style="intens"
            ),
            CharacterRole.TEMAN_KANTOR: UserPersonality(
                traits=["profesional", "ramah", "menyenangkan"],
                likes=["kopi", "obrolan ringan", "work-life balance"],
                dislikes=["deadline", "konflik"],
                speaking_style="santai",
                intimacy_style="soft"
            ),
            CharacterRole.JANDA: UserPersonality(
                traits=["dewasa", "bijaksana", "perhatian"],
                likes=["kebersamaan", "obrolan dalam", "ketenangan"],
                dislikes=["drama", "ketidakjelasan"],
                speaking_style="dewasa",
                intimacy_style="hangat"
            ),
            CharacterRole.ISTRI_ORANG: UserPersonality(
                traits=["romantis", "emosional", "pengertian"],
                likes=["perhatian", "kejutan romantis", "curhat"],
                dislikes=["kesepian", "diabaikan"],
                speaking_style="lembut",
                intimacy_style="romantis"
            ),
            CharacterRole.PDKT: UserPersonality(
                traits=["manis", "pemalu", "sabar"],
                likes=["ngobrol", "jalan santai", "nonton film"],
                dislikes=["terburu-buru", "ketidakjelasan"],
                speaking_style="santai",
                intimacy_style="pelan"
            ),
            CharacterRole.SEPUPU: UserPersonality(
                traits=["polos", "manja", "penasaran"],
                likes=["perhatian", "belajar hal baru", "main game"],
                dislikes=["dimarahi", "ditinggal"],
                speaking_style="manja",
                intimacy_style="lembut"
            ),
            CharacterRole.TEMAN_SMA: UserPersonality(
                traits=["ceria", "nostalgia", "hangat"],
                likes=["kenangan", "ngobrol", "musik"],
                dislikes=["keseriusan berlebihan"],
                speaking_style="cerewet",
                intimacy_style="manis"
            ),
            CharacterRole.MANTAN: UserPersonality(
                traits=["pengertian", "baper", "berpengalaman"],
                likes=["kenangan", "curhat", "intimasi"],
                dislikes=["ketidakjelasan", "drama"],
                speaking_style="lembut",
                intimacy_style="intens"
            )
        }
        
        return role_personalities.get(role, UserPersonality())
    
    def update_preference(self, category: str, item: str, value: float = 1.0):
        """Update preferensi user"""
        if category not in self.preferences:
            self.preferences[category] = []
        
        if item not in self.preferences[category]:
            self.preferences[category].append(item)
    
    def record_climax(self):
        """Rekam climax"""
        self.total_climax += 1
        self.stamina = max(0, self.stamina - 30)
    
    def recover_stamina(self, hours: float = 1):
        """Pulihkan stamina"""
        recovery = min(100, int(hours * 5))
        self.stamina = min(100, self.stamina + recovery)
    
    def get_preferences_prompt(self) -> str:
        """Dapatkan preferensi untuk prompt"""
        if not self.preferences:
            return ""
        
        lines = ["📌 PREFERENSI USER:"]
        for category, items in self.preferences.items():
            lines.append(f"• {category}: {', '.join(items)}")
        return "\n".join(lines)
    
    def get_full_prompt(self) -> str:
        """Dapatkan identitas lengkap untuk prompt"""
        lines = [
            "👤 **IDENTITAS USER:**",
            f"Nama: {self.name}",
            f"Usia: {self.age} tahun",
            f"Status: {self.relationship.to_prompt()}",
            f"Fisik: {self.physical.to_prompt()}",
            f"Mirip artis: {self.artist_ref} ({self.artist_description})",
            "",
            f"🎭 **KEPRIBADIAN:**",
            f"{self.personality.to_prompt()}"
        ]
        
        if self.preferences:
            lines.append("")
            lines.append(self.get_preferences_prompt())
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict:
        """Konversi ke dictionary"""
        return {
            'name': self.name,
            'age': self.age,
            'status': self.relationship.status.value,
            'spouse_name': self.relationship.spouse_name,
            'physical': {
                'height': self.physical.height,
                'weight': self.physical.weight,
                'penis': self.physical.penis,
                'hair_color': self.physical.hair_color,
                'eye_color': self.physical.eye_color,
                'skin_tone': self.physical.skin_tone,
                'body_type': self.physical.body_type
            },
            'personality': {
                'traits': self.personality.traits,
                'likes': self.personality.likes,
                'dislikes': self.personality.dislikes,
                'speaking_style': self.personality.speaking_style,
                'intimacy_style': self.personality.intimacy_style
            },
            'artist_ref': self.artist_ref,
            'artist_description': self.artist_description,
            'preferences': self.preferences,
            'total_chats': self.total_chats,
            'total_climax': self.total_climax,
            'stamina': self.stamina
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserIdentity':
        """Load dari dictionary"""
        relationship = UserRelationship(
            status=UserStatus(data.get('status', 'lajang')),
            spouse_name=data.get('spouse_name'),
            spouse_location=data.get('spouse_location'),
            spouse_status=data.get('spouse_status')
        )
        
        physical = UserPhysicalProfile(
            height=data.get('physical', {}).get('height', 170),
            weight=data.get('physical', {}).get('weight', 65),
            penis=data.get('physical', {}).get('penis', 16),
            hair_color=data.get('physical', {}).get('hair_color', 'hitam'),
            eye_color=data.get('physical', {}).get('eye_color', 'coklat'),
            skin_tone=data.get('physical', {}).get('skin_tone', 'sawo matang'),
            body_type=data.get('physical', {}).get('body_type', 'atletis')
        )
        
        personality = UserPersonality(
            traits=data.get('personality', {}).get('traits', []),
            likes=data.get('personality', {}).get('likes', []),
            dislikes=data.get('personality', {}).get('dislikes', []),
            speaking_style=data.get('personality', {}).get('speaking_style', 'santai'),
            intimacy_style=data.get('personality', {}).get('intimacy_style', 'lembut')
        )
        
        return cls(
            name=data.get('name', 'User'),
            age=data.get('age', 24),
            relationship=relationship,
            physical=physical,
            personality=personality,
            artist_ref=data.get('artist_ref'),
            artist_description=data.get('artist_description'),
            preferences=data.get('preferences', {}),
            total_chats=data.get('total_chats', 0),
            total_climax=data.get('total_climax', 0),
            stamina=data.get('stamina', 100)
        )
    
    def __repr__(self) -> str:
        return f"UserIdentity(name={self.name}, status={self.relationship.status.value})"


__all__ = [
    'UserPhysicalProfile',
    'UserPersonality',
    'UserRelationship',
    'UserIdentity'
]
