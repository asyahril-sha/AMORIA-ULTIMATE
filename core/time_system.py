# core/time_system.py
# -*- coding: utf-8 -*-
"""
Time System untuk AMORIA
"""

import time
import re
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class TimeSystem:
    """
    Sistem waktu realistis untuk AMORIA
    - Waktu berjalan natural
    - Bisa di-override oleh user
    - Mempengaruhi mood dan aktivitas
    """
    
    def __init__(self, initial_time: Optional[str] = None):
        """
        Args:
            initial_time: Waktu awal dalam format "HH:MM" atau None (pakai waktu real)
        """
        if initial_time:
            self.current = initial_time
        else:
            self.current = datetime.now().strftime("%H:%M")
        
        self.last_update = time.time()
        self.override_history: list = []
        self.override_count = 0
    
    def advance(self, minutes: int = 5):
        """
        Majukan waktu berdasarkan percakapan
        Setiap chat memajukan waktu 5 menit
        
        Args:
            minutes: Menit yang dimajukan (default 5)
        """
        try:
            current_dt = datetime.strptime(self.current, "%H:%M")
            new_dt = current_dt + timedelta(minutes=minutes)
            self.current = new_dt.strftime("%H:%M")
            self.last_update = time.time()
        except Exception as e:
            logger.warning(f"Time advance failed: {e}")
    
    def detect_and_apply(self, user_message: str):
        """
        Deteksi keyword waktu dari pesan user dan override waktu
        
        Args:
            user_message: Pesan dari user
        """
        msg_lower = user_message.lower()
        
        # Mapping keyword ke waktu
        time_patterns = {
            'subuh': '04:30',
            'pagi': '08:00',
            'pagi-pagi': '07:00',
            'siang': '12:00',
            'sore': '16:00',
            'petang': '17:00',
            'malam': '20:00',
            'malam-malam': '22:00',
            'tengah malam': '00:00',
            'dini hari': '02:00',
        }
        
        # Regex untuk waktu spesifik (jam 7, jam 8 malam)
        time_regex = r'jam (\d{1,2})(?:\s*(\w+))?'
        match = re.search(time_regex, msg_lower)
        
        if match:
            hour = int(match.group(1))
            period = match.group(2) if match.group(2) else ''
            
            if period in ['malam', 'mlm']:
                hour = hour if hour < 12 else hour
            elif period in ['pagi', 'siang']:
                pass
            elif hour < 7:
                pass
            
            new_time = f"{hour:02d}:00"
            self._apply_override(new_time, f"user said jam {hour}")
            return
        
        # Cek keyword waktu
        for keyword, time_str in time_patterns.items():
            if keyword in msg_lower:
                self._apply_override(time_str, keyword)
                break
    
    def _apply_override(self, new_time: str, reason: str):
        """Apply time override and record history"""
        old_time = self.current
        
        if old_time != new_time:
            self.current = new_time
            self.override_count += 1
            
            self.override_history.append({
                'timestamp': time.time(),
                'old_time': old_time,
                'new_time': new_time,
                'reason': reason
            })
            
            # Keep only last 20 overrides
            if len(self.override_history) > 20:
                self.override_history = self.override_history[-20:]
            
            logger.debug(f"Time overridden: {old_time} → {new_time} ({reason})")
    
    def get_time_feel(self) -> str:
        """Get descriptive time feel for prompts"""
        hour = int(self.current.split(':')[0])
        
        if 4 <= hour < 6:
            return "subuh"
        elif 6 <= hour < 10:
            return "pagi"
        elif 10 <= hour < 14:
            return "siang"
        elif 14 <= hour < 18:
            return "sore"
        elif 18 <= hour < 22:
            return "malam"
        else:
            return "malam"
    
    def get_time_display(self) -> str:
        """Get time for display"""
        return self.current
    
    def get_time_of_day(self) -> str:
        """Get time category"""
        return self.get_time_feel()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for storage"""
        return {
            'current': self.current,
            'last_update': self.last_update,
            'override_history': self.override_history,
            'override_count': self.override_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TimeSystem':
        """Create from stored dict"""
        instance = cls(data.get('current'))
        instance.last_update = data.get('last_update', time.time())
        instance.override_history = data.get('override_history', [])
        instance.override_count = data.get('override_count', 0)
        return instance
