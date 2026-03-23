# references/areas.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
Areas Reference - Database Referensi Area Sensitif (Bukan Template)
=============================================================================
"""

import random
import logging
from typing import Dict, List, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)


class AreaCategory(str, Enum):
    HEAD = "head"
    NECK = "neck"
    CHEST = "chest"
    BACK = "back"
    ARMS = "arms"
    STOMACH = "stomach"
    HIPS = "hips"
    LEGS = "legs"
    FEET = "feet"
    SPECIAL = "special"


class AreaDatabase:
    """Database area sensitif sebagai referensi"""
    
    def __init__(self):
        self.head_areas = [
            {"id": "head_forehead", "name": "Dahi", "sensitivity": 5, "notes": "Ciuman di dahi romantis"},
            {"id": "head_temple", "name": "Pelipis", "sensitivity": 6, "notes": "Ciuman ringan menenangkan"},
            {"id": "head_earlobe", "name": "Daun Telinga", "sensitivity": 8, "notes": "Bisikan atau ciuman"},
            {"id": "head_behind_ear", "name": "Belakang Telinga", "sensitivity": 9, "notes": "Sangat sensitif"},
            {"id": "head_cheek", "name": "Pipi", "sensitivity": 4, "notes": "Ciuman manis"},
            {"id": "head_lips", "name": "Bibir", "sensitivity": 9, "notes": "Ciuman, gigitan ringan"},
        ]
        
        self.neck_areas = [
            {"id": "neck_front", "name": "Leher Depan", "sensitivity": 7, "notes": "Ciuman ringan"},
            {"id": "neck_side", "name": "Leher Samping", "sensitivity": 8, "notes": "Sangat sensitif"},
            {"id": "neck_back", "name": "Leher Belakang", "sensitivity": 7, "notes": "Elusan ringan"},
            {"id": "neck_collarbone", "name": "Tulang Selangka", "sensitivity": 6, "notes": "Ciuman ringan"},
            {"id": "neck_dimple", "name": "Lekuk Leher", "sensitivity": 9, "notes": "Sweet spot"},
        ]
        
        self.chest_areas = [
            {"id": "chest_upper", "name": "Dada Atas", "sensitivity": 5, "notes": "Elusan ringan"},
            {"id": "nipple_left", "name": "Puting Kiri", "sensitivity": 9, "notes": "Sangat sensitif"},
            {"id": "nipple_right", "name": "Puting Kanan", "sensitivity": 9, "notes": "Sangat sensitif"},
            {"id": "areola_left", "name": "Areola Kiri", "sensitivity": 8, "notes": "Bisa dijilat"},
        ]
        
        self.back_areas = [
            {"id": "back_upper", "name": "Punggung Atas", "sensitivity": 5, "notes": "Elusan atau pijatan"},
            {"id": "back_middle", "name": "Punggung Tengah", "sensitivity": 5, "notes": "Area luas"},
            {"id": "back_lower", "name": "Punggung Bawah", "sensitivity": 6, "notes": "Dekat pinggang"},
            {"id": "spine", "name": "Tulang Belakang", "sensitivity": 7, "notes": "Elusan dari atas ke bawah"},
        ]
        
        self.arms_areas = [
            {"id": "shoulder_left", "name": "Bahu Kiri", "sensitivity": 5, "notes": "Pijatan"},
            {"id": "armpit_left", "name": "Ketiak Kiri", "sensitivity": 7, "notes": "Sensitif, geli"},
            {"id": "wrist_left", "name": "Pergelangan Kiri", "sensitivity": 6, "notes": "Area sensitif, nadi"},
        ]
        
        self.stomach_areas = [
            {"id": "stomach_upper", "name": "Perut Atas", "sensitivity": 5, "notes": "Elusan"},
            {"id": "stomach_lower", "name": "Perut Bawah", "sensitivity": 7, "notes": "Dekat area intim"},
            {"id": "belly_button", "name": "Pusar", "sensitivity": 8, "notes": "Sangat sensitif"},
            {"id": "side_waist_left", "name": "Samping Pinggang Kiri", "sensitivity": 7, "notes": "Area geli"},
        ]
        
        self.hips_areas = [
            {"id": "hip_bone_left", "name": "Tulang Pinggul Kiri", "sensitivity": 6, "notes": "Area menonjol"},
            {"id": "buttock_upper_left", "name": "Bokong Atas Kiri", "sensitivity": 7, "notes": "Area sensitif"},
        ]
        
        self.legs_areas = [
            {"id": "thigh_front_left", "name": "Paha Depan Kiri", "sensitivity": 6, "notes": "Elusan"},
            {"id": "thigh_inner_left", "name": "Paha Dalam Kiri", "sensitivity": 8, "notes": "Sangat sensitif"},
            {"id": "knee_left", "name": "Lutut Kiri", "sensitivity": 3, "notes": "Kurang sensitif"},
            {"id": "calf_left", "name": "Betis Kiri", "sensitivity": 4, "notes": "Elusan atau pijatan"},
            {"id": "ankle_left", "name": "Pergelangan Kaki Kiri", "sensitivity": 5, "notes": "Elusan"},
        ]
        
        self.feet_areas = [
            {"id": "foot_sole_left", "name": "Telapak Kaki Kiri", "sensitivity": 6, "notes": "Sensitif, geli"},
            {"id": "toes_left", "name": "Jari Kaki Kiri", "sensitivity": 5, "notes": "Beberapa orang sensitif"},
        ]
        
        self.special_areas = [
            {"id": "special_ear", "name": "Ear Kissing", "sensitivity": 9, "notes": "Untuk foreplay"},
            {"id": "special_neck", "name": "Neck Biting", "sensitivity": 8, "notes": "Bisa meninggalkan bekas"},
            {"id": "special_spine", "name": "Spine Tracing", "sensitivity": 7, "notes": "Dengan ujung jari"},
            {"id": "special_inner_thigh", "name": "Inner Thigh Kiss", "sensitivity": 9, "notes": "Membangun gairah"},
        ]
        
        self.all_areas = (
            self.head_areas + self.neck_areas + self.chest_areas +
            self.back_areas + self.arms_areas + self.stomach_areas +
            self.hips_areas + self.legs_areas + self.feet_areas +
            self.special_areas
        )
        
        logger.info(f"✅ AreaDatabase initialized: {len(self.all_areas)} areas")
    
    def get_all_areas(self) -> List[Dict]:
        return self.all_areas
    
    def get_random_area(self) -> Dict:
        return random.choice(self.all_areas)
    
    def get_areas_by_sensitivity(self, min_sensitivity: int = 7, max_sensitivity: int = 10) -> List[Dict]:
        return [a for a in self.all_areas if min_sensitivity <= a['sensitivity'] <= max_sensitivity]
    
    def get_areas_by_category(self, category: AreaCategory) -> List[Dict]:
        categories = {
            AreaCategory.HEAD: self.head_areas,
            AreaCategory.NECK: self.neck_areas,
            AreaCategory.CHEST: self.chest_areas,
            AreaCategory.BACK: self.back_areas,
            AreaCategory.ARMS: self.arms_areas,
            AreaCategory.STOMACH: self.stomach_areas,
            AreaCategory.HIPS: self.hips_areas,
            AreaCategory.LEGS: self.legs_areas,
            AreaCategory.FEET: self.feet_areas,
            AreaCategory.SPECIAL: self.special_areas,
        }
        return categories.get(category, [])


_area_db = None


def get_area_database() -> AreaDatabase:
    global _area_db
    if _area_db is None:
        _area_db = AreaDatabase()
    return _area_db


__all__ = ['AreaDatabase', 'AreaCategory', 'get_area_database']
