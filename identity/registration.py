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
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from database.models import CharacterRole, UserStatus, Registration as DBRegistration
from database.models import USER_PHYSICAL_TEMPLATES

# =============================================================================
# IMPORT DARI FILE TERPISAH (SINGLE SOURCE OF TRUTH)
# =============================================================================
from .bot_identity import BotIdentity, BotPersonality, BotPhysicalProfile, BotPersonalityType, BotFamilyRelation
from .user_identity import UserIdentity, UserPhysicalProfile, UserPersonality, UserRelationship

logger = logging.getLogger(__name__)


class CharacterStatus(str, Enum):
    """Status karakter dalam registrasi"""
    ACTIVE = "active"
    CLOSED = "closed"
    ENDED = "ended"


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
    
    # Identity objects (menggunakan class dari file terpisah)
    bot: BotIdentity
    user: UserIdentity
    
    # Progress
    level: int = 1
    total_chats: int = 0
    total_climax_bot: int = 0
    total_climax_user: int = 0
    stamina_bot: int = 100
    stamina_user: int = 100
    
    # Intimacy Cycle
    in_intimacy_cycle: bool = False
    intimacy_cycle_count: int = 0
    last_climax_time: Optional[float] = None
    cooldown_until: Optional[float] = None
    
    # Weighted Memory
    weighted_memory_score: float = 0.5
    weighted_memory_data: Dict = field(default_factory=dict)
    
    # Emotional Bias
    emotional_bias: Dict = field(default_factory=dict)
    
    # Secondary Emotion
    secondary_emotion: Optional[str] = None
    secondary_arousal: int = 0
    secondary_emotion_reason: Optional[str] = None
    
    # Physical Sensation
    physical_sensation: str = "biasa aja"
    physical_hunger: int = 30
    physical_thirst: int = 30
    physical_temperature: int = 25
    
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
        
        Args:
            role: Role karakter (IPAR, PDKT, dll)
            sequence: Nomor urut (1, 2, 3, ...)
            user_name: Nama user (opsional, random jika None)
            bot_name: Nama bot (opsional, random jika None)
        
        Returns:
            CharacterRegistration baru
        """
        # Get template untuk role
        template = USER_PHYSICAL_TEMPLATES.get(role)
        
        # =========================================================
        # GENERATE NAMA
        # =========================================================
        
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
        
        # =========================================================
        # GENERATE USIA DAN FISIK
        # =========================================================
        
        # Generate usia (bot 20-25, user = bot + 2)
        bot_age = random.randint(20, 25)
        user_age = bot_age + 2
        
        # Generate tinggi dan berat bot
        bot_height = random.randint(155, 170)
        bot_weight = random.randint(45, 60)
        
        # Generate tinggi dan berat user
        user_height = random.randint(165, 180)
        user_weight = random.randint(55, 75)
        
        # Generate penis size
        user_penis = random.randint(15, 17)
        
        # =========================================================
        # GENERATE STATUS USER
        # =========================================================
        
        # Status user berdasarkan role
        if role == CharacterRole.IPAR:
            user_status = UserStatus.SUAMI_NOVA
            spouse_name = "Nova"
        elif role == CharacterRole.PELAKOR:
            user_status = UserStatus.SUAMI
            spouse_name = random.choice(["Dewi", "Sari", "Rina", "Linda", "Maya"])
        else:
            user_status = UserStatus.LAJANG
            spouse_name = None
        
        # =========================================================
        # GENERATE ARTIST REFERENCE
        # =========================================================
        
        artist_ref = template.artist_ref if template else None
        artist_description = template.artist_description if template else "pria tampan"
        
        # =========================================================
        # BUAT BOT IDENTITY (MENGGUNAKAN FACTORY METHOD)
        # =========================================================
        
        bot = BotIdentity.create_for_role(role, bot_name)
        
        # Override physical yang sudah di-generate dengan nilai random
        bot.physical.age = bot_age
        bot.physical.height = bot_height
        bot.physical.weight = bot_weight
        
        # =========================================================
        # BUAT USER IDENTITY
        # =========================================================
        
        relationship = UserRelationship(
            status=user_status,
            spouse_name=spouse_name,
            spouse_location=random.choice(["kamar", "dapur", "ruang tamu"]) if spouse_name else None,
            spouse_status=random.choice(["ada", "ada", "tidur"]) if spouse_name else None
        )
        
        user_physical = UserPhysicalProfile(
            height=user_height,
            weight=user_weight,
            penis=user_penis,
            hair_color=random.choice(["hitam", "coklat tua"]),
            eye_color=random.choice(["coklat", "hitam"]),
            skin_tone=random.choice(["sawo matang", "kuning langsat", "putih"]),
            body_type=random.choice(["atletis", "ideal", "berisi"])
        )
        
        user_personality = UserPersonality(
            traits=["santai", "penyayang", "perhatian"],
            likes=["ngobrol santai", "jalan-jalan", "nonton film"],
            dislikes=["drama", "konflik", "kebohongan"],
            speaking_style="santai",
            intimacy_style="lembut"
        )
        
        user = UserIdentity(
            name=user_name,
            age=user_age,
            relationship=relationship,
            physical=user_physical,
            personality=user_personality,
            artist_ref=artist_ref,
            artist_description=artist_description
        )
        
        # Generate ID
        registration_id = f"{role.value.upper()}-{sequence:03d}"
        
        logger.info(f"✅ Created new character: {registration_id} ({bot_name} - {user_name})")
        
        return cls(
            id=registration_id,
            role=role,
            sequence=sequence,
            bot=bot,
            user=user,
            created_at=time.time(),
            last_updated=time.time()
        )
    
    def get_score(self) -> float:
        """
        Hitung score untuk ranking
        
        Formula: (Total Chat × 0.3) + (Level × 0.4) + (Total Climax × 0.3)
        """
        total_chat_score = min(100, self.total_chats) / 100
        level_score = self.level / 12
        climax_score = min(50, self.total_climax_bot + self.total_climax_user) / 50
        
        return (total_chat_score * 0.3) + (level_score * 0.4) + (climax_score * 0.3)
    
    def can_start_intimacy(self) -> tuple:
        """
        Cek apakah bisa memulai intim
        
        Returns:
            (can_start, reason)
        """
        # Level minimal 7
        if self.level < 7:
            return False, f"Level masih {self.level}/7. Butuh level 7 untuk intim."
        
        # Stamina minimal 20%
        if self.stamina_bot < 20:
            return False, f"Stamina bot {self.stamina_bot}% < 20%"
        
        if self.stamina_user < 20:
            return False, f"Stamina user {self.stamina_user}% < 20%"
        
        # Cooldown
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
        
        # Cooldown 3 jam setelah climax
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
        # Kembali ke level 10
        self.level = 10
        self.last_updated = time.time()
    
    def get_progress_to_next_level(self) -> float:
        """
        Hitung progress ke level berikutnya
        
        Returns:
            Progress dalam persen (0-100)
        """
        from config import settings
        
        if self.level <= 10:
            target = settings.level.level_targets.get(self.level + 1, 0)
            if target == 0:
                return 100.0
            current_target = settings.level.level_targets.get(self.level, 0)
            progress = ((self.total_chats - current_target) / (target - current_target)) * 100
            return max(0, min(100, progress))
        else:
            # Level 11-12
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
        """
        Convert ke database model
        
        Returns:
            DBRegistration object
        """
        return DBRegistration(
            id=self.id,
            role=self.role,
            sequence=self.sequence,
            status=self.status,
            created_at=self.created_at,
            last_updated=self.last_updated,
            bot_name=self.bot.name,
            bot_age=self.bot.physical.age,
            bot_height=self.bot.physical.height,
            bot_weight=self.bot.physical.weight,
            bot_chest=self.bot.physical.chest,
            bot_hijab=self.bot.physical.hijab,
            user_name=self.user.name,
            user_status=self.user.relationship.status,
            user_age=self.user.age,
            user_height=self.user.physical.height,
            user_weight=self.user.physical.weight,
            user_penis=self.user.physical.penis,
            user_artist_ref=self.user.artist_ref,
            level=self.level,
            total_chats=self.total_chats,
            total_climax_bot=self.total_climax_bot,
            total_climax_user=self.total_climax_user,
            stamina_bot=self.stamina_bot,
            stamina_user=self.stamina_user,
            in_intimacy_cycle=self.in_intimacy_cycle,
            intimacy_cycle_count=self.intimacy_cycle_count,
            last_climax_time=self.last_climax_time,
            cooldown_until=self.cooldown_until,
            weighted_memory_score=self.weighted_memory_score,
            weighted_memory_data=self.weighted_memory_data,
            emotional_bias=self.emotional_bias,
            secondary_emotion=self.secondary_emotion,
            secondary_arousal=self.secondary_arousal,
            secondary_emotion_reason=self.secondary_emotion_reason,
            physical_sensation=self.physical_sensation,
            physical_hunger=self.physical_hunger,
            physical_thirst=self.physical_thirst,
            physical_temperature=self.physical_temperature,
            metadata=self.metadata
        )
    
    @classmethod
    def from_db_registration(cls, db_reg: DBRegistration) -> 'CharacterRegistration':
        """
        Create from database model
        
        Args:
            db_reg: DBRegistration object dari database
        
        Returns:
            CharacterRegistration object
        """
        from .bot_identity import BotIdentity, BotPhysicalProfile, BotPersonality, BotPersonalityType, BotFamilyRelation
        from .user_identity import UserIdentity, UserPhysicalProfile, UserPersonality, UserRelationship
        
        # =========================================================
        # BUILD BOT IDENTITY
        # =========================================================
        
        physical = BotPhysicalProfile(
            name=db_reg.bot_name,
            age=db_reg.bot_age,
            height=db_reg.bot_height,
            weight=db_reg.bot_weight,
            chest=db_reg.bot_chest,
            hijab=db_reg.bot_hijab
        )
        
        # Default personality
        personality = BotPersonality(
            type=BotPersonalityType.MANIS,
            traits=["manis", "ramah"],
            speaking_style="santai",
            intimacy_style="lembut",
            response_length="sedang"
        )
        
        # Family relation (untuk IPAR)
        family = BotFamilyRelation()
        if db_reg.role == CharacterRole.IPAR:
            family.has_older_sister = True
            family.sister_name = "Nova"
            family.sister_panggilan = "Kak Nova"
            family.lives_with_sister = True
            family.user_is_sister_husband = True
        
        bot = BotIdentity(
            name=db_reg.bot_name,
            role=db_reg.role,
            physical=physical,
            personality=personality,
            family=family
        )
        
        # =========================================================
        # BUILD USER IDENTITY
        # =========================================================
        
        relationship = UserRelationship(
            status=db_reg.user_status,
            spouse_name="Nova" if db_reg.user_status == UserStatus.SUAMI_NOVA else None,
            spouse_location=None,
            spouse_status=None
        )
        
        user_physical = UserPhysicalProfile(
            height=db_reg.user_height,
            weight=db_reg.user_weight,
            penis=db_reg.user_penis
        )
        
        user_personality = UserPersonality()
        
        user = UserIdentity(
            name=db_reg.user_name,
            age=db_reg.user_age,
            relationship=relationship,
            physical=user_physical,
            personality=user_personality,
            artist_ref=db_reg.user_artist_ref
        )
        
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
            in_intimacy_cycle=db_reg.in_intimacy_cycle,
            intimacy_cycle_count=db_reg.intimacy_cycle_count,
            last_climax_time=db_reg.last_climax_time,
            cooldown_until=db_reg.cooldown_until,
            weighted_memory_score=db_reg.weighted_memory_score,
            weighted_memory_data=db_reg.weighted_memory_data,
            emotional_bias=db_reg.emotional_bias,
            secondary_emotion=db_reg.secondary_emotion,
            secondary_arousal=db_reg.secondary_arousal,
            secondary_emotion_reason=db_reg.secondary_emotion_reason,
            physical_sensation=db_reg.physical_sensation,
            physical_hunger=db_reg.physical_hunger,
            physical_thirst=db_reg.physical_thirst,
            physical_temperature=db_reg.physical_temperature,
            created_at=db_reg.created_at,
            last_updated=db_reg.last_updated,
            metadata=db_reg.metadata
        )
    
    def format_status(self) -> str:
        """
        Format status untuk ditampilkan
        
        Returns:
            String status karakter
        """
        status_emoji = {
            CharacterStatus.ACTIVE: "🟢",
            CharacterStatus.CLOSED: "⚪",
            CharacterStatus.ENDED: "🔴"
        }.get(self.status, "⚪")
        
        return (
            f"{status_emoji} **{self.bot.name}** ({self.role.value.upper()})\n"
            f"   👤 User: {self.user.name}\n"
            f"   📊 Level {self.level}/12 | {self.total_chats} chat | {self.total_climax_bot + self.total_climax_user} climax\n"
            f"   🔥 Stamina: {self.stamina_bot}% (bot) / {self.stamina_user}% (user)"
        )
    
    def __repr__(self) -> str:
        return f"CharacterRegistration(id={self.id}, role={self.role.value}, user={self.user.name}, bot={self.bot.name})"


__all__ = [
    'CharacterStatus',
    'CharacterRegistration',
]
