# identity/__init__.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
Identity Package - Multi-Identity System
=============================================================================
"""

from .registration import CharacterRegistration, CharacterStatus, BotIdentity, UserIdentity
from .manager import IdentityManager
from .user_identity import UserPhysicalProfile, UserPersonality, UserRelationship, UserIdentity
from .bot_identity import BotPersonalityType, BotPhysicalProfile, BotPersonality, BotFamilyRelation, BotIdentity

__all__ = [
    'CharacterRegistration',
    'CharacterStatus',
    'BotIdentity',
    'UserIdentity',
    'IdentityManager',
    'UserPhysicalProfile',
    'UserPersonality',
    'UserRelationship',
    'BotPersonalityType',
    'BotPhysicalProfile',
    'BotPersonality',
    'BotFamilyRelation',
]
