# anora/__init__.py
"""
ANORA - Virtual Human dengan Jiwa
"""

import logging
logger = logging.getLogger(__name__)

# Export version
__version__ = "1.0.0"

# Try to import components
try:
    from .core import get_anora, anora
    from .brain import get_anora_brain, anora_brain
    from .chat import get_anora_chat
    from .roles import get_anora_roles, RoleType
    from .places import get_anora_places
    from .location_manager import get_anora_location, LocationType, LocationDetail
    
    __all__ = [
        'get_anora', 'anora',
        'get_anora_brain', 'anora_brain',
        'get_anora_chat',
        'get_anora_roles', 'RoleType',
        'get_anora_places',
        'get_anora_location', 'LocationType', 'LocationDetail',
    ]
    
    logger.info("✅ ANORA modules loaded successfully")
    
except ImportError as e:
    logger.error(f"❌ ANORA import error: {e}")
    # Define dummy functions to avoid crashes
    def get_anora():
        return None
    def get_anora_brain():
        return None
    # ... etc
