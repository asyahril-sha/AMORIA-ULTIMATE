# public/events.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Random Events for Public Areas
Compatible with AMORIA's emotional flow and arousal system
=============================================================================
"""

import random
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class RandomEvents:
    """Event random di lokasi public AMORIA"""
    
    def __init__(self):
        self.events = {
            'caught': {
                'messages': [
                    "⚠️ Seseorang lewat! Cepet sembunyi!",
                    "🚪 Pintu terbuka! Ada yang masuk!",
                    "👣 Suara langkah kaki mendekat!",
                    "🔦 Senter menyorot! Awas!",
                    "🗣️ Ada yang manggil! Cepet sembunyi!",
                    "📱 HP berdering kencang! Matiin!"
                ],
                'arousal_change': 20,
                'mood_effect': 'panicked',
                'risk_increase': 30
            },
            'almost_caught': {
                'messages': [
                    "😰 Ada yang lewat, tapi gak liat kita.",
                    "🚪 Pintu terbuka sebentar, untung cepet nutup.",
                    "👣 Suara langkah kaki, tapi lewat aja.",
                    "🔦 Senter menyorot ke arah kita, tapi gak fokus.",
                    "🗣️ Ada yang manggil dari jauh, tapi gak nyamperin.",
                    "📱 HP bergetar, untung langsung dimatiin."
                ],
                'arousal_change': 10,
                'mood_effect': 'excited',
                'risk_increase': 10
            },
            'romantic': {
                'messages': [
                    "🌧️ Tiba-tiba hujan rintik-rintik, makin romantis.",
                    "🎵 Suara musik dari kejauhan menambah suasana.",
                    "🌙 Cahaya bulan menyinari wajahmu.",
                    "🍃 Angin sepoi-sepoi bikin suasana makin hangat.",
                    "✨ Bintang bertaburan di langit, malam sempurna.",
                    "🕯️ Lampu jalan tiba-tiba mati, suasana jadi lebih intim."
                ],
                'arousal_change': 15,
                'mood_effect': 'romantic',
                'risk_increase': -5
            },
            'disturbance': {
                'messages': [
                    "🔊 Suara kendaraan mendekat dengan kencang!",
                    "💡 Lampu tiba-tiba menyala terang!",
                    "📢 Ada pengumuman melalui pengeras suara!",
                    "🚨 Alarm mobil berbunyi di dekat situ!",
                    "🐕 Anjing menggonggong keras dari kejauhan!"
                ],
                'arousal_change': -5,
                'mood_effect': 'alert',
                'risk_increase': 15
            },
            'funny': {
                'messages': [
                    "😹 Tiba-tiba kamu bersin keras, kami berdua terkekeh.",
                    "🤣 Ada yang lewat dengan gaya lucu, kami menahan tawa.",
                    "🐱 Seekor kucing lewat dan melongo melihat kita.",
                    "🍃 Daun kering jatuh tepat di kepalaku, kamu tertawa.",
                    "📱 HP-mu tiba-tiba berbunyi dengan nada dering lucu."
                ],
                'arousal_change': 5,
                'mood_effect': 'playful',
                'risk_increase': 0
            }
        }
        logger.info("✅ RandomEvents initialized for AMORIA")
    
    def get_random_event(self, location_risk: int, intimacy_level: int = 1) -> Optional[Dict]:
        """
        Dapatkan event random berdasarkan risiko lokasi dan level
        
        Args:
            location_risk: Risiko lokasi (0-100)
            intimacy_level: Level AMORIA (1-12)
        """
        # Semakin tinggi level, semakin kecil chance kena event negatif
        base_chance = 0.15
        if intimacy_level >= 10:
            base_chance = 0.08
        elif intimacy_level >= 7:
            base_chance = 0.10
        elif intimacy_level >= 4:
            base_chance = 0.12
        
        if random.random() > base_chance:
            return None
        
        # Pilih event berdasarkan risiko
        if location_risk >= 70:
            event_type = random.choices(
                ['caught', 'almost_caught', 'disturbance'],
                weights=[0.3, 0.4, 0.3]
            )[0]
        elif location_risk >= 40:
            event_type = random.choices(
                ['almost_caught', 'disturbance', 'romantic', 'funny'],
                weights=[0.3, 0.2, 0.3, 0.2]
            )[0]
        else:
            event_type = random.choices(
                ['romantic', 'funny', 'almost_caught'],
                weights=[0.5, 0.3, 0.2]
            )[0]
        
        event = self.events[event_type]
        
        # Modifikasi berdasarkan level
        arousal_change = event['arousal_change']
        if intimacy_level >= 7 and event_type in ['caught', 'disturbance']:
            arousal_change = int(arousal_change * 0.7)  # Lebih tenang
        elif intimacy_level >= 10 and event_type == 'romantic':
            arousal_change = int(arousal_change * 1.3)  # Lebih menikmati
        
        return {
            'type': event_type,
            'message': random.choice(event['messages']),
            'arousal_change': arousal_change,
            'mood_effect': event['mood_effect'],
            'risk_increase': event['risk_increase']
        }
    
    def format_event_message(self, event: Dict) -> str:
        """Format pesan event untuk ditampilkan"""
        emojis = {
            'caught': '⚠️',
            'almost_caught': '😰',
            'romantic': '💕',
            'disturbance': '🔊',
            'funny': '😹'
        }
        
        emoji = emojis.get(event['type'], '✨')
        arousal_text = f"+{event['arousal_change']}" if event['arousal_change'] >= 0 else f"{event['arousal_change']}"
        
        return f"{emoji} _{event['message']}_\n🎭 Arousal: {arousal_text}% | Mood: {event['mood_effect']}"


__all__ = ['RandomEvents']
