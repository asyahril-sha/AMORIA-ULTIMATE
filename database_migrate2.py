# database/migrate.py

import logging

logger = logging.getLogger(__name__)


async def create_registrations_table(db):
    await db.execute("DROP TABLE IF EXISTS registrations")

    await db.execute("""
        CREATE TABLE registrations (
            id TEXT PRIMARY KEY,
            role TEXT,
            sequence INTEGER,
            status TEXT,
            created_at REAL,
            last_updated REAL,
            bot_identity TEXT,
            user_identity TEXT,
            bot_name TEXT,
            user_name TEXT,
            level INTEGER,
            total_chats INTEGER,
            stamina_bot INTEGER,
            stamina_user INTEGER,
            metadata TEXT
        )
    """)

    await db.commit()
    logger.info("✅ registrations created")


async def create_working_memory_table(db):
    await db.execute("DROP TABLE IF EXISTS working_memory")

    await db.execute("""
        CREATE TABLE working_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_id TEXT,
            user_message TEXT,
            bot_response TEXT,
            timestamp REAL
        )
    """)

    await db.commit()
    logger.info("✅ working_memory created")


async def create_long_term_memory_table(db):
    await db.execute("DROP TABLE IF EXISTS long_term_memory")

    await db.execute("""
        CREATE TABLE long_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_id TEXT,
            memory_type TEXT,
            content TEXT,
            importance REAL,
            timestamp REAL,
            status TEXT,
            emotional_tag TEXT,
            metadata TEXT
        )
    """)

    await db.commit()
    logger.info("✅ long_term_memory created")


async def create_state_tracker_table(db):
    await db.execute("DROP TABLE IF EXISTS state_tracker")

    await db.execute("""
        CREATE TABLE state_tracker (
            registration_id TEXT PRIMARY KEY,
            location_bot TEXT,
            location_user TEXT,
            updated_at REAL
        )
    """)

    await db.commit()
    logger.info("✅ state_tracker created")


async def run_migrations():
    from database.connection import get_db

    db = await get_db()

    await create_registrations_table(db)
    await create_working_memory_table(db)
    await create_long_term_memory_table(db)
    await create_state_tracker_table(db)

    logger.info("🔥 ALL TABLES READY")
