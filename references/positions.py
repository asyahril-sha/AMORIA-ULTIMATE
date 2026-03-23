# references/positions.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
Positions Reference - Database Referensi Posisi (Bukan Template)
=============================================================================
"""

import random
import logging
from typing import Dict, List, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class IntensityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class PositionDatabase:
    """Database 50+ posisi sex sebagai referensi"""
    
    def __init__(self):
        self.missionary_positions = [
            {"id": "missionary_classic", "name": "Missionary Classic", "category": "missionary",
             "difficulty": DifficultyLevel.EASY, "intensity": IntensityLevel.MEDIUM,
             "description": "Posisi klasik dengan pasangan di bawah", "tags": ["romantic", "classic"]},
            {"id": "missionary_legs_up", "name": "Legs Up Missionary", "category": "missionary",
             "difficulty": DifficultyLevel.MEDIUM, "intensity": IntensityLevel.HIGH,
             "description": "Kaki diangkat ke atas", "tags": ["deep", "intense"]},
            {"id": "missionary_pillow", "name": "Pillow Under Hips", "category": "missionary",
             "difficulty": DifficultyLevel.EASY, "intensity": IntensityLevel.HIGH,
             "description": "Bantal di bawah pinggul", "tags": ["comfortable", "deep"]},
        ]
        
        self.doggy_positions = [
            {"id": "doggy_classic", "name": "Classic Doggy", "category": "doggy",
             "difficulty": DifficultyLevel.EASY, "intensity": IntensityLevel.HIGH,
             "description": "Posisi dari belakang", "tags": ["intense", "deep"]},
            {"id": "doggy_arched", "name": "Arched Doggy", "category": "doggy",
             "difficulty": DifficultyLevel.HARD, "intensity": IntensityLevel.EXTREME,
             "description": "Punggung melengkung", "tags": ["deep", "extreme"]},
        ]
        
        self.woman_top_positions = [
            {"id": "cowgirl_classic", "name": "Classic Cowgirl", "category": "woman_top",
             "difficulty": DifficultyLevel.MEDIUM, "intensity": IntensityLevel.MEDIUM,
             "description": "Wanita di atas, menghadap pasangan", "tags": ["dominant", "intimate"]},
            {"id": "reverse_cowgirl", "name": "Reverse Cowgirl", "category": "woman_top",
             "difficulty": DifficultyLevel.HARD, "intensity": IntensityLevel.HIGH,
             "description": "Wanita di atas, membelakangi pasangan", "tags": ["dominant", "exciting"]},
        ]
        
        self.sitting_positions = [
            {"id": "lap_dance", "name": "Lap Dance", "category": "sitting",
             "difficulty": DifficultyLevel.MEDIUM, "intensity": IntensityLevel.MEDIUM,
             "description": "Wanita duduk di pangkuan", "tags": ["intimate", "romantic"]},
            {"id": "lotus", "name": "Lotus", "category": "sitting",
             "difficulty": DifficultyLevel.HARD, "intensity": IntensityLevel.MEDIUM,
             "description": "Kaki saling melingkar", "tags": ["yoga", "spiritual"]},
        ]
        
        self.standing_positions = [
            {"id": "standing_doggy", "name": "Standing Doggy", "category": "standing",
             "difficulty": DifficultyLevel.MEDIUM, "intensity": IntensityLevel.HIGH,
             "description": "Berdiri, pasangan membungkuk", "tags": ["quick", "intense"]},
            {"id": "wall_position", "name": "Wall Position", "category": "standing",
             "difficulty": DifficultyLevel.EASY, "intensity": IntensityLevel.HIGH,
             "description": "Wanita bersandar di dinding", "tags": ["quick", "wall"]},
        ]
        
        self.side_positions = [
            {"id": "spooning", "name": "Spooning", "category": "side",
             "difficulty": DifficultyLevel.EASY, "intensity": IntensityLevel.LOW,
             "description": "Berbaring miring, seperti sendok", "tags": ["cuddly", "intimate"]},
        ]
        
        self.oral_positions = [
            {"id": "oral_kneeling", "name": "Kneeling Oral", "category": "oral",
             "difficulty": DifficultyLevel.EASY, "intensity": IntensityLevel.MEDIUM,
             "description": "Berlutut di depan pasangan", "tags": ["oral", "submissive"]},
            {"id": "oral_69", "name": "69", "category": "oral",
             "difficulty": DifficultyLevel.MEDIUM, "intensity": IntensityLevel.HIGH,
             "description": "Saling memuaskan secara bersamaan", "tags": ["oral", "mutual"]},
        ]
        
        self.all_positions = (
            self.missionary_positions +
            self.doggy_positions +
            self.woman_top_positions +
            self.sitting_positions +
            self.standing_positions +
            self.side_positions +
            self.oral_positions
        )
        
        logger.info(f"✅ PositionDatabase initialized: {len(self.all_positions)} positions")
    
    def get_all_positions(self) -> List[Dict]:
        return self.all_positions
    
    def get_random_position(self) -> Dict:
        return random.choice(self.all_positions)
    
    def get_positions_by_intensity(self, intensity: IntensityLevel) -> List[Dict]:
        return [p for p in self.all_positions if p['intensity'] == intensity]
    
    def get_positions_by_difficulty(self, difficulty: DifficultyLevel) -> List[Dict]:
        return [p for p in self.all_positions if p['difficulty'] == difficulty]
    
    def get_positions_by_tag(self, tag: str) -> List[Dict]:
        return [p for p in self.all_positions if tag in p.get('tags', [])]


_position_db = None


def get_position_database() -> PositionDatabase:
    global _position_db
    if _position_db is None:
        _position_db = PositionDatabase()
    return _position_db


__all__ = ['PositionDatabase', 'get_position_database', 'DifficultyLevel', 'IntensityLevel']
