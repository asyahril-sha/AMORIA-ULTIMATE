# public/risk.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Risk Calculator for Public Areas
Compatible with AMORIA's leveling and emotional flow
=============================================================================
"""

import logging
import random
from typing import Dict

logger = logging.getLogger(__name__)


class RiskCalculator:
    """Kalkulator risiko untuk lokasi public AMORIA"""
    
    def __init__(self):
        self.risk_levels = {
            'very_low': (0, 20),
            'low': (21, 40),
            'medium': (41, 60),
            'high': (61, 80),
            'very_high': (81, 100)
        }
        
        # Efek risiko ke emotional flow AMORIA
        self.emotional_effects = {
            'very_low': {'arousal_boost': 5, 'mood': 'relaxed'},
            'low': {'arousal_boost': 10, 'mood': 'excited'},
            'medium': {'arousal_boost': 15, 'mood': 'thrilled'},
            'high': {'arousal_boost': 20, 'mood': 'anxious'},
            'very_high': {'arousal_boost': 25, 'mood': 'terrified'}
        }
        
        logger.info("✅ RiskCalculator initialized for AMORIA")
    
    async def calculate_risk(self, base_risk: int, intimacy_level: int = 1, 
                             arousal: int = 0, is_intimacy_cycle: bool = False) -> Dict:
        """
        Hitung risiko dengan mempertimbangkan level AMORIA
        
        Args:
            base_risk: Risiko dasar lokasi
            intimacy_level: Level AMORIA (1-12)
            arousal: Arousal saat ini (0-100)
            is_intimacy_cycle: Apakah dalam siklus intim
        """
        final_risk = base_risk
        
        # Pengaruh level (semakin tinggi level, semakin paham risiko)
        final_risk -= (intimacy_level - 1) * 2
        
        # Pengaruh arousal (arousal tinggi = kurang waspada)
        final_risk += int(arousal / 20)
        
        # Pengaruh intimacy cycle
        if is_intimacy_cycle:
            final_risk += 10
        
        # Random factor
        final_risk += random.randint(-10, 10)
        final_risk = max(0, min(100, final_risk))
        
        risk_level = self._get_risk_level(final_risk)
        emotional_effect = self.emotional_effects[risk_level]
        
        return {
            'base_risk': base_risk,
            'final_risk': final_risk,
            'risk_level': risk_level,
            'description': self._get_risk_description(risk_level),
            'emotional_effect': emotional_effect,
            'modifiers': {
                'level_bonus': (intimacy_level - 1) * 2,
                'arousal_penalty': int(arousal / 20),
                'intimacy_cycle': 10 if is_intimacy_cycle else 0,
                'random': final_risk - base_risk + ((intimacy_level - 1) * 2) - int(arousal / 20) - (10 if is_intimacy_cycle else 0)
            }
        }
    
    def _get_risk_level(self, risk: int) -> str:
        for level, (low, high) in self.risk_levels.items():
            if low <= risk <= high:
                return level
        return 'medium'
    
    def _get_risk_description(self, level: str) -> str:
        desc = {
            'very_low': "Aman banget! Hampir pasti tidak ketahuan. Nikmati momen tanpa khawatir.",
            'low': "Cukup aman, asal hati-hati. Tetap waspada dengan sekitar.",
            'medium': "Risiko sedang. Waspada dengan sekitar, jangan terlalu lama.",
            'high': "Risiko tinggi! Harus ekstra hati-hati. Cepat selesaikan.",
            'very_high': "Sangat berisiko! Siap-siap lari kalau ketahuan. Cuma untuk yang berani."
        }
        return desc.get(level, "Risiko sedang.")
    
    def format_risk_report(self, risk_data: Dict, location_name: str) -> str:
        risk = risk_data['final_risk']
        level = risk_data['risk_level'].upper()
        
        bar_length = 15
        filled = int(risk / 100 * bar_length)
        bar = "⚠️" * filled + "⚪" * (bar_length - filled)
        
        effect = risk_data['emotional_effect']
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║                     ⚠️ RISK ASSESSMENT ⚠️                         ║
╠══════════════════════════════════════════════════════════════════╣
║ 📍 Lokasi: {location_name:<50} ║
║                                                                  ║
║ 📊 Risk Level: {level:<15} | Score: {risk}%                         ║
║ {bar}                                                             ║
║                                                                  ║
║ 📝 {risk_data['description']:<64} ║
║                                                                  ║
║ 🎭 Emotional Effect: +{effect['arousal_boost']} arousal | Mood: {effect['mood']}     ║
║                                                                  ║
║ 💡 **Tips:**                                                     ║
║ • Tetap waspada dengan sekitar                                   ║
║ • Jangan terlalu lama di satu tempat                             ║
║ • Siapkan alasan jika ketahuan                                   ║
║ • Matikan notifikasi HP                                          ║
╚══════════════════════════════════════════════════════════════════╝
"""


__all__ = ['RiskCalculator']
