# references/__init__.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
References Package - Database Referensi (Bukan Template)
=============================================================================
"""

from .artists import (
    ARTIS_INDONESIA_NON_HIJAB,
    ARTIS_INDONESIA_HIJAB,
    ARTIS_INTERNASIONAL_NON_HIJAB,
    ARTIS_INTERNASIONAL_HIJAB,
    ALL_ARTIS,
    ROLE_REFERENCES,
    get_random_artist_for_role,
    get_artist_by_name,
    format_artist_description,
    get_artist_by_popularity
)

from .positions import (
    PositionDatabase,
    get_position_database,
    DifficultyLevel,
    IntensityLevel
)

from .areas import (
    AreaDatabase,
    AreaCategory,
    get_area_database
)

from .climax import (
    ClimaxDatabase,
    ClimaxIntensity,
    ClimaxType,
    get_climax_database
)

from .gesture_db import (
    POSITION_GESTURES,
    ACTIVITY_GESTURES,
    EMOTION_GESTURES,
    AROUSAL_GESTURES,
    SPECIAL_SITUATION_GESTURES,
    get_gesture,
    get_gesture_by_combination,
    get_random_gesture
)

from .role_config import (
    IPAR_CONFIG,
    TEMAN_KANTOR_CONFIG,
    JANDA_CONFIG,
    PELAKOR_CONFIG,
    ISTRI_ORANG_CONFIG,
    PDKT_CONFIG,
    SEPUPU_CONFIG,
    TEMAN_SMA_CONFIG,
    MANTAN_CONFIG,
    get_role_config,
    get_all_role_names
)

__all__ = [
    # Artists
    'ARTIS_INDONESIA_NON_HIJAB',
    'ARTIS_INDONESIA_HIJAB',
    'ARTIS_INTERNASIONAL_NON_HIJAB',
    'ARTIS_INTERNASIONAL_HIJAB',
    'ALL_ARTIS',
    'ROLE_REFERENCES',
    'get_random_artist_for_role',
    'get_artist_by_name',
    'format_artist_description',
    'get_artist_by_popularity',
    
    # Positions
    'PositionDatabase',
    'get_position_database',
    'DifficultyLevel',
    'IntensityLevel',
    
    # Areas
    'AreaDatabase',
    'AreaCategory',
    'get_area_database',
    
    # Climax
    'ClimaxDatabase',
    'ClimaxIntensity',
    'ClimaxType',
    'get_climax_database',
    
    # Gestures
    'POSITION_GESTURES',
    'ACTIVITY_GESTURES',
    'EMOTION_GESTURES',
    'AROUSAL_GESTURES',
    'SPECIAL_SITUATION_GESTURES',
    'get_gesture',
    'get_gesture_by_combination',
    'get_random_gesture',
    
    # Role Config
    'IPAR_CONFIG',
    'TEMAN_KANTOR_CONFIG',
    'JANDA_CONFIG',
    'PELAKOR_CONFIG',
    'ISTRI_ORANG_CONFIG',
    'PDKT_CONFIG',
    'SEPUPU_CONFIG',
    'TEMAN_SMA_CONFIG',
    'MANTAN_CONFIG',
    'get_role_config',
    'get_all_role_names',
]
