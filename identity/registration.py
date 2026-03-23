# identity/registration.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
Registration Model - Multi-Identity System
=============================================================================
"""

import time
import random
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

from database.models import CharacterRole, UserStatus, Registration as DBRegistration
from database.models import USER_PHYSICAL_TEMPLATES


class CharacterStatus(str, Enum):
    """Status karakter dalam registrasi"""
    ACTIVE = "active"
    CLOSED = "closed"
    ENDED = "ended"


@dataclass
class BotIdentity:
    """Identitas bot dalam registrasi"""
    name: str
    role: CharacterRole
    age: int = 22
    height: int = 165
    weight: int = 52
    chest: str = "34B"
    hijab: bool = False
    
    # Role-specific
    family_relation: Optional[str] = None
    
    @property
    def display_name(self) -> str:
        return f"{self.name} ({self.role.value.upper()})"
    
    @property
    def physical_description(self) -> str:
        hijab_text = "berhijab" if self.hijab else "tidak berhijab"
        return f"{self.age} tahun, {self.height}cm, {self.weight}kg, dada {self.chest}, {hijab_text}"
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'role': self.role.value,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'chest': self.chest,
            'hijab': self.hijab
        }


@dataclass
class UserIdentity:
    """Identitas user dalam registrasi"""
    name: str
    status: UserStatus
    age: int = 24
    height: int = 170
    weight: int = 65
    penis: int = 16
    artist_ref: Optional[str] = None
    artist_description: Optional[str] = None
    
    # Role-specific
    spouse_name: Optional[str] = None
    spouse_location: Optional[str] = None
    spouse_status: Optional[str] = None
    
    @property
    def is_married(self) -> bool:
        return self.status in [UserStatus.SUAMI, UserStatus.SUAMI_NOVA]
    
    @property
    def display_name(self) -> str:
        status_text = "Suami Nova" if self.status == UserStatus.SUAMI_NOVA else \
                      "Suami" if self.status == UserStatus.SUAMI else "Lajang"
        return f"{self.name} ({status_text})"
    
    @property
    def physical_description(self) -> str:
        return f"{self.age} tahun, {self.height}cm, {self.weight}kg, penis {self.penis}cm, mirip {self.artist_ref or 'pria tampan'}"
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'status': self.status.value,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'penis': self.penis,
            'artist_ref': self.artist_ref,
            'spouse_name': self.spouse_name
        }


@dataclass
class CharacterRegistration:
    """
    Registrasi karakter - satu dunia virtual dengan identitas bot dan user
    Format ID: {ROLE}-{SEQUENCE}
    Contoh: IPAR-001, PDKT-002
    """
    
    # Identitas
    id: str
    role: CharacterRole
    sequence: int
    status: CharacterStatus = CharacterStatus.ACTIVE
    
    # Identity objects
    bot: BotIdentity = field(default_factory=lambda: None)
    user: UserIdentity = field(default_factory=lambda: None)
    
    # Progress
    level: int = 1
    total_chats: int = 0
    total_climax_bot: int = 0
    total_climax_user: int = 0
    stamina_bot: int = 100
    stamina_user: int = 100
    
    # ===== TAMBAHKAN INI UNTUK WEIGHTED MEMORY =====
    weighted_memory_score: float = 0.5
    
    # Intimacy Cycle
    in_intimacy_cycle: bool = False
    intimacy_cycle_count: int = 0
    last_climax_time: Optional[float] = None
    cooldown_until: Optional[float] = None
    
    # Timestamps
    created_at: float = field(default_factory=time.time)
    last_updated: float = field(default_factory=time.time)
    
    # Metadata
    metadata: Dict = field(default_factory=dict)
    
    @classmethod
    def create_new(
        cls,
        role: CharacterRole,
        sequence: int,
        user_name: Optional[str] = None,
        bot_name: Optional[str] = None
    ) -> 'CharacterRegistration':
        """
        Buat registrasi baru dengan generate identity otomatis
        """
        template = USER_PHYSICAL_TEMPLATES.get(role)
        
        # Generate nama user
        if not user_name:
            user_names = {
                CharacterRole.IPAR: ["Budi", "Andi", "Rizky", "Dian", "Eko", "Fajar", "Gilang", "Hendra"],
                CharacterRole.PELAKOR: ["Hendra", "Rudi", "Tono", "Agus", "Bayu", "Candra", "Dodi"],
                CharacterRole.TEMAN_KANTOR: ["Rizky", "Dian", "Andre", "Fajar", "Gilang", "Hendra"],
                CharacterRole.JANDA: ["Wahyu", "Hendra", "Teguh", "Pras", "Yoga"],
                CharacterRole.ISTRI_ORANG: ["Rizky", "Dian", "Andre", "Fajar", "Gilang"],
                CharacterRole.PDKT: ["Rizky", "Andre", "Fajar", "Gilang", "Kevin"],
                CharacterRole.SEPUPU: ["Rizky", "Andre", "Fajar", "Gilang", "Kevin"],
                CharacterRole.TEMAN_SMA: ["Rizky", "Andre", "Fajar", "Gilang", "Kevin"],
                CharacterRole.MANTAN: ["Rizky", "Dian", "Andre", "Fajar", "Gilang"]
            }
            user_name = random.choice(user_names.get(role, ["User"]))
        
        # Generate nama bot
        if not bot_name:
            bot_names = {
                CharacterRole.IPAR: ["Sari", "Dewi", "Maya", "Putri", "Anita", "Lestari", "Wulan"],
                CharacterRole.PELAKOR: ["Vina", "Sasha", "Bella", "Cantika", "Mira", "Ira"],
                CharacterRole.TEMAN_KANTOR: ["Diana", "Linda", "Ayu", "Dita", "Vera", "Nina"],
                CharacterRole.JANDA: ["Rina", "Tuti", "Susi", "Maya", "Ira", "Vina"],
                CharacterRole.ISTRI_ORANG: ["Dewi", "Sari", "Rina", "Linda", "Tina"],
                CharacterRole.PDKT: ["Aurora", "Cinta", "Kirana", "Fika", "Nadia", "Amara"],
                CharacterRole.SEPUPU: ["Putri", "Nadia", "Sari", "Dina", "Lina", "Tari"],
                CharacterRole.TEMAN_SMA: ["Anita", "Bella", "Cici", "Dina", "Eva", "Fani"],
                CharacterRole.MANTAN: ["Sarah", "Nadia", "Maya", "Rina", "Vina", "Dewi"]
            }
            bot_name = random.choice(bot_names.get(role, ["Amoria"]))
        
        # Generate usia
        bot_age = random.randint(20, 25)
        user_age = bot_age + 2
        
        # Generate fisik
        bot_height = random.randint(155, 170)
        bot_weight = random.randint(45, 60)
        user_height = random.randint(165, 180)
        user_weight = random.randint(55, 75)
        user_penis = random.randint(15, 17)
        
        # Status user berdasarkan role
        if role == CharacterRole.IPAR:
            user_status = UserStatus.SUAMI_NOVA
            spouse_name = "Nova"
        elif role == CharacterRole.PELAKOR:
            user_status = UserStatus.SUAMI
            spouse_name = random.choice(["Dewi", "Sari", "Rina", "Linda"])
        else:
            user_status = UserStatus.LAJANG
            spouse_name = None
        
        # Artist reference
        artist_ref = template.artist_ref if template else None
        artist_description = template.artist_description if template else "pria tampan"
        
        # Bot Identity
        bot = BotIdentity(
            name=bot_name,
            role=role,
            age=bot_age,
            height=bot_height,
            weight=bot_weight,
            chest=random.choice(["32B", "34A", "34B", "34C"]),
            hijab=role in [CharacterRole.ISTRI_ORANG] and random.random() > 0.5
        )
        
        # User Identity
        user = UserIdentity(
            name=user_name,
            status=user_status,
            age=user_age,
            height=user_height,
            weight=user_weight,
            penis=user_penis,
            artist_ref=artist_ref,
            artist_description=artist_description,
            spouse_name=spouse_name
        )
        
        # Generate ID
        registration_id = f"{role.value.upper()}-{sequence:03d}"
        
        return cls(
            id=registration_id,
            role=role,
            sequence=sequence,
            bot=bot,
            user=user,
            weighted_memory_score=0.5,
            created_at=time.time(),
            last_updated=time.time()
        )
    
    def get_score(self) -> float:
        """Hitung score untuk ranking"""
        total_chat_score = min(100, self.total_chats) / 100
        level_score = self.level / 12
        climax_score = min(50, self.total_climax_bot + self.total_climax_user) / 50
        
        return (total_chat_score * 0.3) + (level_score * 0.4) + (climax_score * 0.3)
    
    def can_start_intimacy(self) -> Tuple[bool, str]:
        """Cek apakah bisa memulai intim"""
        if self.level < 10:
            return False, f"Level masih {self.level}/10. Butuh level 10 untuk intim."
        
        if self.stamina_bot < 20:
            return False, f"Stamina bot {self.stamina_bot}% < 20%"
        
        if self.stamina_user < 20:
            return False, f"Stamina user {self.stamina_user}% < 20%"
        
        if self.cooldown_until and time.time() < self.cooldown_until:
            remaining = int((self.cooldown_until - time.time()) / 60)
            return False, f"Masih dalam cooldown aftercare ({remaining} menit tersisa)"
        
        return True, "OK"
    
    def record_climax(self, is_bot: bool = True):
        """Rekam climax"""
        if is_bot:
            self.total_climax_bot += 1
            self.stamina_bot = max(0, self.stamina_bot - 30)
        else:
            self.total_climax_user += 1
            self.stamina_user = max(0, self.stamina_user - 30)
        
        self.last_climax_time = time.time()
        self.cooldown_until = time.time() + (3 * 3600)
        self.last_updated = time.time()
    
    def start_intimacy_cycle(self):
        """Mulai siklus intim"""
        self.in_intimacy_cycle = True
        self.intimacy_cycle_count += 1
        self.last_updated = time.time()
    
    def end_intimacy_cycle(self):
        """Akhiri siklus intim (setelah aftercare)"""
        self.in_intimacy_cycle = False
        self.level = 10
        self.last_updated = time.time()
    
    def get_progress_to_next_level(self) -> float:
        """Dapatkan progress ke level berikutnya"""
        from config import settings
        
        if self.level <= 10:
            target = settings.level.level_targets.get(self.level + 1, 0)
            if target == 0:
                return 100.0
            current_target = settings.level.level_targets.get(self.level, 0)
            progress = ((self.total_chats - current_target) / (target - current_target)) * 100
            return max(0, min(100, progress))
        else:
            if self.level == 11:
                total = settings.level.level_11_max - settings.level.level_11_min
                if total <= 0:
                    return 0
                progress = ((self.total_chats - settings.level.level_11_min) / total) * 100
                return max(0, min(100, progress))
            elif self.level == 12:
                total = settings.level.level_12_max - settings.level.level_12_min
                if total <= 0:
                    return 100
                progress = ((self.total_chats - settings.level.level_12_min) / total) * 100
                return max(0, min(100, progress))
        
        return 0
    
    def to_db_registration(self) -> DBRegistration:
        """Convert ke database model"""
        return DBRegistration(
            id=self.id,
            role=self.role,
            sequence=self.sequence,
            status=self.status,
            created_at=self.created_at,
            last_updated=self.last_updated,
            bot_name=self.bot.name,
            bot_age=self.bot.age,
            bot_height=self.bot.height,
            bot_weight=self.bot.weight,
            bot_chest=self.bot.chest,
            bot_hijab=self.bot.hijab,
            user_name=self.user.name,
            user_status=self.user.status,
            user_age=self.user.age,
            user_height=self.user.height,
            user_weight=self.user.weight,
            user_penis=self.user.penis,
            user_artist_ref=self.user.artist_ref,
            level=self.level,
            total_chats=self.total_chats,
            total_climax_bot=self.total_climax_bot,
            total_climax_user=self.total_climax_user,
            stamina_bot=self.stamina_bot,
            stamina_user=self.stamina_user,
            weighted_memory_score=self.weighted_memory_score,
            in_intimacy_cycle=self.in_intimacy_cycle,
            intimacy_cycle_count=self.intimacy_cycle_count,
            last_climax_time=self.last_climax_time,
            cooldown_until=self.cooldown_until,
            metadata=self.metadata
        )
    
    @classmethod
    def from_db_registration(cls, db_reg: DBRegistration) -> 'CharacterRegistration':
        """Create from database model"""
        bot = BotIdentity(
            name=db_reg.bot_name,
            role=db_reg.role,
            age=db_reg.bot_age,
            height=db_reg.bot_height,
            weight=db_reg.bot_weight,
            chest=db_reg.bot_chest,
            hijab=db_reg.bot_hijab
        )
        
        user = UserIdentity(
            name=db_reg.user_name,
            status=db_reg.user_status,
            age=db_reg.user_age,
            height=db_reg.user_height,
            weight=db_reg.user_weight,
            penis=db_reg.user_penis,
            artist_ref=db_reg.user_artist_ref
        )
        
        if db_reg.user_status == UserStatus.SUAMI_NOVA:
            user.spouse_name = "Nova"
        
        return cls(
            id=db_reg.id,
            role=db_reg.role,
            sequence=db_reg.sequence,
            status=db_reg.status,
            bot=bot,
            user=user,
            level=db_reg.level,
            total_chats=db_reg.total_chats,
            total_climax_bot=db_reg.total_climax_bot,
            total_climax_user=db_reg.total_climax_user,
            stamina_bot=db_reg.stamina_bot,
            stamina_user=db_reg.stamina_user,
            weighted_memory_score=getattr(db_reg, 'weighted_memory_score', 0.5),
            in_intimacy_cycle=db_reg.in_intimacy_cycle,
            intimacy_cycle_count=db_reg.intimacy_cycle_count,
            last_climax_time=db_reg.last_climax_time,
            cooldown_until=db_reg.cooldown_until,
            created_at=db_reg.created_at,
            last_updated=db_reg.last_updated,
            metadata=db_reg.metadata
        )
    
    def format_status(self) -> str:
        """Format status untuk ditampilkan"""
        status_emoji = "🟢" if self.status == CharacterStatus.ACTIVE else "⚪" if self.status == CharacterStatus.CLOSED else "🔴"
        
        return (
            f"{status_emoji} **{self.bot.name}** ({self.role.value.upper()})\n"
            f"   👤 User: {self.user.display_name}\n"
            f"   📊 Level {self.level}/12 | {self.total_chats} chat | {self.total_climax_bot + self.total_climax_user} climax\n"
            f"   🔥 Stamina: {self.stamina_bot}% (bot) / {self.stamina_user}% (user)"
        )
    
    def __repr__(self) -> str:
        return f"CharacterRegistration(id={self.id}, role={self.role.value}, user={self.user.name}, bot={self.bot.name})"


__all__ = [
    'CharacterStatus',
    'BotIdentity',
    'UserIdentity',
    'CharacterRegistration',
]
