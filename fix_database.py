# fix_time_data.py
# -*- coding: utf-8 -*-
"""
Fix script untuk menambahkan kolom time_data ke tabel state_tracker
"""

import asyncio
import sys
import sqlite3
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


async def fix_time_data_column():
    """Tambahkan kolom time_data ke tabel state_tracker"""
    
    print("=" * 60)
    print("🔧 FIX: Adding time_data column to state_tracker")
    print("=" * 60)
    
    try:
        # Path database
        db_path = Path("data/amoria.db")
        
        if not db_path.exists():
            print(f"❌ Database not found at {db_path}")
            return False
        
        print(f"📁 Database: {db_path}")
        
        # Connect langsung dengan sqlite3
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Cek apakah kolom time_data sudah ada
        cursor.execute("PRAGMA table_info(state_tracker)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'time_data' in columns:
            print("✅ Kolom time_data sudah ada")
            conn.close()
            return True
        
        # Tambahkan kolom time_data
        print("📝 Menambahkan kolom time_data...")
        cursor.execute("ALTER TABLE state_tracker ADD COLUMN time_data TEXT")
        conn.commit()
        
        print("✅ Kolom time_data berhasil ditambahkan")
        
        # Verifikasi
        cursor.execute("PRAGMA table_info(state_tracker)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'time_data' in columns:
            print("✅ Verifikasi: kolom time_data ada")
        else:
            print("❌ Verifikasi gagal: kolom time_data tidak ditemukan")
        
        conn.close()
        
        print("=" * 60)
        print("✅ FIX COMPLETE!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def fix_all_missing_columns():
    """Tambahkan semua kolom yang mungkin hilang"""
    
    print("=" * 60)
    print("🔧 FIX: Adding all missing columns to state_tracker")
    print("=" * 60)
    
    try:
        db_path = Path("data/amoria.db")
        
        if not db_path.exists():
            print(f"❌ Database not found at {db_path}")
            return False
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Cek kolom yang ada
        cursor.execute("PRAGMA table_info(state_tracker)")
        existing = [col[1] for col in cursor.fetchall()]
        
        print(f"📊 Existing columns: {existing}")
        
        # Kolom yang diperlukan
        required_columns = {
            'time_data': 'TEXT',
            'clothing_bot_outer_bottom': 'TEXT',
            'clothing_user_outer_bottom': 'TEXT',
            'clothing_history': 'TEXT',
            'family_status': 'TEXT',
            'family_location': 'TEXT',
            'family_activity': 'TEXT',
            'family_estimate_return': 'TEXT',
            'time_override_history': 'TEXT',
        }
        
        added = 0
        for col, col_type in required_columns.items():
            if col not in existing:
                try:
                    cursor.execute(f"ALTER TABLE state_tracker ADD COLUMN {col} {col_type}")
                    print(f"  ✅ Added: {col}")
                    added += 1
                except Exception as e:
                    print(f"  ⚠️ Failed: {col} - {e}")
            else:
                print(f"  ⏭️ Already exists: {col}")
        
        if added > 0:
            conn.commit()
            print(f"\n✅ Added {added} column(s)")
        else:
            print("\n✅ No missing columns")
        
        conn.close()
        
        print("=" * 60)
        print("✅ FIX COMPLETE!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "all":
        success = asyncio.run(fix_all_missing_columns())
    else:
        success = asyncio.run(fix_time_data_column())
    
    sys.exit(0 if success else 1)
