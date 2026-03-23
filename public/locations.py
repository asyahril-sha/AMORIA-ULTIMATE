# public/locations.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Public Locations Database
Compatible with AMORIA's leveling system (1-12)
=============================================================================
"""

import random
import logging
from typing import Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class LocationCategory(str, Enum):
    """Kategori lokasi berdasarkan risiko AMORIA"""
    SAFE = "safe"           # Risiko rendah
    URBAN = "urban"         # Risiko sedang
    NATURE = "nature"       # Risiko rendah-menengah
    EXTREME = "extreme"     # Risiko tinggi
    TRANSPORT = "transport" # Risiko variatif


class Location:
    """Model lokasi public untuk AMORIA"""
    
    def __init__(self, id: str, name: str, category: LocationCategory, 
                 base_risk: int, base_thrill: int, description: str, tips: str,
                 min_level: int = 1, emotional_effect: str = "normal"):
        self.id = id
        self.name = name
        self.category = category
        self.base_risk = base_risk
        self.base_thrill = base_thrill
        self.description = description
        self.tips = tips
        self.min_level = min_level  # Level minimal AMORIA untuk akses
        self.emotional_effect = emotional_effect  # Pengaruh ke emotional flow
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.value,
            'base_risk': self.base_risk,
            'base_thrill': self.base_thrill,
            'description': self.description,
            'tips': self.tips,
            'min_level': self.min_level,
            'emotional_effect': self.emotional_effect
        }


class PublicLocations:
    """Database lokasi public AMORIA"""
    
    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self._init_locations()
        logger.info(f"✅ PublicLocations initialized: {len(self.locations)} locations")
    
    def _init_locations(self):
        """Inisialisasi semua lokasi dengan parameter AMORIA"""
        
        # ===== SAFE LOCATIONS (Level 1-12) =====
        safe = [
            ("kamar_tidur", "Kamar Tidur", LocationCategory.SAFE, 5, 50,
             "Kamar tidur yang nyaman dengan ranjang empuk. Privasi total.",
             "Tutup pintu, matikan lampu utama, nyalakan lampu tidur.",
             1, "relaxed"),
            ("ruang_tamu", "Ruang Tamu", LocationCategory.SAFE, 8, 45,
             "Ruang tamu dengan sofa empuk dan TV menyala.",
             "Tutup gorden, matikan TV, nikmati suasana.",
             1, "casual"),
            ("balkon", "Balkon", LocationCategory.SAFE, 12, 55,
             "Balkon dengan pemandangan kota. Udara malam sejuk.",
             "Tutup pintu kaca, matikan lampu luar.",
             3, "romantic"),
            ("ruang_kerja", "Ruang Kerja", LocationCategory.SAFE, 10, 40,
             "Ruang kerja dengan meja besar dan kursi nyaman.",
             "Kunci pintu, matikan lampu utama.",
             2, "professional"),
        ]
        for id, name, cat, risk, thrill, desc, tips, lvl, effect in safe:
            self.locations[id] = Location(id, name, cat, risk, thrill, desc, tips, lvl, effect)
        
        # ===== URBAN LOCATIONS (Level 4-12) =====
        urban = [
            ("mall_toilet", "Toilet Mall", LocationCategory.URBAN, 65, 75,
             "Toilet umum di mall yang ramai. Risiko ketahuan cukup tinggi.",
             "Pilih toilet di lantai atas yang sepi, masuk ke stall terakhir.",
             4, "anxious"),
            ("parkir_basement", "Parkiran Basement", LocationCategory.URBAN, 55, 70,
             "Parkiran basement yang gelap dan sepi. Mobil-mobil parkir berjajar.",
             "Parkir di pojok yang jauh dari CCTV, tutup kaca gelap.",
             4, "excited"),
            ("lift", "Lift", LocationCategory.URBAN, 60, 80,
             "Lift kaca dengan pemandangan kota. Risiko ketahuan tinggi.",
             "Pilih lift di jam sepi, tekan tombol lantai tertinggi.",
             5, "thrilling"),
            ("tangga_darurat", "Tangga Darurat", LocationCategory.URBAN, 50, 65,
             "Tangga darurat gedung yang sepi. Hanya digunakan saat darurat.",
             "Pilih jam istirahat kantor, masuk ke sudut yang tidak terlihat.",
             4, "adventurous"),
            ("ruang_ganti", "Ruang Ganti", LocationCategory.URBAN, 45, 70,
             "Ruang ganti di toko baju. Ada kaca besar dan kursi.",
             "Pilih jam sepi, masuk ke bilik terakhir.",
             4, "playful"),
            ("toilet_pom", "Toilet SPBU", LocationCategory.URBAN, 70, 80,
             "Toilet SPBU yang sering sepi di malam hari. Lampu temaram.",
             "Pilih SPBU yang sepi, parkir di pojok.",
             5, "tense"),
            ("gudang", "Gudang Toko", LocationCategory.URBAN, 50, 65,
             "Gudang di belakang toko yang jarang dikunjungi.",
             "Pastikan tidak ada CCTV, masuk saat jam makan siang.",
             4, "mysterious"),
        ]
        for id, name, cat, risk, thrill, desc, tips, lvl, effect in urban:
            self.locations[id] = Location(id, name, cat, risk, thrill, desc, tips, lvl, effect)
        
        # ===== NATURE LOCATIONS (Level 3-12) =====
        nature = [
            ("pantai_malam", "Pantai Malam", LocationCategory.NATURE, 35, 85,
             "Pantai sepi di malam hari, hanya suara ombak dan angin.",
             "Pilih spot yang gelap, bawa tikar, jangan terlalu dekat air.",
             3, "romantic"),
            ("hutan_pinus", "Hutan Pinus", LocationCategory.NATURE, 30, 80,
             "Hutan pinus yang sejuk dan sepi. Suasana sangat private.",
             "Pilih siang hari yang tidak terlalu ramai, bawa tenda kecil.",
             4, "peaceful"),
            ("taman_kota", "Taman Kota", LocationCategory.NATURE, 40, 65,
             "Taman kota dengan bangku-bangku tersembunyi di balik pohon.",
             "Pilih jam makan siang atau sore hari yang sepi.",
             3, "relaxed"),
            ("kebun_teh", "Kebun Teh", LocationCategory.NATURE, 25, 70,
             "Perkebunan teh dengan pemandangan indah dan udara sejuk.",
             "Pilih pagi hari saat kabut masih tebal, mobil parkir di area tersembunyi.",
             4, "calm"),
            ("air_terjun", "Air Terjun", LocationCategory.NATURE, 35, 75,
             "Air terjun tersembunyi di dalam hutan. Suara air menutupi suara lain.",
             "Pilih hari kerja agar sepi, cari spot di balik batu besar.",
             5, "energetic"),
            ("sawah", "Sawah Malam", LocationCategory.NATURE, 40, 70,
             "Area persawahan di malam hari, sangat sepi dan gelap.",
             "Bawa penerangan kecil, hati-hati dengan hewan.",
             4, "adventurous"),
            ("bukit", "Bukit Kecil", LocationCategory.NATURE, 30, 80,
             "Bukit kecil dengan pemandangan kota dari kejauhan.",
             "Pilih malam hari, bawa selimut, nikmati bintang.",
             3, "romantic"),
        ]
        for id, name, cat, risk, thrill, desc, tips, lvl, effect in nature:
            self.locations[id] = Location(id, name, cat, risk, thrill, desc, tips, lvl, effect)
        
        # ===== EXTREME LOCATIONS (Level 7-12) =====
        extreme = [
            ("masjid", "Halaman Masjid", LocationCategory.EXTREME, 85, 95,
             "Halaman masjid yang sepi di malam hari. Risiko sangat tinggi.",
             "Hati-hati! Sangat berisiko. Pilih malam larut saat tidak ada kegiatan.",
             8, "guilty"),
            ("kantor_polisi", "Belakang Kantor Polisi", LocationCategory.EXTREME, 90, 98,
             "Area belakang kantor polisi yang gelap. Risiko tertinggi!",
             "Hanya untuk yang paling berani. Siap-siap lari kalau ketahuan.",
             10, "terrified"),
            ("kuburan", "Area Pemakaman", LocationCategory.EXTREME, 70, 90,
             "Pemakaman umum yang sepi malam hari. Banyak mitos.",
             "Jangan ganggu yang sudah meninggal. Bawa sesajen kecil.",
             7, "spooky"),
            ("sekolah", "Halaman Sekolah", LocationCategory.EXTREME, 60, 80,
             "Halaman sekolah di malam hari. Ada satpam yang patroli.",
             "Pastikan tidak ada satpam, masuk dari belakang.",
             7, "nostalgic"),
            ("rumah_ibadah", "Rumah Ibadah", LocationCategory.EXTREME, 75, 85,
             "Rumah ibadah yang sepi di siang hari atau malam.",
             "Sangat tidak sopan jika ketahuan. Pilih waktu yang benar-benar kosong.",
             8, "guilty"),
            ("kantor_dinas", "Kantor Pemerintah", LocationCategory.EXTREME, 65, 85,
             "Kantor dinas di malam hari. Area parkir luas dan gelap.",
             "CCTV mungkin aktif, pilih spot buta kamera.",
             7, "tense"),
        ]
        for id, name, cat, risk, thrill, desc, tips, lvl, effect in extreme:
            self.locations[id] = Location(id, name, cat, risk, thrill, desc, tips, lvl, effect)
        
        # ===== TRANSPORT LOCATIONS (Level 4-12) =====
        transport = [
            ("mobil", "Di Dalam Mobil", LocationCategory.TRANSPORT, 45, 70,
             "Mobil dengan kaca film gelap. Bisa parkir di mana saja.",
             "Parkir di tempat sepi, mesin dimatikan, kaca ditutup.",
             4, "intimate"),
            ("kereta_malam", "Kereta Malam", LocationCategory.TRANSPORT, 50, 75,
             "Kereta ekonomi malam hari. Banyak kursi kosong.",
             "Pilih gerbong paling belakang, pilih waktu larut malam.",
             5, "adventurous"),
            ("bus_malam", "Bus Malam", LocationCategory.TRANSPORT, 55, 70,
             "Bus AKAP malam hari. Perjalanan panjang.",
             "Pilih kursi paling belakang, selimuti diri, jangan terlalu berisik.",
             5, "cozy"),
            ("kapal", "Kapal Ferry", LocationCategory.TRANSPORT, 40, 65,
             "Kapal ferry antar pulau. Banyak sudut tersembunyi.",
             "Pilih area belakang kapal yang sepi, malam hari.",
             4, "romantic"),
            ("pesawat", "Toilet Pesawat", LocationCategory.TRANSPORT, 85, 90,
             "Toilet di dalam pesawat. Risiko sangat tinggi!",
             "Hanya untuk yang berani. Lakukan cepat, jangan terlalu lama.",
             9, "thrilling"),
            ("truk", "Bak Truk", LocationCategory.TRANSPORT, 60, 75,
             "Bak truk yang parkir di rest area. Tertutup terpal.",
             "Pastikan supir tidak ada, pilih truk yang sudah lama parkir.",
             6, "adventurous"),
        ]
        for id, name, cat, risk, thrill, desc, tips, lvl, effect in transport:
            self.locations[id] = Location(id, name, cat, risk, thrill, desc, tips, lvl, effect)
        
        # ===== PREMIUM LOCATIONS (Level 10-12) =====
        premium = [
            ("puncak_gunung", "Puncak Gunung", LocationCategory.NATURE, 20, 95,
             "Puncak gunung saat sunrise. Pemandangan luar biasa.",
             "Camping semalam, tenda berdua di tengah alam.",
             10, "spiritual"),
            ("villa_terpencil", "Villa Terpencil", LocationCategory.SAFE, 15, 85,
             "Villa di pegunungan, jauh dari keramaian.",
             "Sewa villa private, nikmati kolam renang pribadi.",
             10, "luxurious"),
            ("hotel_mewah", "Hotel Mewah", LocationCategory.SAFE, 10, 80,
             "Hotel bintang 5 dengan privasi terjaga.",
             "Pilih room service, jangan keluar kamar.",
             8, "elegant"),
            ("yacht", "Yacht Pribadi", LocationCategory.TRANSPORT, 5, 95,
             "Yacht pribadi di tengah laut. Privasi total.",
             "Tepi laut, matikan mesin, nikmati bintang.",
             11, "blissful"),
        ]
        for id, name, cat, risk, thrill, desc, tips, lvl, effect in premium:
            self.locations[id] = Location(id, name, cat, risk, thrill, desc, tips, lvl, effect)
    
    def get_all_locations(self) -> List[Dict]:
        return [loc.to_dict() for loc in self.locations.values()]
    
    def get_locations_by_level(self, level: int) -> List[Dict]:
        """Dapatkan lokasi yang accessible berdasarkan level AMORIA"""
        return [loc.to_dict() for loc in self.locations.values() if loc.min_level <= level]
    
    def get_random_location(self, level: int = 1) -> Dict:
        """Dapatkan lokasi random yang sesuai level"""
        available = [loc for loc in self.locations.values() if loc.min_level <= level]
        if not available:
            available = list(self.locations.values())
        loc = random.choice(available)
        return loc.to_dict()
    
    def get_location_by_id(self, location_id: str) -> Optional[Dict]:
        loc = self.locations.get(location_id)
        return loc.to_dict() if loc else None
    
    def get_location_by_name(self, name: str) -> Optional[Dict]:
        name_lower = name.lower()
        for loc in self.locations.values():
            if loc.name.lower() == name_lower or name_lower in loc.name.lower():
                return loc.to_dict()
        return None
    
    def get_locations_by_category(self, category: LocationCategory, level: int = 1) -> List[Dict]:
        return [loc.to_dict() for loc in self.locations.values() 
                if loc.category == category and loc.min_level <= level]
    
    def get_location_stats(self, level: int = 1) -> Dict:
        """Dapatkan statistik lokasi berdasarkan level"""
        accessible = [loc for loc in self.locations.values() if loc.min_level <= level]
        stats = {
            'total': len(self.locations),
            'accessible': len(accessible),
            'locked': len(self.locations) - len(accessible),
            'next_unlock': self._get_next_unlock_level(level),
            'categories': {}
        }
        
        for cat in LocationCategory:
            cat_locs = [loc for loc in accessible if loc.category == cat]
            stats['categories'][cat.value] = len(cat_locs)
        
        return stats
    
    def _get_next_unlock_level(self, current_level: int) -> Optional[Dict]:
        """Dapatkan lokasi yang akan terbuka di level berikutnya"""
        for loc in self.locations.values():
            if loc.min_level > current_level:
                return {'name': loc.name, 'level': loc.min_level}
        return None


__all__ = ['PublicLocations', 'Location', 'LocationCategory']
