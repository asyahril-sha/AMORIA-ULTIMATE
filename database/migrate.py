# database/migrate.py
# -*- coding: utf-8 -*-

import logging
from database.connection import get_db

logger = logging.getLogger(__name__)


# =========================================================
# CREATE TABLES (SAFE - NO DROP)
# =========================================================

async def create_registrations_table(db):
    await db.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id TEXT PRIMARY KEY,
        role TEXT,
        sequence INTEGER,
        status TEXT DEFAULT 'active',
        created_at REAL,
        last_updated REAL,

        bot_name TEXT,
        user_name TEXT,

        level INTEGER DEFAULT 1,
        total_chats INTEGER DEFAULT 0,

        metadata TEXT DEFAULT '{}'
    )
    """)


async def create_working_memory_table(db):
    await db.execute("""
    CREATE TABLE IF NOT EXISTS working_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registration_id TEXT,
        chat_index INTEGER,
        timestamp REAL,
        user_message TEXT,
        bot_response TEXT,
        context TEXT
    )
    """)


async def create_long_term_memory_table(db):
    await db.execute("""
    CREATE TABLE IF NOT EXISTS long_term_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registration_id TEXT,
        memory_type TEXT,
        content TEXT,
        importance REAL DEFAULT 0.5,
        timestamp REAL,
        status TEXT,
        emotional_tag TEXT,
        metadata TEXT DEFAULT '{}'
    )
    """)


async def create_state_tracker_table(db):
    await db.execute("""
    CREATE TABLE IF NOT EXISTS state_tracker (
        registration_id TEXT PRIMARY KEY,

        location_bot TEXT,
        location_user TEXT,

        activity_bot TEXT,
        activity_user TEXT,

        updated_at REAL
    )
    """)


async def create_backups_table(db):
    await db.execute("""
    CREATE TABLE IF NOT EXISTS backups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        size INTEGER,
        created_at REAL,
        type TEXT DEFAULT 'auto',
        status TEXT DEFAULT 'completed'
    )
    """)


# =========================================================
# ADD MISSING COLUMNS (SAFE MIGRATION)
# =========================================================

async def fix_missing_columns(db):
    try:
        columns = await db.fetch_all("PRAGMA table_info(registrations)")
        existing = [col["name"] for col in columns]

        needed = {
            "bot_identity": "TEXT",
            "user_identity": "TEXT",
            "stamina_bot": "INTEGER DEFAULT 100",
            "stamina_user": "INTEGER DEFAULT 100",
            "physical_sensation": "TEXT",
            "physical_hunger": "INTEGER DEFAULT 30",
        }

        for col, definition in needed.items():
            if col not in existing:
                try:
                    await db.execute(f"ALTER TABLE registrations ADD COLUMN {col} {definition}")
                    logger.info(f"✅ Added column: {col}")
                except Exception as e:
                    logger.warning(f"⚠️ Failed add column {col}: {e}")

    except Exception as e:
        logger.warning(f"⚠️ Column migration skipped: {e}")


# =========================================================
# INDEXES (OPTIONAL)
# =========================================================

async def create_indexes(db):
    try:
        await db.execute("CREATE INDEX IF NOT EXISTS idx_registrations_role ON registrations(role)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_memory_reg ON working_memory(registration_id)")
    except Exception as e:
        logger.warning(f"⚠️ Index creation skipped: {e}")


# =========================================================
# MAIN MIGRATION
# =========================================================

async def run_migrations():
    logger.info("=" * 60)
    logger.info("🚀 SQLITE SAFE MIGRATION")
    logger.info("=" * 60)

    try:
        db = await get_db()

        # Create tables
        await create_registrations_table(db)
        await create_working_memory_table(db)
        await create_long_term_memory_table(db)
        await create_state_tracker_table(db)
        await create_backups_table(db)

        # Index
        await create_indexes(db)

        # Fix columns
        await fix_missing_columns(db)

        # VERIFY
        tables = await db.fetch_all(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        table_names = [t["name"] for t in tables]

        logger.info("\n📊 TABLES:")
        for table in sorted(table_names):
            try:
                count = await db.fetch_one(f"SELECT COUNT(*) as count FROM {table}")
                row_count = count["count"] if count else 0
                logger.info(f"   • {table}: {row_count} rows")
            except Exception as e:
                logger.warning(f"⚠️ Could not read {table}: {e}")

        logger.info("=" * 60)
        logger.info("✅ Migration Complete")
        logger.info("=" * 60)

        return True

    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        return False


# =========================================================
# EXPORT (WAJIB ADA BIAR GAK ERROR IMPORT)
# =========================================================

async def migrate():
    return await run_migrations()
