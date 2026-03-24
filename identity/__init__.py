# identity/__init__.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
Identity Package - Multi-Identity System
=============================================================================
"""

from .registration import CharacterRegistration, CharacterStatus
from .manager import IdentityManager
from .bot_identity import (
    BotIdentity,
    BotPersonality,
    BotPhysicalProfile,
    BotPersonalityType,
    BotFamilyRelation
)
from .user_identity import (
    UserIdentity,
    UserPhysicalProfile,
    UserPersonality,
    UserRelationship
)

__all__ = [
    # Registration
    'CharacterRegistration',
    'CharacterStatus',
    
    # Manager
    'IdentityManager',
    
    # Bot Identity
    'BotIdentity',
    'BotPersonality',
    'BotPhysicalProfile',
    'BotPersonalityType',
    'BotFamilyRelation',
    
    # User Identity
    'UserIdentity',
    'UserPhysicalProfile',
    'UserPersonality',
    'UserRelationship',
]
