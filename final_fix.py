# fix_database_final.py
# -*- coding: utf-8 -*-
"""
Final Database Fix - Menambahkan semua kolom yang hilang
"""

import sqlite3
import os
from pathlib import Path


def fix_all_tables():
    """Perbaiki semua tabel database"""
    
    print("=" * 70)
    print("💜 AMORIA - FINAL DATABASE FIX")
    print("=" * 70)
    
    # Path database untuk Railway
    db_path = Path("/app/data/amoria.db")
    
    # Buat direktori data jika belum ada
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Database path: {db_path}")
    
    try:
        # Connect ke database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        print("✅ Connected to database\n")
        
        # =========================================================
        # 1. FIX STATE_TRACKER TABLE
        # =========================================================
        print("📊 1. MEMPERBAIKI TABEL state_tracker")
        print("-" * 50)
        
        # Cek apakah tabel state_tracker ada
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='state_tracker'")
        if not cursor.fetchone():
            print("⚠️ Tabel state_tracker belum ada, membuat...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS state_tracker (
                    registration_id TEXT PRIMARY KEY,
                    location_bot TEXT,
                    location_user TEXT,
                    position_bot TEXT,
                    position_user TEXT,
                    position_relative TEXT,
                    clothing_bot_outer TEXT,
                    clothing_bot_outer_bottom TEXT,
                    clothing_bot_inner_top TEXT,
                    clothing_bot_inner_bottom TEXT,
                    clothing_user_outer TEXT,
                    clothing_user_outer_bottom TEXT,
                    clothing_user_inner_bottom TEXT,
                    clothing_history TEXT,
                    family_status TEXT,
                    family_location TEXT,
                    family_activity TEXT,
                    family_estimate_return TEXT,
                    activity_bot TEXT,
                    activity_user TEXT,
                    current_time TEXT,
                    time_override_history TEXT,
                    time_data TEXT,
                    updated_at REAL
                )
            ''')
            conn.commit()
            print("✅ Tabel state_tracker dibuat")
        
        # Cek kolom yang ada
        cursor.execute("PRAGMA table_info(state_tracker)")
        existing = [col[1] for col in cursor.fetchall()]
        
        # Kolom yang diperlukan untuk state_tracker
        state_columns = {
            'time_data': 'TEXT',
            'clothing_bot_outer_bottom': 'TEXT',
            'clothing_user_outer_bottom': 'TEXT',
            'clothing_history': 'TEXT',
            'family_status': 'TEXT',
            'family_location': 'TEXT',
            'family_activity': 'TEXT',
            'family_estimate_return': 'TEXT',
            'time_override_history': 'TEXT',
            'current_time': 'TEXT',
            'position_bot': 'TEXT',
            'position_user': 'TEXT',
            'position_relative': 'TEXT',
        }
        
        added = 0
        for col, col_type in state_columns.items():
            if col not in existing:
                try:
                    cursor.execute(f"ALTER TABLE state_tracker ADD COLUMN {col} {col_type}")
                    print(f"  ✅ Added: {col}")
                    added += 1
                except Exception as e:
                    print(f"  ⚠️ Failed: {col} - {e}")
        
        if added > 0:
            conn.commit()
            print(f"\n✅ Added {added} column(s) to state_tracker")
        else:
            print("✅ All columns already exist in state_tracker")
        
        # =========================================================
        # 2. FIX REGISTRATIONS TABLE
        # =========================================================
        print("\n📊 2. MEMPERBAIKI TABEL registrations")
        print("-" * 50)
        
        cursor.execute("PRAGMA table_info(registrations)")
        existing = [col[1] for col in cursor.fetchall()]
        
        # Kolom yang diperlukan untuk registrations
        reg_columns = {
            'weighted_memory_score': 'REAL DEFAULT 0.5',
            'weighted_memory_data': "TEXT DEFAULT '{}'",
            'emotional_bias': "TEXT DEFAULT '{}'",
            'secondary_emotion': 'TEXT',
            'secondary_arousal': 'INTEGER DEFAULT 0',
            'secondary_emotion_reason': 'TEXT',
            'physical_sensation': "TEXT DEFAULT 'biasa aja'",
            'physical_hunger': 'INTEGER DEFAULT 30',
            'physical_thirst': 'INTEGER DEFAULT 30',
            'physical_temperature': 'INTEGER DEFAULT 25',
            'stamina_bot': 'INTEGER DEFAULT 100',
            'stamina_user': 'INTEGER DEFAULT 100',
            'in_intimacy_cycle': 'BOOLEAN DEFAULT 0',
            'intimacy_cycle_count': 'INTEGER DEFAULT 0',
            'last_climax_time': 'REAL',
            'cooldown_until': 'REAL',
            'bot_identity': "TEXT DEFAULT '{}'",
            'user_identity': "TEXT DEFAULT '{}'",
            'bot_photo': 'TEXT',
            'intimacy_level': 'INTEGER DEFAULT 0',
            'emotional_state': "TEXT DEFAULT '{}'",
            'last_active': 'REAL',
        }
        
        added = 0
        for col, col_type in reg_columns.items():
            if col not in existing:
                try:
                    cursor.execute(f"ALTER TABLE registrations ADD COLUMN {col} {col_type}")
                    print(f"  ✅ Added: {col}")
                    added += 1
                except Exception as e:
                    print(f"  ⚠️ Failed: {col} - {e}")
        
        if added > 0:
            conn.commit()
            print(f"\n✅ Added {added} column(s) to registrations")
        else:
            print("✅ All columns already exist in registrations")
        
        # =========================================================
        # 3. FIX LONG_TERM_MEMORY TABLE
        # =========================================================
        print("\n📊 3. MEMPERBAIKI TABEL long_term_memory")
        print("-" * 50)
        
        # Cek apakah tabel long_term_memory ada
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='long_term_memory'")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(long_term_memory)")
            existing = [col[1] for col in cursor.fetchall()]
            
            if 'status' not in existing:
                try:
                    cursor.execute("ALTER TABLE long_term_memory ADD COLUMN status TEXT")
                    print("  ✅ Added: status")
                    added += 1
                except Exception as e:
                    print(f"  ⚠️ Failed: status - {e}")
            
            if 'emotional_tag' not in existing:
                try:
                    cursor.execute("ALTER TABLE long_term_memory ADD COLUMN emotional_tag TEXT")
                    print("  ✅ Added: emotional_tag")
                    added += 1
                except Exception as e:
                    print(f"  ⚠️ Failed: emotional_tag - {e}")
            
            if added > 0:
                conn.commit()
                print(f"\n✅ Added {added} column(s) to long_term_memory")
            else:
                print("✅ All columns already exist in long_term_memory")
        else:
            print("⚠️ Table long_term_memory not found, will be created when needed")
        
        # =========================================================
        # 4. VERIFIKASI FINAL
        # =========================================================
        print("\n📊 4. VERIFIKASI DATABASE")
        print("-" * 50)
        
        # Cek state_tracker
        cursor.execute("PRAGMA table_info(state_tracker)")
        state_cols = [col[1] for col in cursor.fetchall()]
        print(f"\nstate_tracker: {len(state_cols)} columns")
        
        if 'time_data' in state_cols:
            print("  ✅ time_data: OK")
        else:
            print("  ❌ time_data: MISSING!")
        
        # Cek registrations
        cursor.execute("PRAGMA table_info(registrations)")
        reg_cols = [col[1] for col in cursor.fetchall()]
        print(f"\nregistrations: {len(reg_cols)} columns")
        
        critical = ['weighted_memory_score', 'emotional_bias', 'secondary_emotion', 
                    'physical_sensation', 'physical_hunger', 'stamina_bot']
        for col in critical:
            if col in reg_cols:
                print(f"  ✅ {col}: OK")
            else:
                print(f"  ❌ {col}: MISSING!")
        
        # =========================================================
        # 5. DATABASE INFO
        # =========================================================
        print("\n📊 5. DATABASE INFO")
        print("-" * 50)
        
        # Hitung rows
        cursor.execute("SELECT COUNT(*) FROM registrations")
        reg_count = cursor.fetchone()[0]
        print(f"registrations: {reg_count} rows")
        
        cursor.execute("SELECT COUNT(*) FROM state_tracker")
        state_count = cursor.fetchone()[0]
        print(f"state_tracker: {state_count} rows")
        
        # Database size
        if db_path.exists():
            size_mb = db_path.stat().st_size / (1024 * 1024)
            print(f"Database size: {size_mb:.2f} MB")
        
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ DATABASE FIX COMPLETE!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = fix_all_tables()
    
    if success:
        print("\n🎉 Database siap digunakan! Bot bisa dijalankan.")
    else:
        print("\n❌ Fix gagal, periksa error di atas.")
