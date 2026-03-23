# references/gesture_db.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
Gesture Reference - Database Referensi Gesture (Bukan Template)
=============================================================================
"""

import random
from typing import Dict, List, Optional


POSITION_GESTURES = {
    'duduk_di_antara_kaki': {
        'description': 'Duduk di antara kaki user',
        'gestures': [
            "*membelai lembut paha user dengan ujung jari*",
            "*menatap ke atas ke arah user sambil tersenyum*",
            "*menyandarkan kepala di dada user*",
            "*tangan meraih tangan user, menggenggam erat*",
            "*mendekatkan wajah, napas terasa hangat*"
        ]
    },
    'duduk_di_pangkuan': {
        'description': 'Duduk di pangkuan user',
        'gestures': [
            "*memeluk leher user*",
            "*menyandarkan kepala di bahu user*",
            "*mencium pipi user cepat*",
            "*memainkan rambut user*",
            "*berbisik di telinga user*"
        ]
    },
    'di_belakang': {
        'description': 'Di belakang user',
        'gestures': [
            "*memeluk user dari belakang*",
            "*mencium bahu user pelan*",
            "*berbisik di telinga user*",
            "*menyandarkan dagu di bahu user*"
        ]
    },
    'bersebelahan': {
        'description': 'Bersebelahan dengan user',
        'gestures': [
            "*menyandarkan kepala ke bahu user*",
            "*menggenggam tangan user*",
            "*mencolek pinggang user*",
            "*mengusap punggung tangan user*"
        ]
    },
    'berhadapan': {
        'description': 'Berhadapan dengan user',
        'gestures': [
            "*menatap mata user dalam-dalam*",
            "*mengusap pipi user*",
            "*mencium kening user*",
            "*mendekatkan wajah*"
        ]
    }
}


ACTIVITY_GESTURES = {
    'memijat': {
        'gestures': [
            "*jari-jari menekan lembut punggung*",
            "*ibu jari menguleni area yang tegang*",
            "*tangan bergerak lambat*",
            "*jari-jari merambat ke area sensitif*"
        ]
    },
    'nonton_film': {
        'gestures': [
            "*mata tertuju pada layar, sesekali melirik*",
            "*tersenyum kecil*",
            "*menutup mata saat adegan serem*",
            "*tanpa sadar tubuh bergeser lebih dekat*"
        ]
    },
    'masak_bareng': {
        'gestures': [
            "*berdiri di samping, tangan bersentuhan*",
            "*meminta user mengajari*",
            "*sengaja menyenggol user*",
            "*melihat user dengan mata berbinar*"
        ]
    }
}


EMOTION_GESTURES = {
    'malu': [
        "*menunduk, pipi memerah*",
        "*memainkan ujung baju*",
        "*menutup wajah dengan tangan*",
        "*menatap ke samping*"
    ],
    'berani': [
        "*menatap langsung ke mata user*",
        "*mendekat, mengambil inisiatif*",
        "*tersenyum genit*",
        "*menyentuh user lebih lama*"
    ],
    'horny': [
        "*napas memburu, dada naik turun*",
        "*tangan gemetar saat menyentuh*",
        "*menggigit bibir*",
        "*tubuh bergeser lebih dekat*"
    ],
    'climax': [
        "*tubuh gemetar hebat*",
        "*mata terpejam rapat*",
        "*suara erangan tertahan*",
        "*badan lemas, bersandar*"
    ],
    'lemas': [
        "*badan lemas, bersandar*",
        "*mata setengah terpejam*",
        "*tangan masih gemetar kecil*",
        "*tersenyum lemas*"
    ],
    'senang': [
        "*tersenyum lebar*",
        "*melompat kecil*",
        "*memeluk user erat*",
        "*tertawa kecil*"
    ]
}


AROUSAL_GESTURES = {
    'very_low': ["*santai, bersandar*", "*tersenyum biasa*", "*melihat sekeliling*"],
    'low': ["*mulai deg-degan*", "*memainkan rambut*", "*melirik user sekilas*"],
    'medium': ["*jantung berdebar*", "*pipi merona*", "*mendekat perlahan*"],
    'high': ["*napas memburu*", "*tangan gemetar*", "*tubuh bergeser*"],
    'very_high': ["*napas tersengal*", "*tubuh gemetar*", "*tangan mencengkeram*"]
}


SPECIAL_SITUATION_GESTURES = {
    'pertama_kali_sentuh': [
        "*tubuh menegang, napas tertahan*",
        "*mata membelalak, kaget*",
        "*pipi memerah, menunduk*"
    ],
    'kaget_ketahuan': [
        "*membeku, tidak bergerak*",
        "*cepat menjauh, pura-pura sibuk*",
        "*berbisik panik, 'cepat!'*"
    ],
    'usai_intim': [
        "*badan lemas, bersandar*",
        "*tersenyum puas*",
        "*memeluk erat, tidak mau lepas*"
    ]
}


def get_gesture(position: str = None, activity: str = None, emotion: str = None, arousal: int = None) -> str:
    """Dapatkan gesture berdasarkan kombinasi situasi"""
    if arousal is not None:
        if arousal >= 80:
            level = 'very_high'
        elif arousal >= 60:
            level = 'high'
        elif arousal >= 40:
            level = 'medium'
        elif arousal >= 20:
            level = 'low'
        else:
            level = 'very_low'
        gestures = AROUSAL_GESTURES.get(level, [])
        if gestures:
            return random.choice(gestures)
    
    if position and position in POSITION_GESTURES:
        gestures = POSITION_GESTURES[position]['gestures']
        if gestures:
            return random.choice(gestures)
    
    if activity and activity in ACTIVITY_GESTURES:
        gestures = ACTIVITY_GESTURES[activity]['gestures']
        if gestures:
            return random.choice(gestures)
    
    if emotion and emotion in EMOTION_GESTURES:
        gestures = EMOTION_GESTURES[emotion]
        if gestures:
            return random.choice(gestures)
    
    default_gestures = ["*tersenyum kecil*", "*menatap user*", "*mendekat sedikit*", "*menghela napas*"]
    return random.choice(default_gestures)


def get_gesture_by_combination(position: str = None, activity: str = None, emotion: str = None, arousal: int = None) -> str:
    return get_gesture(position, activity, emotion, arousal)


def get_random_gesture() -> str:
    all_gestures = []
    for pos in POSITION_GESTURES.values():
        all_gestures.extend(pos['gestures'])
    for act in ACTIVITY_GESTURES.values():
        all_gestures.extend(act['gestures'])
    for emo in EMOTION_GESTURES.values():
        all_gestures.extend(emo)
    for aro in AROUSAL_GESTURES.values():
        all_gestures.extend(aro)
    for sp in SPECIAL_SITUATION_GESTURES.values():
        all_gestures.extend(sp)
    return random.choice(all_gestures) if all_gestures else "*tersenyum kecil*"


__all__ = [
    'POSITION_GESTURES',
    'ACTIVITY_GESTURES',
    'EMOTION_GESTURES',
    'AROUSAL_GESTURES',
    'SPECIAL_SITUATION_GESTURES',
    'get_gesture',
    'get_gesture_by_combination',
    'get_random_gesture'
]
