# identity/manager.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
Identity Manager - Multi-Identity System
=============================================================================
"""

import time
import logging
import random
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

from database.repository import Repository
from database.models import CharacterRole, RegistrationStatus
from .registration import CharacterRegistration, CharacterStatus, BotIdentity, UserIdentity

logger = logging.getLogger(__name__)


class IdentityManager:
    """
    Manager untuk multi-identity system
    Mengelola semua registrasi karakter
    """
    
    def __init__(self):
        self.repo = Repository()
        self._current_registration: Optional[CharacterRegistration] = None
        self._active_session: Optional[str] = None
    
    # =========================================================================
    # REGISTRATION MANAGEMENT
    # =========================================================================
    
    async def create_character(
        self,
        role: CharacterRole,
        user_name: Optional[str] = None,
        bot_name: Optional[str] = None
    ) -> CharacterRegistration:
        """
        Buat karakter baru
        
        Args:
            role: Role karakter
            user_name: Nama user (opsional, random jika None)
            bot_name: Nama bot (opsional, random jika None)
        
        Returns:
            CharacterRegistration baru
        """
        # Dapatkan nomor urut berikutnya
        sequence = await self.repo.get_next_sequence(role)
        
        # Buat registrasi
        registration = CharacterRegistration.create_new(
            role=role,
            sequence=sequence,
            user_name=user_name,
            bot_name=bot_name
        )
        
        # Simpan ke database
        db_reg = registration.to_db_registration()
        await self.repo.create_registration(db_reg)
        
        # Inisialisasi state tracker
        from database.models import StateTracker, ClothingState
        state = StateTracker(
            registration_id=registration.id,
            location_bot="ruang tamu",
            location_user="ruang tamu",
            position_bot="duduk",
            position_user="duduk",
            position_relative="bersebelahan",
            clothing_state=ClothingState(),
            emotion_bot="senang",
            arousal_bot=0,
            mood_bot="normal",
            current_time=self._get_initial_time()
        )
        
        # Set initial clothing based on role and time
        await self._init_clothing(state, registration.role)
        
        await self.repo.save_state(state)
        
        logger.info(f"✅ Created new character: {registration.id} ({role.value})")
        
        return registration
    
    async def get_character(self, registration_id: str) -> Optional[CharacterRegistration]:
        """
        Dapatkan karakter berdasarkan ID
        
        Args:
            registration_id: ID registrasi (contoh: IPAR-001)
        
        Returns:
            CharacterRegistration atau None
        """
        db_reg = await self.repo.get_registration(registration_id)
        if not db_reg:
            return None
        
        return CharacterRegistration.from_db_registration(db_reg)
    
    async def get_all_characters(self, role: Optional[CharacterRole] = None) -> List[CharacterRegistration]:
        """
        Dapatkan semua karakter
        
        Args:
            role: Filter role (opsional)
        
        Returns:
            List CharacterRegistration
        """
        db_regs = await self.repo.get_user_registrations(0, role)  # user_id 0 karena admin tunggal
        
        characters = []
        for db_reg in db_regs:
            characters.append(CharacterRegistration.from_db_registration(db_reg))
        
        # Sort by last_updated
        characters.sort(key=lambda x: x.last_updated, reverse=True)
        
        return characters
    
    async def get_active_character(self) -> Optional[CharacterRegistration]:
        """
        Dapatkan karakter yang sedang aktif
        
        Returns:
            CharacterRegistration atau None
        """
        if self._current_registration:
            # Load latest state
            return await self.get_character(self._current_registration.id)
        return None
    
    async def switch_character(self, registration_id: str) -> Optional[CharacterRegistration]:
        """
        Switch ke karakter lain
        
        Args:
            registration_id: ID registrasi
        
        Returns:
            CharacterRegistration atau None
        """
        character = await self.get_character(registration_id)
        if not character:
            logger.warning(f"Character not found: {registration_id}")
            return None
        
        # Close current session if any
        if self._current_registration:
            await self.close_current_session()
        
        self._current_registration = character
        self._active_session = character.id
        
        logger.info(f"🔄 Switched to character: {character.id}")
        
        return character
    
    async def close_current_session(self):
        """Tutup session saat ini (simpan state)"""
        if self._current_registration:
            # Update status ke closed
            self._current_registration.status = CharacterStatus.CLOSED
            self._current_registration.last_updated = time.time()
            
            # Save to database
            db_reg = self._current_registration.to_db_registration()
            await self.repo.update_registration(db_reg)
            
            logger.info(f"📁 Closed session: {self._current_registration.id}")
            
            self._current_registration = None
            self._active_session = None
    
    async def end_character(self, registration_id: str) -> bool:
        """
        Akhiri karakter (hapus permanen)
        
        Args:
            registration_id: ID registrasi
        
        Returns:
            True jika berhasil
        """
        character = await self.get_character(registration_id)
        if not character:
            return False
        
        # If this is the active character, close session first
        if self._active_session == registration_id:
            await self.close_current_session()
        
        # Delete from database
        await self.repo.delete_registration(registration_id)
        
        logger.info(f"💔 Ended character: {registration_id}")
        
        return True
    
    # =========================================================================
    # RANKING & RETENTION
    # =========================================================================
    
    async def get_top_characters(self, role: CharacterRole, limit: int = 10) -> List[CharacterRegistration]:
        """
        Dapatkan top karakter berdasarkan score
        
        Args:
            role: Role karakter
            limit: Jumlah maksimal
        
        Returns:
            List CharacterRegistration
        """
        characters = await self.get_all_characters(role)
        
        # Hitung score
        scored = [(c, c.get_score()) for c in characters]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return [c for c, _ in scored[:limit]]
    
    async def cleanup_old_characters(self):
        """
        Bersihkan karakter lama (simpan top 10 per role)
        """
        for role in CharacterRole:
            top = await self.get_top_characters(role, 10)
            top_ids = [c.id for c in top]
            
            all_chars = await self.get_all_characters(role)
            for char in all_chars:
                if char.id not in top_ids and char.status != CharacterStatus.ACTIVE:
                    await self.end_character(char.id)
        
        logger.info("🧹 Cleaned up old characters")
    
    # =========================================================================
    # STATE MANAGEMENT
    # =========================================================================
    
    async def get_character_state(self, registration_id: str) -> Optional[Dict]:
        """
        Dapatkan state tracker untuk karakter
        
        Args:
            registration_id: ID registrasi
        
        Returns:
            State data atau None
        """
        from database.models import StateTracker
        state = await self.repo.load_state(registration_id)
        
        if not state:
            return None
        
        return {
            'location_bot': state.location_bot,
            'location_user': state.location_user,
            'position_bot': state.position_bot,
            'position_user': state.position_user,
            'position_relative': state.position_relative,
            'clothing': state.clothing_state.to_dict(),
            'emotion_bot': state.emotion_bot,
            'arousal_bot': state.arousal_bot,
            'mood_bot': state.mood_bot.value,
            'family_status': state.family_status.value if state.family_status else None,
            'family_location': state.family_location.value if state.family_location else None,
            'current_time': state.current_time,
            'updated_at': state.updated_at
        }
    
    async def update_character_state(self, registration_id: str, updates: Dict):
        """
        Update state tracker untuk karakter
        
        Args:
            registration_id: ID registrasi
            updates: Dictionary updates
        """
        from database.models import StateTracker, ClothingState
        
        current = await self.repo.load_state(registration_id)
        
        if not current:
            # Create new state
            current = StateTracker(registration_id=registration_id)
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(current, key):
                setattr(current, key, value)
        
        # Update clothing if provided
        if 'clothing' in updates:
            clothing_data = updates['clothing']
            if isinstance(clothing_data, dict):
                for k, v in clothing_data.items():
                    if hasattr(current.clothing_state, k):
                        setattr(current.clothing_state, k, v)
        
        current.updated_at = time.time()
        
        await self.repo.save_state(current)
    
    async def update_family_status(
        self,
        registration_id: str,
        status: str,
        location: Optional[str] = None,
        activity: Optional[str] = None
    ):
        """
        Update status keluarga (istri/kakak)
        
        Args:
            registration_id: ID registrasi
            status: Status ("ada", "tidak_ada", "tidur")
            location: Lokasi (opsional)
            activity: Aktivitas (opsional)
        """
        from database.models import FamilyStatus, FamilyLocation
        
        updates = {
            'family_status': FamilyStatus(status) if status else None,
            'family_activity': activity
        }
        
        if location:
            updates['family_location'] = FamilyLocation(location)
        
        await self.update_character_state(registration_id, updates)
    
    async def update_clothing(
        self,
        registration_id: str,
        layer: str,
        item: Optional[str] = None,
        remove: bool = False,
        reason: str = ""
    ):
        """
        Update pakaian karakter
        
        Args:
            registration_id: ID registrasi
            layer: Lapisan pakaian ("outer_top", "outer_bottom", "inner_top", "inner_bottom")
            item: Nama pakaian (opsional)
            remove: True untuk melepas, False untuk memakai
            reason: Alasan perubahan
        """
        state = await self.repo.load_state(registration_id)
        if not state:
            return
        
        if remove:
            if layer == "outer_top":
                state.clothing_state.remove_outer_top(reason)
            elif layer == "outer_bottom":
                state.clothing_state.remove_outer_bottom(reason)
            elif layer == "inner_top":
                state.clothing_state.remove_inner_top(reason)
            elif layer == "inner_bottom":
                state.clothing_state.remove_inner_bottom(reason)
        else:
            # Memakai pakaian
            if layer == "outer_top":
                state.clothing_state.bot_outer_top = item
                state.clothing_state.bot_outer_top_on = True
            elif layer == "outer_bottom":
                state.clothing_state.bot_outer_bottom = item
                state.clothing_state.bot_outer_bottom_on = True
            elif layer == "inner_top":
                state.clothing_state.bot_inner_top = item
                state.clothing_state.bot_inner_top_on = True
            elif layer == "inner_bottom":
                state.clothing_state.bot_inner_bottom = item
                state.clothing_state.bot_inner_bottom_on = True
        
        state.updated_at = time.time()
        await self.repo.save_state(state)
    
    # =========================================================================
    # MEMORY MANAGEMENT
    # =========================================================================
    
    async def add_to_memory(
        self,
        registration_id: str,
        user_message: str,
        bot_response: str,
        context: Dict
    ):
        """
        Tambah interaksi ke memory
        
        Args:
            registration_id: ID registrasi
            user_message: Pesan user
            bot_response: Respons bot
            context: Konteks saat itu
        """
        from database.models import WorkingMemoryItem
        
        # Dapatkan chat index terakhir
        last_index = await self.repo.get_last_chat_index(registration_id)
        new_index = last_index + 1
        
        # Tambah ke working memory
        item = WorkingMemoryItem(
            registration_id=registration_id,
            chat_index=new_index,
            user_message=user_message[:500],
            bot_response=bot_response[:500],
            context=context
        )
        
        await self.repo.add_to_working_memory(item)
        
        # Cleanup old working memory (keep 1000)
        await self.repo.cleanup_old_working_memory(registration_id, keep=1000)
        
        # Update registration total chats
        character = await self.get_character(registration_id)
        if character:
            character.total_chats += 1
            character.last_updated = time.time()
            await self.repo.update_registration(character.to_db_registration())
    
    async def get_memory_context(self, registration_id: str, limit: int = 50) -> str:
        """
        Dapatkan konteks memory untuk prompt
        
        Args:
            registration_id: ID registrasi
            limit: Jumlah chat terakhir
        
        Returns:
            String konteks memory
        """
        memories = await self.repo.get_working_memory(registration_id, limit)
        
        if not memories:
            return "Belum ada percakapan."
        
        lines = ["📜 PERCAKAPAN TERAKHIR:"]
        for m in memories:
            lines.append(f"• [{self._format_time(m['timestamp'])}] User: {m['user'][:100]}")
            lines.append(f"  Bot: {m['bot'][:100]}")
        
        return "\n".join(lines)
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def _get_initial_time(self) -> str:
        """Dapatkan waktu awal random"""
        times = ["pagi", "siang", "sore", "malam"]
        hours = {
            "pagi": "08:00",
            "siang": "13:00",
            "sore": "17:00",
            "malam": "21:00"
        }
        time_of_day = random.choice(times)
        return hours[time_of_day]
    
    def _format_time(self, timestamp: float) -> str:
        """Format timestamp ke string waktu"""
        return datetime.fromtimestamp(timestamp).strftime("%H:%M")
    
    async def _init_clothing(self, state, role: CharacterRole):
        """Inisialisasi pakaian awal berdasarkan role"""
        from database.models import ClothingState
        
        # Pakaian bot
        if role == CharacterRole.IPAR:
            state.clothing_state.bot_outer_top = "daster rumah motif bunga"
            state.clothing_state.bot_outer_bottom = None
            state.clothing_state.bot_inner_top = "bra"
            state.clothing_state.bot_inner_bottom = "celana dalam"
        elif role == CharacterRole.TEMAN_KANTOR:
            state.clothing_state.bot_outer_top = "kemeja putih"
            state.clothing_state.bot_outer_bottom = "rok hitam"
            state.clothing_state.bot_inner_top = "bra"
            state.clothing_state.bot_inner_bottom = "celana dalam"
        elif role == CharacterRole.JANDA:
            state.clothing_state.bot_outer_top = "daster tipis"
            state.clothing_state.bot_outer_bottom = None
            state.clothing_state.bot_inner_top = "bra"
            state.clothing_state.bot_inner_bottom = "celana dalam"
        else:
            state.clothing_state.bot_outer_top = "kaos"
            state.clothing_state.bot_outer_bottom = "celana jeans"
            state.clothing_state.bot_inner_top = "bra"
            state.clothing_state.bot_inner_bottom = "celana dalam"
        
        # Pakaian user
        state.clothing_state.user_outer_top = "kaos"
        state.clothing_state.user_outer_bottom = "celana jeans"
        state.clothing_state.user_inner_bottom = "celana dalam"
        
        state.updated_at = time.time()
    
    async def get_registration_stats(self) -> Dict:
        """
        Dapatkan statistik registrasi
        
        Returns:
            Dictionary statistik
        """
        characters = await self.get_all_characters()
        
        total = len(characters)
        by_role = {}
        active = 0
        total_chats = 0
        total_climax = 0
        
        for c in characters:
            role_name = c.role.value
            by_role[role_name] = by_role.get(role_name, 0) + 1
            if c.status == CharacterStatus.ACTIVE:
                active += 1
            total_chats += c.total_chats
            total_climax += c.total_climax_bot + c.total_climax_user
        
        return {
            "total_characters": total,
            "active_characters": active,
            "by_role": by_role,
            "total_chats_all_time": total_chats,
            "total_climax_all_time": total_climax,
            "top_character": max(characters, key=lambda x: x.get_score()) if characters else None
        }


__all__ = ['IdentityManager']
