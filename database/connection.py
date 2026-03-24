# database/connection.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
Database Connection
=============================================================================
"""

import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from contextlib import asynccontextmanager

import aiosqlite

from config import settings

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Manajemen koneksi database SQLite
    Support async operations dengan connection pooling
    """
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.pool_size = getattr(settings.database, 'pool_size', 5)
        self.timeout = getattr(settings.database, 'timeout', 30)
        self._connection: Optional[aiosqlite.Connection] = None
        self._initialized = False
        self._in_transaction = False
        
    async def initialize(self):
        """Initialize database and create tables"""
        try:
            # Buat directory jika belum ada
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Koneksi pertama untuk setup
            self._connection = await aiosqlite.connect(
                str(self.db_path),
                timeout=self.timeout
            )
            
            # Enable foreign keys
            await self._connection.execute("PRAGMA foreign_keys = ON")
            
            # Optimize SQLite for performance
            await self._connection.execute("PRAGMA journal_mode = WAL")
            await self._connection.execute("PRAGMA synchronous = NORMAL")
            await self._connection.execute("PRAGMA cache_size = 10000")
            await self._connection.execute("PRAGMA temp_store = MEMORY")
            await self._connection.execute("PRAGMA busy_timeout = 5000")
            
            self._initialized = True
            logger.info(f"✅ Database initialized at {self.db_path}")
            
            # Create tables after connection
            await self._create_tables()
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    async def _create_tables(self):
        """Create all database tables with complete columns"""
        
        # ===== REGISTRATIONS TABLE (Complete - 43 columns) =====
        await self._connection.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                -- Primary & Basic Info (6)
                id TEXT PRIMARY KEY,
                role TEXT NOT NULL,
                sequence INTEGER NOT NULL,
                status TEXT DEFAULT 'active',
                created_at REAL NOT NULL,
                last_updated REAL NOT NULL,
                
                -- Identity (2)
                bot_identity TEXT DEFAULT '{}',
                user_identity TEXT DEFAULT '{}',
                
                -- Bot Physical (7)
                bot_name TEXT NOT NULL,
                bot_age INTEGER,
                bot_height INTEGER,
                bot_weight INTEGER,
                bot_chest TEXT,
                bot_hijab BOOLEAN DEFAULT 0,
                bot_photo TEXT,
                
                -- User Physical (7)
                user_name TEXT NOT NULL,
                user_status TEXT DEFAULT 'lajang',
                user_age INTEGER,
                user_height INTEGER,
                user_weight INTEGER,
                user_penis INTEGER,
                user_artist_ref TEXT,
                
                -- Stats & Progression (7)
                level INTEGER DEFAULT 1,
                total_chats INTEGER DEFAULT 0,
                total_climax_bot INTEGER DEFAULT 0,
                total_climax_user INTEGER DEFAULT 0,
                stamina_bot INTEGER DEFAULT 100,
                stamina_user INTEGER DEFAULT 100,
                total_interactions INTEGER DEFAULT 0,
                
                -- Intimacy System (5)
                in_intimacy_cycle BOOLEAN DEFAULT 0,
                intimacy_cycle_count INTEGER DEFAULT 0,
                intimacy_level INTEGER DEFAULT 0,
                last_climax_time REAL,
                cooldown_until REAL,
                
                -- Memory & Emotion (4)
                weighted_memory_score REAL DEFAULT 0.5,
                weighted_memory_data TEXT DEFAULT '{}',
                emotional_bias TEXT DEFAULT '{}',
                emotional_state TEXT DEFAULT '{}',
                
                -- Secondary Emotion (3)
                secondary_emotion TEXT,
                secondary_arousal INTEGER DEFAULT 0,
                secondary_emotion_reason TEXT,
                
                -- Physical State (4)
                physical_sensation TEXT DEFAULT 'biasa aja',
                physical_hunger INTEGER DEFAULT 30,
                physical_thirst INTEGER DEFAULT 30,
                physical_temperature INTEGER DEFAULT 25,
                
                -- Environment & Meta (3)
                current_location TEXT,
                metadata TEXT DEFAULT '{}',
                last_active REAL
            )
        ''')
        
        # ===== WORKING MEMORY TABLE =====
        await self._connection.execute('''
            CREATE TABLE IF NOT EXISTS working_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                registration_id TEXT NOT NULL,
                chat_index INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                user_message TEXT,
                bot_response TEXT,
                context TEXT,
                FOREIGN KEY (registration_id) REFERENCES registrations(id) ON DELETE CASCADE
            )
        ''')
        
        # ===== LONG TERM MEMORY TABLE =====
        await self._connection.execute('''
            CREATE TABLE IF NOT EXISTS long_term_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                registration_id TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                content TEXT NOT NULL,
                importance REAL DEFAULT 0.5,
                timestamp REAL NOT NULL,
                status TEXT,
                emotional_tag TEXT,
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (registration_id) REFERENCES registrations(id) ON DELETE CASCADE
            )
        ''')
        
        # ===== STATE TRACKER TABLE (Complete) =====
        await self._connection.execute('''
            CREATE TABLE IF NOT EXISTS state_tracker (
                registration_id TEXT PRIMARY KEY,
                
                -- Location & Position
                location_bot TEXT,
                location_user TEXT,
                position_bot TEXT,
                position_user TEXT,
                position_relative TEXT,
                
                -- Clothing (complete)
                clothing_bot_outer TEXT,
                clothing_bot_outer_bottom TEXT,
                clothing_bot_inner_top TEXT,
                clothing_bot_inner_bottom TEXT,
                clothing_user_outer TEXT,
                clothing_user_outer_bottom TEXT,
                clothing_user_inner_bottom TEXT,
                clothing_history TEXT,
                
                -- Family State
                family_status TEXT,
                family_location TEXT,
                family_activity TEXT,
                family_estimate_return TEXT,
                
                -- Activity
                activity_bot TEXT,
                activity_user TEXT,
                
                -- Emotion & Arousal
                emotion_bot TEXT,
                arousal_bot INTEGER DEFAULT 0,
                mood_bot TEXT,
                emotion_user TEXT,
                arousal_user INTEGER DEFAULT 0,
                
                -- Time
                current_time TEXT,
                time_override_history TEXT DEFAULT '[]',
                
                updated_at REAL NOT NULL,
                FOREIGN KEY (registration_id) REFERENCES registrations(id) ON DELETE CASCADE
            )
        ''')
        
        # ===== BACKUPS TABLE =====
        await self._connection.execute('''
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                size INTEGER,
                created_at REAL NOT NULL,
                type TEXT DEFAULT 'auto',
                status TEXT DEFAULT 'completed',
                metadata TEXT DEFAULT '{}'
            )
        ''')
        
        # ===== INDEXES =====
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_registrations_role ON registrations(role, status)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_registrations_updated ON registrations(last_updated)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_registrations_level ON registrations(level)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_registrations_status ON registrations(status)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_working_memory_reg ON working_memory(registration_id)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_working_memory_chat ON working_memory(registration_id, chat_index)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_long_term_memory_reg ON long_term_memory(registration_id, memory_type)")
        await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_state_tracker_updated ON state_tracker(updated_at)")
        
        await self._connection.commit()
        logger.info("✅ Database tables created with complete schema")
        
        # Verify tables
        await self._verify_tables()
    
    async def _verify_tables(self):
        """Verify tables have correct columns"""
        # Check registrations table
        cursor = await self._connection.execute("PRAGMA table_info(registrations)")
        columns = await cursor.fetchall()
        col_names = [col[1] for col in columns]
        
        required_columns = [
            'weighted_memory_score', 'weighted_memory_data', 'emotional_bias',
            'stamina_bot', 'stamina_user', 'in_intimacy_cycle'
        ]
        
        missing = [col for col in required_columns if col not in col_names]
        
        if missing:
            logger.warning(f"⚠️ Missing columns in registrations: {missing}")
            # Add missing columns
            for col in missing:
                await self._add_column('registrations', col)
        
        # Check state_tracker table
        cursor = await self._connection.execute("PRAGMA table_info(state_tracker)")
        columns = await cursor.fetchall()
        col_names = [col[1] for col in columns]
        
        required_state = ['clothing_bot_outer_bottom', 'family_status', 'time_override_history']
        missing_state = [col for col in required_state if col not in col_names]
        
        if missing_state:
            logger.warning(f"⚠️ Missing columns in state_tracker: {missing_state}")
            for col in missing_state:
                await self._add_column('state_tracker', col)
        
        await self._connection.commit()
    
    async def _add_column(self, table: str, column: str, definition: str = None):
        """Add column if not exists"""
        definitions = {
            'weighted_memory_score': "REAL DEFAULT 0.5",
            'weighted_memory_data': "TEXT DEFAULT '{}'",
            'emotional_bias': "TEXT DEFAULT '{}'",
            'stamina_bot': "INTEGER DEFAULT 100",
            'stamina_user': "INTEGER DEFAULT 100",
            'in_intimacy_cycle': "BOOLEAN DEFAULT 0",
            'intimacy_cycle_count': "INTEGER DEFAULT 0",
            'last_climax_time': "REAL",
            'cooldown_until': "REAL",
            'bot_identity': "TEXT DEFAULT '{}'",
            'user_identity': "TEXT DEFAULT '{}'",
            'clothing_bot_outer_bottom': "TEXT",
            'family_status': "TEXT",
            'time_override_history': "TEXT DEFAULT '[]'",
            'clothing_history': "TEXT",
        }
        
        if definition is None:
            definition = definitions.get(column, "TEXT")
        
        try:
            await self._connection.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
            logger.info(f"  ✅ Added column: {table}.{column}")
        except Exception as e:
            if "duplicate column" not in str(e).lower():
                logger.warning(f"  ⚠️ Could not add {table}.{column}: {e}")
    
    async def execute(self, query: str, params: tuple = ()) -> aiosqlite.Cursor:
        """Execute query and return cursor"""
        if not self._connection:
            await self.initialize()
        
        cursor = await self._connection.execute(query, params)
        return cursor
    
    async def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch one row as dict"""
        if not self._connection:
            await self.initialize()
        
        self._connection.row_factory = aiosqlite.Row
        cursor = await self._connection.execute(query, params)
        row = await cursor.fetchone()
        return dict(row) if row else None
    
    async def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch all rows as list of dicts"""
        if not self._connection:
            await self.initialize()
        
        self._connection.row_factory = aiosqlite.Row
        cursor = await self._connection.execute(query, params)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    
    async def commit(self):
        """Commit current transaction"""
        if not self._connection:
            await self.initialize()
        
        try:
            await self._connection.commit()
            self._in_transaction = False
            logger.debug("Transaction committed")
        except Exception as e:
            logger.error(f"Commit error: {e}")
            raise
    
    async def rollback(self):
        """Rollback current transaction"""
        if not self._connection:
            await self.initialize()
        
        try:
            await self._connection.rollback()
            self._in_transaction = False
            logger.debug("Transaction rolled back")
        except Exception as e:
            logger.error(f"Rollback error: {e}")
            raise
    
    async def execute_many(self, query: str, params_list: List[tuple]):
        """Execute many inserts/updates"""
        if not self._connection:
            await self.initialize()
        
        await self._connection.executemany(query, params_list)
        await self.commit()
    
    async def vacuum(self):
        """Vacuum database (optimize)"""
        if not self._connection:
            await self.initialize()
        
        await self._connection.execute("VACUUM")
        logger.info("✅ Database vacuum completed")
    
    async def backup(self, backup_path: Path) -> bool:
        """Backup database to file"""
        try:
            if not self._connection:
                await self.initialize()
            
            backup_conn = await aiosqlite.connect(str(backup_path))
            await self._connection.backup(backup_conn)
            await backup_conn.close()
            
            logger.info(f"✅ Database backed up to {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False
    
    async def get_stats(self) -> Dict:
        """Get database statistics"""
        stats = {}
        
        tables = ['registrations', 'working_memory', 'long_term_memory', 'state_tracker']
        
        for table in tables:
            try:
                result = await self.fetch_one(f"SELECT COUNT(*) as count FROM {table}")
                stats[f"{table}_count"] = result['count'] if result else 0
            except:
                stats[f"{table}_count"] = 0
        
        # Active registrations
        active = await self.fetch_one(
            "SELECT COUNT(*) as count FROM registrations WHERE status = 'active'"
        )
        stats['active_registrations'] = active['count'] if active else 0
        
        # Total chats
        total_chats = await self.fetch_one(
            "SELECT SUM(total_chats) as total FROM registrations"
        )
        stats['total_chats_all_time'] = total_chats['total'] if total_chats and total_chats['total'] else 0
        
        # Database size
        if self.db_path.exists():
            stats['db_size_mb'] = round(self.db_path.stat().st_size / (1024 * 1024), 2)
        else:
            stats['db_size_mb'] = 0
            
        return stats
    
    async def close(self):
        """Close database connection"""
        if self._connection:
            await self._connection.close()
            self._connection = None
            self._initialized = False
            logger.info("📁 Database connection closed")
    
    @asynccontextmanager
    async def transaction(self):
        """Context manager for transactions"""
        if not self._connection:
            await self.initialize()
        
        try:
            await self._connection.execute("BEGIN")
            self._in_transaction = True
            yield self
            await self.commit()
        except Exception as e:
            await self.rollback()
            raise


# =============================================================================
# GLOBAL DATABASE INSTANCE
# =============================================================================

_db_instance: Optional[DatabaseConnection] = None


async def get_db() -> DatabaseConnection:
    """Get global database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseConnection(settings.database.path)
        await _db_instance.initialize()
    return _db_instance


async def init_db():
    """Initialize database (for startup)"""
    db = await get_db()
    return db


async def close_db():
    """Close global database connection"""
    global _db_instance
    if _db_instance:
        await _db_instance.close()
        _db_instance = None
        logger.info("📁 Global database connection closed")


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

async def execute_sql(sql: str, params: tuple = ()) -> aiosqlite.Cursor:
    """Execute raw SQL (for migrations)"""
    db = await get_db()
    return await db.execute(sql, params)


async def fetch_all_sql(sql: str, params: tuple = ()) -> List[Dict]:
    """Fetch all rows from raw SQL"""
    db = await get_db()
    return await db.fetch_all(sql, params)


async def fetch_one_sql(sql: str, params: tuple = ()) -> Optional[Dict]:
    """Fetch one row from raw SQL"""
    db = await get_db()
    return await db.fetch_one(sql, params)


__all__ = [
    'DatabaseConnection',
    'get_db',
    'init_db',
    'close_db',
    'execute_sql',
    'fetch_all_sql',
    'fetch_one_sql',
]
