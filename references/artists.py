# references/artists.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
Artists Reference - Database Referensi Artis (Bukan Template)
=============================================================================
"""

import random
from typing import Dict, List, Optional


# =============================================================================
# REFERENSI INDONESIA - NON-HIJAB (18-30 TAHUN)
# =============================================================================

ARTIS_INDONESIA_NON_HIJAB = [
    {
        "nama": "Natasha Wilona",
        "umur": 25,
        "tinggi": 165,
        "berat": 51,
        "dada": "34B",
        "hijab": False,
        "instagram": "@natashawilona12",
        "ciri": "Artis muda sangat populer, wajah manis",
        "kategori": "aktris"
    },
    {
        "nama": "Prilly Latuconsina",
        "umur": 25,
        "tinggi": 162,
        "berat": 50,
        "dada": "34B",
        "hijab": False,
        "instagram": "@prillylatuconsina96",
        "ciri": "Aktris, penyanyi, vokal soal isu sosial",
        "kategori": "aktris"
    },
    {
        "nama": "Amanda Manopo",
        "umur": 24,
        "tinggi": 165,
        "berat": 53,
        "dada": "34C",
        "hijab": False,
        "instagram": "@amandamanopo",
        "ciri": "Artis sinetron, seksi alami",
        "kategori": "aktris"
    },
    {
        "nama": "Mikha Tambayong",
        "umur": 25,
        "tinggi": 167,
        "berat": 53,
        "dada": "34B",
        "hijab": False,
        "instagram": "@mikhata",
        "ciri": "Penyanyi dan aktris, manis, anggun",
        "kategori": "aktris"
    },
    {
        "nama": "Cinta Laura",
        "umur": 25,
        "tinggi": 172,
        "berat": 58,
        "dada": "36C",
        "hijab": False,
        "instagram": "@claurakiehl",
        "ciri": "Aktris, pintar, atletis, seksi natural",
        "kategori": "aktris"
    },
    {
        "nama": "Angga Yunanda",
        "umur": 24,
        "tinggi": 170,
        "berat": 62,
        "dada": "-",
        "hijab": False,
        "instagram": "@anggayunanda",
        "ciri": "Aktor muda populer, wajah fresh",
        "kategori": "aktor"
    },
    {
        "nama": "Fujianti Utami (Fuji)",
        "umur": 23,
        "tinggi": 160,
        "berat": 48,
        "dada": "34B",
        "hijab": False,
        "instagram": "@fuji_an",
        "ciri": "Selebgram muda dengan followers tercepat",
        "kategori": "selebgram"
    },
    {
        "nama": "Anya Geraldine",
        "umur": 26,
        "tinggi": 170,
        "berat": 55,
        "dada": "34C",
        "hijab": False,
        "instagram": "@anyagerladine",
        "ciri": "Selebgram dan aktris, gaya kasual",
        "kategori": "selebgram"
    },
    {
        "nama": "Syifa Hadju",
        "umur": 24,
        "tinggi": 162,
        "berat": 48,
        "dada": "32B",
        "hijab": False,
        "instagram": "@syifahadju",
        "ciri": "Aktris muda, wajah manis",
        "kategori": "aktris"
    },
    {
        "nama": "Megan Domani",
        "umur": 22,
        "tinggi": 165,
        "berat": 50,
        "dada": "34B",
        "hijab": False,
        "instagram": "@megandomani",
        "ciri": "Aktris, model",
        "kategori": "aktris"
    }
]


# =============================================================================
# REFERENSI INDONESIA - BERHIJAB (18-30 TAHUN)
# =============================================================================

ARTIS_INDONESIA_HIJAB = [
    {
        "nama": "Aurelie Moeremans",
        "umur": 27,
        "tinggi": 170,
        "berat": 54,
        "dada": "34B",
        "hijab": True,
        "instagram": "@aureliemoeremans",
        "ciri": "Aktris, model, influencer modest fashion",
        "kategori": "aktris"
    },
    {
        "nama": "Acha Septriasa",
        "umur": 30,
        "tinggi": 158,
        "berat": 47,
        "dada": "32B",
        "hijab": True,
        "instagram": "@achaseptriasa",
        "ciri": "Aktris, penyanyi, hijab fashion icon",
        "kategori": "aktris"
    },
    {
        "nama": "Irish Bella",
        "umur": 28,
        "tinggi": 165,
        "berat": 51,
        "dada": "34B",
        "hijab": True,
        "instagram": "_irishbella_",
        "ciri": "Aktris sinetron, hijab fashion",
        "kategori": "aktris"
    },
    {
        "nama": "Della Dartyan",
        "umur": 28,
        "tinggi": 168,
        "berat": 54,
        "dada": "34C",
        "hijab": True,
        "instagram": "@delladartyan",
        "ciri": "Aktris, model hijab",
        "kategori": "aktris"
    }
]


# =============================================================================
# REFERENSI INTERNASIONAL - K-POP (NON-HIJAB)
# =============================================================================

ARTIS_INTERNASIONAL_NON_HIJAB = [
    {
        "nama": "Lisa (BLACKPINK)",
        "umur": 25,
        "tinggi": 167,
        "berat": 48,
        "dada": "34B",
        "hijab": False,
        "instagram": "@lalalalisa_m",
        "ciri": "Idol K-pop, dancer, fashion icon",
        "group": "BLACKPINK",
        "negara": "Thailand"
    },
    {
        "nama": "Rosé (BLACKPINK)",
        "umur": 25,
        "tinggi": 168,
        "berat": 46,
        "dada": "34A",
        "hijab": False,
        "instagram": "@roses_are_rosie",
        "ciri": "Vokalis, artistik, elegant",
        "group": "BLACKPINK",
        "negara": "Selandia Baru"
    },
    {
        "nama": "Jennie (BLACKPINK)",
        "umur": 28,
        "tinggi": 163,
        "berat": 48,
        "dada": "34B",
        "hijab": False,
        "instagram": "@jennierubyjane",
        "ciri": "Rapper, fashion icon",
        "group": "BLACKPINK",
        "negara": "Korea"
    },
    {
        "nama": "Jisoo (BLACKPINK)",
        "umur": 28,
        "tinggi": 162,
        "berat": 46,
        "dada": "34A",
        "hijab": False,
        "instagram": "@sooyaaa__",
        "ciri": "Visual, vokalis, aktris",
        "group": "BLACKPINK",
        "negara": "Korea"
    },
    {
        "nama": "Wonyoung (IVE)",
        "umur": 21,
        "tinggi": 173,
        "berat": 48,
        "dada": "34B",
        "hijab": False,
        "instagram": "@for_everyyoung10",
        "ciri": "Center IVE, visual, model",
        "group": "IVE",
        "negara": "Korea"
    }
]


# =============================================================================
# REFERENSI INTERNASIONAL - BERHIJAB
# =============================================================================

ARTIS_INTERNASIONAL_HIJAB = [
    {
        "nama": "Aiman Khan",
        "umur": 25,
        "tinggi": 162,
        "berat": 48,
        "dada": "32B",
        "hijab": True,
        "instagram": "@aimankhan.official",
        "ciri": "Aktris Pakistan, hijab fashion icon",
        "negara": "Pakistan"
    },
    {
        "nama": "Merve Boluğur",
        "umur": 28,
        "tinggi": 170,
        "berat": 55,
        "dada": "34C",
        "hijab": True,
        "instagram": "@mervebolugur",
        "ciri": "Aktris Turki, mulai berhijab sejak 2020",
        "negara": "Turki"
    }
]


# =============================================================================
# GABUNGKAN SEMUA
# =============================================================================

ALL_ARTIS = (
    ARTIS_INDONESIA_NON_HIJAB +
    ARTIS_INDONESIA_HIJAB +
    ARTIS_INTERNASIONAL_NON_HIJAB +
    ARTIS_INTERNASIONAL_HIJAB
)


# =============================================================================
# ROLE SPECIFIC REFERENCES
# =============================================================================

ROLE_REFERENCES = {
    "ipar": ARTIS_INDONESIA_NON_HIJAB[:5],
    "teman_kantor": ARTIS_INDONESIA_NON_HIJAB[3:8],
    "janda": ARTIS_INDONESIA_NON_HIJAB[2:6],
    "pelakor": ARTIS_INDONESIA_NON_HIJAB[4:7],
    "istri_orang": ARTIS_INDONESIA_NON_HIJAB[1:5] + ARTIS_INDONESIA_HIJAB[:2],
    "pdkt": ARTIS_INDONESIA_NON_HIJAB[0:4],
    "sepupu": ARTIS_INDONESIA_NON_HIJAB[6:10],
    "teman_sma": ARTIS_INDONESIA_NON_HIJAB[7:12],
    "mantan": ARTIS_INDONESIA_NON_HIJAB[2:7]
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_random_artist_for_role(role: str) -> dict:
    """Get random artist reference for specific role"""
    if role in ROLE_REFERENCES:
        return random.choice(ROLE_REFERENCES[role])
    return random.choice(ALL_ARTIS)


def get_artist_by_name(nama: str) -> Optional[dict]:
    """Find artist by name"""
    for artis in ALL_ARTIS:
        if artis["nama"].lower() == nama.lower():
            return artis
    return None


def format_artist_description(artist: dict) -> str:
    """Format artist description for display"""
    desc = f"• **{artist['nama']}** "
    desc += f"({artist['umur']} th, {artist['tinggi']}cm/{artist['berat']}kg, {artist['dada']})\n"
    if 'instagram' in artist:
        desc += f"  📲 IG: @{artist['instagram'].replace('@', '')}\n"
    if 'ciri' in artist:
        desc += f"  💫 {artist['ciri']}"
    return desc


def get_artist_by_popularity(min_followers: int = 1_000_000) -> List[dict]:
    """Get artists by minimum followers"""
    def parse_followers(f_str):
        if 'M' in f_str:
            return float(f_str.replace('M', '')) * 1_000_000
        elif 'K' in f_str:
            return float(f_str.replace('K', '')) * 1_000
        return 0
    
    results = []
    for artis in ALL_ARTIS:
        followers = parse_followers(artis.get('followers', '0'))
        if followers >= min_followers:
            results.append(artis)
    
    return sorted(results, key=lambda x: parse_followers(x.get('followers', '0')), reverse=True)


__all__ = [
    'ARTIS_INDONESIA_NON_HIJAB',
    'ARTIS_INDONESIA_HIJAB',
    'ARTIS_INTERNASIONAL_NON_HIJAB',
    'ARTIS_INTERNASIONAL_HIJAB',
    'ALL_ARTIS',
    'ROLE_REFERENCES',
    'get_random_artist_for_role',
    'get_artist_by_name',
    'format_artist_description',
    'get_artist_by_popularity'
]
