# public/area_manager.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Area Manager for Public Locations
Integration with AMORIA's state persistence and spatial awareness
=============================================================================
"""

import time
import logging
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


class AreaManager:
    """Manager untuk area public AMORIA dengan state persistence"""
    
    def __init__(self, locations, risk_calc, thrill_calc, events):
        self.locations = locations
        self.risk_calc = risk_calc
        self.thrill_calc = thrill_calc
        self.events = events
        self.current_location: Optional[str] = None
        self.visit_history: Dict[str, int] = {}  # location_id -> visit_count
        self.last_event_time: float = 0
        logger.info("✅ AreaManager initialized for AMORIA")
    
    async def enter_location(self, location_id: str, character_data: Dict) -> Dict:
        """
        Masuk ke lokasi public dengan update state AMORIA
        
        Args:
            location_id: ID lokasi
            character_data: Data karakter AMORIA (level, arousal, dll)
        """
        location = self.locations.get_location_by_id(location_id)
        if not location:
            return {'success': False, 'error': 'Location not found'}
        
        level = character_data.get('level', 1)
        arousal = character_data.get('arousal', 0)
        in_cycle = character_data.get('in_intimacy_cycle', False)
        
        # Cek level requirement
        if level < location['min_level']:
            return {
                'success': False,
                'error': f'Level {level} belum cukup. Butuh level {location["min_level"]} untuk akses {location["name"]}.'
            }
        
        # Hitung risk dan thrill
        risk = await self.risk_calc.calculate_risk(
            location['base_risk'], level, arousal, in_cycle
        )
        thrill = await self.thrill_calc.calculate_thrill(
            location['base_thrill'], risk['final_risk'], level, 
            location['category'], arousal, in_cycle
        )
        
        # Update history
        self.current_location = location_id
        self.visit_history[location_id] = self.visit_history.get(location_id, 0) + 1
        
        # Cek event
        event = self.events.get_random_event(risk['final_risk'], level)
        self.last_event_time = time.time()
        
        return {
            'success': True,
            'location': location,
            'risk': risk,
            'thrill': thrill,
            'event': event,
            'visit_count': self.visit_history[location_id]
        }
    
    async def update_location_state(self, character_data: Dict, 
                                     action: str = "stay") -> Dict:
        """Update state lokasi berdasarkan aktivitas"""
        if not self.current_location:
            return {'success': False, 'error': 'No current location'}
        
        location = self.locations.get_location_by_id(self.current_location)
        if not location:
            return {'success': False, 'error': 'Location not found'}
        
        arousal = character_data.get('arousal', 0)
        level = character_data.get('level', 1)
        
        # Update arousal berdasarkan lokasi
        arousal_change = 0
        mood_effect = location.get('emotional_effect', 'normal')
        
        if action == "intim":
            arousal_change += 20
        elif action == "kiss":
            arousal_change += 10
        elif action == "touch":
            arousal_change += 5
        
        # Cek event baru
        event = None
        if time.time() - self.last_event_time > 300:  # 5 menit
            event = self.events.get_random_event(location['base_risk'], level)
            if event:
                arousal_change += event['arousal_change']
                self.last_event_time = time.time()
        
        return {
            'success': True,
            'location': location,
            'arousal_change': arousal_change,
            'mood_effect': mood_effect,
            'event': event,
            'visit_count': self.visit_history.get(self.current_location, 0)
        }
    
    def leave_location(self) -> Dict:
        """Keluar dari lokasi public"""
        old_location = self.current_location
        self.current_location = None
        
        return {
            'success': True,
            'left_location': old_location,
            'visit_count': self.visit_history.get(old_location, 0) if old_location else 0
        }
    
    def get_current_location(self) -> Optional[Dict]:
        """Dapatkan lokasi saat ini"""
        if not self.current_location:
            return None
        return self.locations.get_location_by_id(self.current_location)
    
    def get_visit_stats(self) -> Dict:
        """Dapatkan statistik kunjungan"""
        return {
            'current_location': self.current_location,
            'total_visits': sum(self.visit_history.values()),
            'unique_locations': len(self.visit_history),
            'most_visited': max(self.visit_history.items(), key=lambda x: x[1])[0] if self.visit_history else None,
            'history': self.visit_history.copy()
        }


__all__ = ['AreaManager']
