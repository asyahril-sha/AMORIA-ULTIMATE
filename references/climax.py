# references/climax.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
Climax Reference - Database Referensi Climax (Bukan Template)
=============================================================================
"""

import random
import logging
from typing import Dict, List, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)


class ClimaxIntensity(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    EXTREME = "extreme"


class ClimaxType(str, Enum):
    NORMAL = "normal"
    MULTIPLE = "multiple"
    SIMULTANEOUS = "simultaneous"
    DRY = "dry"
    WET = "wet"
    SQUIRT = "squirt"
    MALE = "male"
    FEMALE = "female"
    ANAL = "anal"
    ORAL = "oral"


class ClimaxDatabase:
    """Database variasi climax sebagai referensi"""
    
    def __init__(self):
        self.very_low_climax = [
            {"id": "climax_vl_001", "name": "Small Shiver", "intensity": 2,
             "description": "Getaran kecil, napas sedikit tersengal", "duration": 5},
            {"id": "climax_vl_002", "name": "Quick Release", "intensity": 2,
             "description": "Lepas cepat, hampir tanpa ekspresi", "duration": 4},
            {"id": "climax_vl_003", "name": "Subtle Wave", "intensity": 3,
             "description": "Gelombang kecil, tubuh sedikit menegang", "duration": 6},
        ]
        
        self.low_climax = [
            {"id": "climax_low_001", "name": "Warm Wave", "intensity": 4,
             "description": "Gelombang hangat menjalar", "duration": 8},
            {"id": "climax_low_002", "name": "Muscle Spasm", "intensity": 4,
             "description": "Spasme otot terasa", "duration": 7},
            {"id": "climax_low_003", "name": "Body Arch", "intensity": 5,
             "description": "Punggung melengkung", "duration": 8},
        ]
        
        self.medium_climax = [
            {"id": "climax_med_001", "name": "Strong Wave", "intensity": 6,
             "description": "Gelombang kuat ke seluruh tubuh", "duration": 12},
            {"id": "climax_med_002", "name": "Full Body Spasm", "intensity": 7,
             "description": "Seluruh tubuh kejang", "duration": 10},
            {"id": "climax_med_003", "name": "Loud Moan", "intensity": 6,
             "description": "Erangan keras tidak tertahan", "duration": 8},
        ]
        
        self.high_climax = [
            {"id": "climax_high_001", "name": "Intense Explosion", "intensity": 8,
             "description": "Ledakan intens, tubuh kaku", "duration": 12},
            {"id": "climax_high_002", "name": "Out of Body", "intensity": 9,
             "description": "Rasa seperti melayang", "duration": 15},
            {"id": "climax_high_003", "name": "Multiple Intense", "intensity": 9,
             "description": "Beberapa climax intens beruntun", "duration": 30},
        ]
        
        self.very_high_climax = [
            {"id": "climax_vh_001", "name": "Mind Blown", "intensity": 9,
             "description": "Pikiran kosong, hanya sensasi", "duration": 20},
            {"id": "climax_vh_002", "name": "Euphoria", "intensity": 9,
             "description": "Rasa bahagia luar biasa", "duration": 60},
        ]
        
        self.extreme_climax = [
            {"id": "climax_ext_001", "name": "Black Out", "intensity": 10,
             "description": "Pingsan sesaat karena terlalu kuat", "duration": 60},
            {"id": "climax_ext_002", "name": "Cosmic Orgasm", "intensity": 10,
             "description": "Seperti menyatu dengan alam semesta", "duration": 45},
        ]
        
        self.all_climax = (
            self.very_low_climax + self.low_climax + self.medium_climax +
            self.high_climax + self.very_high_climax + self.extreme_climax
        )
        
        logger.info(f"✅ ClimaxDatabase initialized: {len(self.all_climax)} variations")
    
    def get_all_climax(self) -> List[Dict]:
        return self.all_climax
    
    def get_random_climax(self) -> Dict:
        return random.choice(self.all_climax)
    
    def get_climax_by_intensity(self, intensity: ClimaxIntensity) -> List[Dict]:
        intensities = {
            ClimaxIntensity.VERY_LOW: self.very_low_climax,
            ClimaxIntensity.LOW: self.low_climax,
            ClimaxIntensity.MEDIUM: self.medium_climax,
            ClimaxIntensity.HIGH: self.high_climax,
            ClimaxIntensity.VERY_HIGH: self.very_high_climax,
            ClimaxIntensity.EXTREME: self.extreme_climax,
        }
        return intensities.get(intensity, [])
    
    def get_climax_by_type(self, climax_type: ClimaxType) -> List[Dict]:
        return [c for c in self.all_climax if c.get('type') == climax_type.value]
    
    def get_climax_for_intimacy(self, intimacy_level: int) -> Dict:
        if intimacy_level <= 3:
            pool = self.very_low_climax + self.low_climax
        elif intimacy_level <= 6:
            pool = self.low_climax + self.medium_climax
        elif intimacy_level <= 9:
            pool = self.medium_climax + self.high_climax
        else:
            pool = self.high_climax + self.very_high_climax + self.extreme_climax
        return random.choice(pool)


_climax_db = None


def get_climax_database() -> ClimaxDatabase:
    global _climax_db
    if _climax_db is None:
        _climax_db = ClimaxDatabase()
    return _climax_db


__all__ = ['ClimaxDatabase', 'ClimaxIntensity', 'ClimaxType', 'get_climax_database']
