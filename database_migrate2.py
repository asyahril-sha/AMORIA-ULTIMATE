# database_migrate.py
# -*- coding: utf-8 -*-

import asyncio
import sys
import os
import logging

from config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def run_migration():
    print("=" * 60)
    print("💜 AMORIA DATABASE RESET & MIGRATION")
    print("=" * 60)

    try:
        from database.connection import init_db, close_db, get_db

        # INIT DB
        await init_db()
        print("✅ DB Connected")

        db = await get_db()

        # 🔥 HARD RESET (ANTI ERROR)
        await db.execute("DROP TABLE IF EXISTS registrations")
        await db.execute("DROP TABLE IF EXISTS working_memory")
        await db.execute("DROP TABLE IF EXISTS long_term_memory")
        await db.execute("DROP TABLE IF EXISTS state_tracker")
        await db.commit()

        print("💣 All tables dropped (clean reset)")

        # IMPORT MIGRATION
        from database.migrate import (
            create_registrations_table,
            create_working_memory_table,
            create_long_term_memory_table,
            create_state_tracker_table
        )

        # CREATE TABLES
        await create_registrations_table(db)
        await create_working_memory_table(db)
        await create_long_term_memory_table(db)
        await create_state_tracker_table(db)

        print("✅ All tables recreated")

        # VERIFY
        tables = await db.fetch_all(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )

        print("\n📋 TABLES:")
        for t in tables:
            print(f"   • {t['name']}")

        # SIZE
        db_path = settings.database.path
        if db_path.exists():
            size = db_path.stat().st_size / (1024 * 1024)
            print(f"\n📊 DB Size: {size:.2f} MB")

        print("=" * 60)
        print("✅ DATABASE READY (CLEAN)")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        try:
            from database.connection import close_db
            await close_db()
        except:
            pass


def main():
    success = asyncio.run(run_migration())
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
