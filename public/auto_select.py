# public/auto_select.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Location Auto Selector
Compatible with AMORIA's leveling and weighted memory
=============================================================================
"""

import logging
import random
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


class LocationAutoSelector:
    """Auto selector lokasi berdasarkan level AMORIA dan preferensi"""
    
    def __init__(self, locations):
        self.locations = locations
        logger.info("✅ LocationAutoSelector initialized for AMORIA")
    
    def auto_select(self, intimacy_level: int, prefer_category: Optional[str] = None,
                    arousal: int = 0, memory_score: float = 0.5) -> Dict:
        """
        Auto select lokasi berdasarkan level AMORIA
        
        Args:
            intimacy_level: Level AMORIA (1-12)
            prefer_category: Kategori preferensi
            arousal: Arousal saat ini
            memory_score: Weighted memory score (pengaruh dari kenangan)
        """
        available = [loc for loc in self.locations.locations.values() 
                    if loc.min_level <= intimacy_level]
        
        if prefer_category:
            category_filter = [l for l in available if l.category.value == prefer_category]
            if category_filter:
                available = category_filter
        
        if not available:
            available = list(self.locations.locations.values())
        
        weights = []
        for loc in available:
            weight = 0
            
            # Level-based weight
            if intimacy_level >= 10:
                weight += (100 - loc.base_risk) * 0.5 + loc.base_thrill * 0.5
            elif intimacy_level >= 7:
                weight += (100 - loc.base_risk) * 0.6 + loc.base_thrill * 0.4
            elif intimacy_level >= 4:
                weight += (100 - loc.base_risk) * 0.4 + loc.base_thrill * 0.6
            else:
                weight += loc.base_thrill
            
            # Arousal influence
            weight += arousal * 0.3
            
            # Memory score influence
            weight += memory_score * 20
            
            # Category bonus
            if loc.category == LocationCategory.SAFE and arousal < 30:
                weight += 20
            elif loc.category == LocationCategory.EXTREME and arousal > 50:
                weight += 30
            
            weights.append(max(1, weight))
        
        selected = random.choices(available, weights=weights, k=1)[0]
        return selected.to_dict()
    
    def suggest_locations(self, intimacy_level: int, limit: int = 5,
                          prefer_category: Optional[str] = None) -> List[Dict]:
        """Rekomendasikan lokasi berdasarkan level"""
        available = [loc for loc in self.locations.locations.values() 
                    if loc.min_level <= intimacy_level]
        
        if prefer_category:
            available = [l for l in available if l.category.value == prefer_category]
        
        if not available:
            available = list(self.locations.locations.values())
        
        scored = []
        for loc in available:
            score = 0
            if intimacy_level >= 10:
                score = (100 - loc.base_risk) * 0.5 + loc.base_thrill * 0.5
            elif intimacy_level >= 7:
                score = (100 - loc.base_risk) * 0.6 + loc.base_thrill * 0.4
            else:
                score = (100 - loc.base_risk) * 0.3 + loc.base_thrill * 0.7
            scored.append((loc, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [loc.to_dict() for loc, _ in scored[:limit]]
    
    def get_recommendation_message(self, intimacy_level: int, 
                                   memory_score: float = 0.5) -> str:
        """Dapatkan pesan rekomendasi lokasi"""
        selected = self.auto_select(intimacy_level, memory_score=memory_score)
        
        category_emoji = {
            'safe': '🏠',
            'urban': '🏙️',
            'nature': '🌳',
            'extreme': '⚡',
            'transport': '🚗'
        }.get(selected['category'], '📍')
        
        return f"""
{category_emoji} **{selected['name']}** - Level {selected['min_level']}+
_{selected['description']}_

⚠️ Risk: {selected['base_risk']}% | 🎢 Thrill: {selected['base_thrill']}%
💡 Tips: {selected['tips']}
"""


__all__ = ['LocationAutoSelector']
