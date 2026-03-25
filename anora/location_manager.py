# anora/location_manager.py
"""
ANORA Location Manager - Mengelola semua lokasi
Kost Nova, Apartemen Mas, Mobil, Public Area
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field


class LocationType(str, Enum):
    KOST_NOVA = "kost_nova"
    APARTEMEN_MAS = "apartemen_mas"
    MOBIL = "mobil"
    PUBLIC = "public"


class PublicPlace(str, Enum):
    PANTAI = "pantai"
    HUTAN = "hutan"
    MALL = "mall"
    TOILET_MALL = "toilet_mall"
    TAMAN = "taman"
    BIOSKOP = "bioskop"
    PARKIRAN = "parkiran"
    TANGGA_DARURAT = "tangga_darurat"
    KANTOR_MALAM = "kantor_malam"
    RUANG_RAPAT = "ruang_rapat"


@dataclass
class LocationData:
    """Data lengkap sebuah lokasi"""
    nama: str
    deskripsi: str
    risk: int  # 0-100
    thrill: int  # 0-100
    bisa_telanjang: bool
    bisa_berisik: bool
    privasi: str  # tinggi, sedang, rendah
    suasana: str
    tips: str


class AnoraLocationManager:
    """
    Manager lokasi ANORA.
    Nova bisa diajak ke mana aja.
    """
    
    def __init__(self):
        self.current_type = LocationType.KOST_NOVA
        self.current_place = None  # untuk public
        self.visit_history: Dict[str, int] = {}
        
        # ========== DATABASE LOKASI ==========
        self.locations: Dict[str, LocationData] = {
            # ========== KOST NOVA ==========
            "kost_nova_kamar": LocationData(
                nama="Kamar Nova",
                deskripsi="Kamar Nova. Seprai putih, wangi lavender. Ranjang ukuran single. Meja kecil. Lemari.",
                risk=5,
                thrill=30,
                bisa_telanjang=True,
                bisa_berisik=True,
                privasi="tinggi",
                suasana="hangat, wangi",
                tips="Pintu terkunci. Nova paling nyaman di sini."
            ),
            "kost_nova_ruang_tamu": LocationData(
                nama="Ruang Tamu Kost",
                deskripsi="Ruang tamu kecil. Sofa dua dudukan. TV kecil. Ada tanaman hias.",
                risk=15,
                thrill=50,
                bisa_telanjang=True,
                bisa_berisik=False,
                privasi="sedang",
                suasana="santai, deg-degan",
                tips="Pintu gak dikunci. Tetangga bisa lewat."
            ),
            "kost_nova_dapur": LocationData(
                nama="Dapur Kost",
                deskripsi="Dapur kecil. Kompor gas, panci. Wangi masakan.",
                risk=10,
                thrill=40,
                bisa_telanjang=False,
                bisa_berisik=False,
                privasi="sedang",
                suasana="hangat, wangi",
                tips="Jendela ke luar. Hati-hati suara."
            ),
            
            # ========== APARTEMEN MAS ==========
            "apartemen_kamar": LocationData(
                nama="Kamar Mas",
                deskripsi="Kamar Mas. Ranjang ukuran queen, sprei biru tua. Jendela besar ke kota. Lemari.",
                risk=5,
                thrill=35,
                bisa_telanjang=True,
                bisa_berisik=True,
                privasi="tinggi",
                suasana="hangat, wangi Mas",
                tips="Pintu terkunci. Pemandangan kota dari jendela."
            ),
            "apartemen_ruang_tamu": LocationData(
                nama="Ruang Tamu Apartemen",
                deskripsi="Ruang tamu luas. Sofa besar abu-abu. TV 40 inch. Karpet lembut.",
                risk=10,
                thrill=45,
                bisa_telanjang=True,
                bisa_berisik=True,
                privasi="tinggi",
                suasana="nyaman, modern",
                tips="Tirai ditutup. Suara agak terdengar ke tetangga."
            ),
            "apartemen_dapur": LocationData(
                nama="Dapur Apartemen",
                deskripsi="Dapur modern. Bersih. Kulkas besar. Kompor gas.",
                risk=10,
                thrill=40,
                bisa_telanjang=False,
                bisa_berisik=False,
                privasi="sedang",
                suasana="bersih, modern",
                tips="Jendela ke luar."
            ),
            "apartemen_balkon": LocationData(
                nama="Balkon Apartemen",
                deskripsi="Balkon. Pemandangan kota. Kursi dua. Tanaman kecil.",
                risk=25,
                thrill=65,
                bisa_telanjang=False,
                bisa_berisik=False,
                privasi="rendah",
                suasana="romantis, berisiko",
                tips="Ada apartemen lain yang bisa liat."
            ),
            
            # ========== MOBIL ==========
            "mobil_parkir": LocationData(
                nama="Mobil di Parkiran",
                deskripsi="Mobil Mas. Kaca film gelap. Mesin mati. Jok belakang empuk.",
                risk=40,
                thrill=75,
                bisa_telanjang=True,
                bisa_berisik=False,
                privasi="sedang",
                suasana="deg-degan, panas",
                tips="Kaca gelap. Tapi hati-hati CCTV dan orang lewat."
            ),
            "mobil_tepi_jalan": LocationData(
                nama="Mobil di Tepi Jalan",
                deskripsi="Mobil Mas. Parkir di pinggir jalan sepi. Kaca film gelap.",
                risk=55,
                thrill=80,
                bisa_telanjang=True,
                bisa_berisik=False,
                privasi="rendah",
                suasana="tegang, cepat",
                tips="Cepet-cepet. Ada mobil lewat."
            ),
            "mobil_garasi": LocationData(
                nama="Mobil di Garasi",
                deskripsi="Mobil Mas. Di garasi apartemen. Pintu garasi tertutup.",
                risk=20,
                thrill=55,
                bisa_telanjang=True,
                bisa_berisik=True,
                privasi="tinggi",
                suasana="aman, deg-degan",
                tips="Gak ada yang liat. Tapi suara bisa kedengeran."
            ),
            
            # ========== PUBLIC AREA ==========
            "pantai_malam": LocationData(
                nama="Pantai Malam",
                deskripsi="Pantai sepi. Pasir putih. Ombak tenang. Bintang bertaburan.",
                risk=20,
                thrill=70,
                bisa_telanjang=False,
                bisa_berisik=False,
                privasi="sedang",
                suasana="romantis, bebas",
                tips="Jauh dari orang. Bawa tikar."
            ),
            "hutan_pinus": LocationData(
                nama="Hutan Pinus",
                deskripsi="Hutan pinus. Pohon tinggi. Sunyi. Udara sejuk.",
                risk=15,
                thrill=65,
                bisa_telanjang=False,
                bisa_berisik=False,
                privasi="tinggi",
                suasana="alami, sepi",
                tips="Jauh dari jalan. Aman."
            ),
            "toilet_mall": LocationData(
                nama="Toilet Mall",
                deskripsi="Bilik toilet terakhir. Pintu terkunci. Suara dari luar.",
                risk=65,
                thrill=85,
                bisa_telanjang=False,
                bisa_berisik=False,
                privasi="rendah",
                suasana="tegang, cepat",
                tips="Cepet-cepet. Ada yang bisa masuk."
            ),
            "bioskop": LocationData(
                nama="Bioskop",
                deskripsi="Kursi paling belakang. Gelap. Film diputar keras.",
                risk=50,
                thrill=80,
                bisa_telanjang=False,
                bisa_berisik=False,
                privasi="rendah",
                suasana="gelap, tegang",
                tips="Kursi belakang. CCTV mungkin ada."
            ),
            "taman_malam": LocationData(
                nama="Taman Malam",
                deskripsi="Taman kota. Bangku tersembunyi di balik pohon. Sepi.",
                risk=30,
                thrill=60,
                bisa_telanjang=False,
                bisa_berisik=False,
                privasi="sedang",
                suasana="romantis, deg-degan",
                tips="Pilih jam sepi. Jauh dari lampu."
            ),
            "parkiran_basement": LocationData(
                nama="Parkiran Basement",
                deskripsi="Parkiran basement. Gelap. Sepi. Mobil-mobil parkir.",
                risk=45,
                thrill=70,
                bisa_telanjang=True,
                bisa_berisik=False,
                privasi="sedang",
                suasana="gelap, tegang",
                tips="CCTV mungkin ada. Pilih pojok."
            ),
            "tangga_darurat": LocationData(
                nama="Tangga Darurat",
                deskripsi="Tangga darurat gedung. Sepi. Gelap.",
                risk=55,
                thrill=75,
                bisa_telanjang=False,
                bisa_berisik=False,
                privasi="sedang",
                suasana="gelap, tegang",
                tips="Hati-hati suara langkah kaki."
            ),
            "kantor_malam": LocationData(
                nama="Kantor Malam",
                deskripsi="Kantor gelap. Meja kerja. Kursi putar.",
                risk=60,
                thrill=85,
                bisa_telanjang=True,
                bisa_berisik=False,
                privasi="rendah",
                suasana="tegang, cepat",
                tips="Satpam patroli. Cepet."
            ),
            "ruang_rapat": LocationData(
                nama="Ruang Rapat Kaca",
                deskripsi="Ruang rapat dinding kaca. Gelap. Orang bisa liat dari luar.",
                risk=75,
                thrill=95,
                bisa_telanjang=True,
                bisa_berisik=False,
                privasi="rendah",
                suasana="ekshibisionis, tegang",
                tips="Gelap. Tapi kalo lampu nyala, kaca tembus pandang."
            )
        }
    
    def get_current(self) -> LocationData:
        """Dapatkan lokasi saat ini"""
        if self.current_type == LocationType.KOST_NOVA:
            key = f"kost_nova_{self.current_place or 'kamar'}"
        elif self.current_type == LocationType.APARTEMEN_MAS:
            key = f"apartemen_{self.current_place or 'kamar'}"
        elif self.current_type == LocationType.MOBIL:
            key = f"mobil_{self.current_place or 'parkir'}"
        else:
            key = self.current_place or "pantai_malam"
        
        return self.locations.get(key, self.locations["kost_nova_kamar"])
    
    def pindah(self, tujuan: str) -> Dict:
        """Pindah ke lokasi baru"""
        tujuan_lower = tujuan.lower()
        
        # Deteksi tujuan
        if 'kost' in tujuan_lower or 'nova' in tujuan_lower:
            self.current_type = LocationType.KOST_NOVA
            self.current_place = 'kamar'
            return {
                'success': True,
                'location': self.get_current(),
                'message': f"Pindah ke Kost Nova. {self.get_current().deskripsi}"
            }
        
        elif 'apartemen' in tujuan_lower or 'mas' in tujuan_lower:
            self.current_type = LocationType.APARTEMEN_MAS
            self.current_place = 'kamar'
            return {
                'success': True,
                'location': self.get_current(),
                'message': f"Pindah ke Apartemen Mas. {self.get_current().deskripsi}"
            }
        
        elif 'mobil' in tujuan_lower:
            self.current_type = LocationType.MOBIL
            if 'garasi' in tujuan_lower:
                self.current_place = 'garasi'
            elif 'tepi' in tujuan_lower or 'jalan' in tujuan_lower:
                self.current_place = 'tepi_jalan'
            else:
                self.current_place = 'parkir'
            return {
                'success': True,
                'location': self.get_current(),
                'message': f"Pindah ke Mobil. {self.get_current().deskripsi}"
            }
        
        # Public area
        for place in PublicPlace:
            if place.value in tujuan_lower:
                self.current_type = LocationType.PUBLIC
                self.current_place = place.value
                self.visit_history[place.value] = self.visit_history.get(place.value, 0) + 1
                return {
                    'success': True,
                    'location': self.get_current(),
                    'message': f"Pindah ke {self.get_current().nama}. {self.get_current().deskripsi}"
                }
        
        return {'success': False, 'message': f"Lokasi '{tujuan}' gak ditemukan."}
    
    def get_random_event(self) -> Optional[Dict]:
        """Dapatkan event random berdasarkan lokasi"""
        loc = self.get_current()
        risk = loc.risk
        chance = risk / 100
        
        import random
        if random.random() > chance:
            return None
        
        events = {
            "hampir_ketahuan": [
                "Ada suara langkah kaki mendekat! *cepat nutupin baju*",
                "Pintu terbuka sedikit! *tahan napas*",
                "Senter menyorot dari kejauhan! *merapat ke Mas*",
                "Suara orang ngobrol di deket situ! *diem, jantung berdebar*"
            ],
            "romantis": [
                "Tiba-tiba hujan rintik-rintik. *makin manis*",
                "Bulan muncul dari balik awan. *wajah Nova keceplosan cahaya*",
                "Angin sepoi-sepoi bikin suasana makin hangat.",
                "Suara musik dari kejauhan. *makin romantis*"
            ],
            "ketahuan": [
                "⚠️ ADA YANG LIAT! *cepat cabut*",
                "Pintu kebuka! Orang masuk! *langsung sembunyi*",
                "Senter nyorot tepat ke arah kita! *lari!*"
            ]
        }
        
        if risk > 70:
            event_type = random.choices(["hampir_ketahuan", "romantis", "ketahuan"], weights=[0.5, 0.2, 0.3])[0]
        elif risk > 40:
            event_type = random.choices(["hampir_ketahuan", "romantis"], weights=[0.6, 0.4])[0]
        else:
            event_type = "romantis"
        
        return {
            'type': event_type,
            'text': random.choice(events[event_type]),
            'risk_change': 10 if event_type == "hampir_ketahuan" else -5 if event_type == "romantis" else 30
        }
    
    def format_for_prompt(self) -> str:
        """Format lokasi untuk prompt AI"""
        loc = self.get_current()
        return f"""
LOKASI SAAT INI: {loc.nama}
DESKRIPSI: {loc.deskripsi}
RISK: {loc.risk}% | THRILL: {loc.thrill}%
PRIVASI: {loc.privasi}
SUASANA: {loc.suasana}
TIPS: {loc.tips}
"""


_anora_location = None


def get_anora_location() -> AnoraLocationManager:
    global _anora_location
    if _anora_location is None:
        _anora_location = AnoraLocationManager()
    return _anora_location
