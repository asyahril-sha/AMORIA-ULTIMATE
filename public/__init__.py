# public/__init__.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
Public Package - Public Areas for Intimacy
Compatible with AMORIA methods:
- Chat-based leveling (1-12)
- Weighted memory
- Emotional flow
- Spatial awareness
=============================================================================
"""

from .locations import PublicLocations, Location, LocationCategory
from .risk import RiskCalculator
from .thrill import ThrillSystem
from .auto_select import LocationAutoSelector
from .events import RandomEvents
from .area_manager import AreaManager

__all__ = [
    'PublicLocations',
    'Location',
    'LocationCategory',
    'RiskCalculator',
    'ThrillSystem',
    'LocationAutoSelector',
    'RandomEvents',
    'AreaManager',
]
