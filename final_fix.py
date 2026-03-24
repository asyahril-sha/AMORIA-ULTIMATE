# fix_database_final.py
# -*- coding: utf-8 -*-
"""
Final Database Fix - Membuat semua tabel dan kolom yang hilang
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
        # 1. BUAT TABEL REGISTRATIONS (jika belum ada)
        # =========================================================
        print("📊 1. MEMBUAT/MEMPERBAIKI TABEL registrations")
        print("-" * 50)
        
        # Buat tabel registrations dengan semua kolom
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                id TEXT PRIMARY KEY,
                role TEXT NOT NULL,
                sequence INTEGER NOT NULL,
                status TEXT DEFAULT 'active',
                created_at REAL NOT NULL,
                last_updated REAL NOT NULL,
                
                -- Identity
                bot_identity TEXT DEFAULT '{}',
                user_identity TEXT DEFAULT '{}',
                
                -- Bot Physical
                bot_name TEXT NOT NULL,
                bot_age INTEGER,
                bot_height INTEGER,
                bot_weight INTEGER,
                bot_chest TEXT,
                bot_hijab BOOLEAN DEFAULT 0,
                bot_photo TEXT,
                
                -- User Physical
                user_name TEXT NOT NULL,
                user_status TEXT DEFAULT 'lajang',
                user_age INTEGER,
                user_height INTEGER,
                user_weight INTEGER,
                user_penis INTEGER,
                user_artist_ref TEXT,
                
                -- Stats & Progression
                level INTEGER DEFAULT 1,
                total_chats INTEGER DEFAULT 0,
                total_climax_bot INTEGER DEFAULT 0,
                total_climax_user INTEGER DEFAULT 0,
                stamina_bot INTEGER DEFAULT 100,
                stamina_user INTEGER DEFAULT 100,
                
                -- Intimacy System
                in_intimacy_cycle BOOLEAN DEFAULT 0,
                intimacy_cycle_count INTEGER DEFAULT 0,
                intimacy_level INTEGER DEFAULT 0,
                last_climax_time REAL,
                cooldown_until REAL,
                
                -- Memory & Emotion
                weighted_memory_score REAL DEFAULT 0.5,
                weighted_memory_data TEXT DEFAULT '{}',
                emotional_bias TEXT DEFAULT '{}',
                emotional_state TEXT DEFAULT '{}',
                
                -- Secondary Emotion
                secondary_emotion TEXT,
                secondary_arousal INTEGER DEFAULT 0,
                secondary_emotion_reason TEXT,
                
                -- Physical State
                physical_sensation TEXT DEFAULT 'biasa aja',
                physical_hunger INTEGER DEFAULT 30,
                physical_thirst INTEGER DEFAULT 30,
                physical_temperature INTEGER DEFAULT 25,
                
                -- Meta
                metadata TEXT DEFAULT '{}',
                last_active REAL
            )
        ''')
        print("✅ Tabel registrations dibuat/diperiksa")
        
        # =========================================================
        # 2. BUAT TABEL WORKING_MEMORY
        # =========================================================
        print("\n📊 2. MEMBUAT TABEL working_memory")
        print("-" * 50)
        
        cursor.execute('''
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
        print("✅ Tabel working_memory dibuat/diperiksa")
        
        # =========================================================
        # 3. BUAT TABEL LONG_TERM_MEMORY
        # =========================================================
        print("\n📊 3. MEMBUAT TABEL long_term_memory")
        print("-" * 50)
        
        cursor.execute('''
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
        print("✅ Tabel long_term_memory dibuat/diperiksa")
        
        # =========================================================
        # 4. BUAT TABEL STATE_TRACKER (jika belum ada)
        # =========================================================
        print("\n📊 4. MEMBUAT/MEMPERBAIKI TABEL state_tracker")
        print("-" * 50)
        
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
                updated_at REAL,
                FOREIGN KEY (registration_id) REFERENCES registrations(id) ON DELETE CASCADE
            )
        ''')
        print("✅ Tabel state_tracker dibuat/diperiksa")
        
        # =========================================================
        # 5. BUAT TABEL BACKUPS
        # =========================================================
        print("\n📊 5. MEMBUAT TABEL backups")
        print("-" * 50)
        
        cursor.execute('''
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
        print("✅ Tabel backups dibuat/diperiksa")
        
        # =========================================================
        # 6. BUAT INDEXES
        # =========================================================
        print("\n📊 6. MEMBUAT INDEXES")
        print("-" * 50)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_registrations_role ON registrations(role, status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_registrations_updated ON registrations(last_updated)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_working_memory_reg ON working_memory(registration_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_state_tracker_updated ON state_tracker(updated_at)")
        print("✅ Indexes dibuat")
        
        conn.commit()
        
        # =========================================================
        # 7. VERIFIKASI FINAL
        # =========================================================
        print("\n📊 7. VERIFIKASI DATABASE")
        print("-" * 50)
        
        # Cek semua tabel
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print("\n📋 TABEL YANG ADA:")
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table[0]})")
            cols = cursor.fetchall()
            print(f"   ✅ {table[0]}: {len(cols)} columns")
        
        # Cek registrations critical columns
        cursor.execute("PRAGMA table_info(registrations)")
        reg_cols = [col[1] for col in cursor.fetchall()]
        
        print("\n📋 REGISTRATIONS CRITICAL COLUMNS:")
        critical = ['weighted_memory_score', 'emotional_bias', 'secondary_emotion', 
                    'physical_sensation', 'stamina_bot', 'in_intimacy_cycle']
        for col in critical:
            if col in reg_cols:
                print(f"   ✅ {col}")
            else:
                print(f"   ❌ {col} - MISSING!")
        
        # Cek state_tracker
        cursor.execute("PRAGMA table_info(state_tracker)")
        state_cols = [col[1] for col in cursor.fetchall()]
        
        print("\n📋 STATE_TRACKER CRITICAL COLUMNS:")
        if 'time_data' in state_cols:
            print("   ✅ time_data")
        else:
            print("   ❌ time_data - MISSING!")
        
        # =========================================================
        # 8. DATABASE INFO
        # =========================================================
        print("\n📊 8. DATABASE INFO")
        print("-" * 50)
        
        cursor.execute("SELECT COUNT(*) FROM registrations")
        reg_count = cursor.fetchone()[0]
        print(f"registrations: {reg_count} rows")
        
        cursor.execute("SELECT COUNT(*) FROM state_tracker")
        state_count = cursor.fetchone()[0]
        print(f"state_tracker: {state_count} rows")
        
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
