# public/thrill.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Thrill Calculator for Public Areas
Compatible with AMORIA's emotional flow and arousal system
=============================================================================
"""

import logging
import random
from typing import Dict

logger = logging.getLogger(__name__)


class ThrillSystem:
    """Kalkulator thrill untuk lokasi public AMORIA"""
    
    def __init__(self):
        self.thrill_levels = {
            'very_low': ("😐 Biasa aja", "Gak ada sensasi khusus.", 0),
            'low': ("😊 Sedikit deg-degan", "Mulai terasa getaran seru.", 5),
            'medium': ("😍 Jantung berdebar!", "Seru! Deg-degan mulai terasa.", 10),
            'high': ("🥵 Deg-degan banget!", "Aduh aduh, jantung mau copot!", 15),
            'very_high': ("💥 WAH! Gila!", "Deg-degan gila! Tapi seru banget!", 20)
        }
        logger.info("✅ ThrillSystem initialized for AMORIA")
    
    async def calculate_thrill(self, base_thrill: int, risk_level: int, 
                               intimacy_level: int, location_category: str,
                               arousal: int = 0, is_intimacy_cycle: bool = False) -> Dict:
        """
        Hitung thrill dengan mempertimbangkan level AMORIA dan arousal
        
        Args:
            base_thrill: Thrill dasar lokasi
            risk_level: Level risiko (0-100)
            intimacy_level: Level AMORIA (1-12)
            location_category: Kategori lokasi
            arousal: Arousal saat ini (0-100)
            is_intimacy_cycle: Apakah dalam siklus intim
        """
        thrill = base_thrill
        
        # Pengaruh risiko
        thrill += risk_level * 0.3
        
        # Pengaruh level (semakin tinggi level, semakin menikmati)
        thrill += (intimacy_level - 1) * 3
        
        # Pengaruh arousal (arousal tinggi = lebih sensitif)
        thrill += int(arousal / 10)
        
        # Pengaruh kategori lokasi
        category_boost = {
            'extreme': 10,
            'urban': 8,
            'transport': 5,
            'nature': 3,
            'safe': 0
        }
        thrill += category_boost.get(location_category, 0)
        
        # Pengaruh intimacy cycle
        if is_intimacy_cycle:
            thrill += 15
        
        # Random factor
        thrill += random.randint(-5, 10)
        thrill = max(0, min(100, thrill))
        
        thrill_level = self._get_thrill_level(thrill)
        level_name, description, arousal_boost = self.thrill_levels[thrill_level]
        
        return {
            'base_thrill': base_thrill,
            'final_thrill': thrill,
            'thrill_level': thrill_level,
            'level_name': level_name,
            'description': description,
            'arousal_boost': arousal_boost,
            'modifiers': {
                'risk_contribution': int(risk_level * 0.3),
                'level_contribution': (intimacy_level - 1) * 3,
                'arousal_contribution': int(arousal / 10),
                'category_boost': category_boost.get(location_category, 0),
                'intimacy_cycle_boost': 15 if is_intimacy_cycle else 0,
                'random': thrill - base_thrill - int(risk_level * 0.3) - ((intimacy_level - 1) * 3) - int(arousal / 10) - category_boost.get(location_category, 0) - (15 if is_intimacy_cycle else 0)
            }
        }
    
    def _get_thrill_level(self, thrill: int) -> str:
        if thrill >= 80:
            return 'very_high'
        elif thrill >= 60:
            return 'high'
        elif thrill >= 40:
            return 'medium'
        elif thrill >= 20:
            return 'low'
        return 'very_low'
    
    def format_thrill_report(self, thrill_data: Dict) -> str:
        thrill = thrill_data['final_thrill']
        bar_length = 15
        filled = int(thrill / 100 * bar_length)
        bar = "🎢" * filled + "⚪" * (bar_length - filled)
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║                     🎢 THRILL ASSESSMENT 🎢                       ║
╠══════════════════════════════════════════════════════════════════╣
║ {thrill_data['level_name']:<64} ║
║ {bar}                                                             ║
║                                                                  ║
║ 📝 {thrill_data['description']:<64} ║
║                                                                  ║
║ 🔥 Score: {thrill:.0f}% | Arousal Boost: +{thrill_data['arousal_boost']}     ║
╚══════════════════════════════════════════════════════════════════╝
"""


__all__ = ['ThrillSystem']
