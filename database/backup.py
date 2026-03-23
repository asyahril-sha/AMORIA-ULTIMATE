# database/backup.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
Database Backup Manager - Backup & Restore dengan History
Target Realism 9.9/10
=============================================================================
"""

import json
import time
import logging
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .connection import get_db
from config import settings

logger = logging.getLogger(__name__)


async def create_backup_table():
    """
    Create backup history table if not exists
    Table untuk menyimpan riwayat backup
    """
    db = await get_db()
    
    await db.execute('''
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
    
    # Create index
    await db.execute('CREATE INDEX IF NOT EXISTS idx_backups_created_at ON backups(created_at)')
    await db.execute('CREATE INDEX IF NOT EXISTS idx_backups_type ON backups(type)')
    
    logger.info("✅ Backups table created")


async def add_backup_record(
    filename: str,
    size: int,
    backup_type: str = "auto",
    status: str = "completed",
    metadata: Optional[Dict] = None
) -> int:
    """
    Tambah record backup ke database
    
    Args:
        filename: Nama file backup
        size: Ukuran file dalam bytes
        backup_type: Tipe backup ('auto' atau 'manual')
        status: Status backup ('pending', 'completed', 'failed')
        metadata: Metadata tambahan
    
    Returns:
        ID record backup
    """
    db = await get_db()
    
    result = await db.execute(
        """
        INSERT INTO backups (filename, size, created_at, type, status, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            size,
            datetime.now().timestamp(),
            backup_type,
            status,
            json.dumps(metadata or {})
        )
    )
    
    logger.info(f"✅ Backup record added: {filename} ({size} bytes)")
    
    return result.lastrowid


async def update_backup_status(backup_id: int, status: str, metadata: Optional[Dict] = None):
    """
    Update status backup
    
    Args:
        backup_id: ID backup
        status: Status baru
        metadata: Metadata tambahan
    """
    db = await get_db()
    
    if metadata:
        # Get existing metadata
        row = await db.fetch_one("SELECT metadata FROM backups WHERE id = ?", (backup_id,))
        if row and row['metadata']:
            existing = json.loads(row['metadata'])
            existing.update(metadata)
            new_metadata = json.dumps(existing)
        else:
            new_metadata = json.dumps(metadata)
        
        await db.execute(
            "UPDATE backups SET status = ?, metadata = ? WHERE id = ?",
            (status, new_metadata, backup_id)
        )
    else:
        await db.execute(
            "UPDATE backups SET status = ? WHERE id = ?",
            (status, backup_id)
        )
    
    logger.info(f"📝 Backup {backup_id} status updated: {status}")


async def get_backups(
    limit: int = 10,
    backup_type: Optional[str] = None,
    status: Optional[str] = None
) -> List[Dict]:
    """
    Dapatkan daftar backup terbaru
    
    Args:
        limit: Jumlah maksimal backup
        backup_type: Filter tipe backup ('auto' atau 'manual')
        status: Filter status
    
    Returns:
        List dictionary backup
    """
    db = await get_db()
    
    query = "SELECT * FROM backups"
    params = []
    conditions = []
    
    if backup_type:
        conditions.append("type = ?")
        params.append(backup_type)
    
    if status:
        conditions.append("status = ?")
        params.append(status)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    
    rows = await db.fetch_all(query, tuple(params))
    
    backups = []
    for row in rows:
        backup = dict(row)
        backup['metadata'] = json.loads(backup['metadata']) if backup['metadata'] else {}
        backup['created_at_formatted'] = datetime.fromtimestamp(backup['created_at']).strftime("%Y-%m-%d %H:%M:%S")
        backup['size_mb'] = round(backup['size'] / (1024 * 1024), 2) if backup['size'] else 0
        backups.append(backup)
    
    return backups


async def get_backup_by_filename(filename: str) -> Optional[Dict]:
    """
    Dapatkan backup berdasarkan nama file
    
    Args:
        filename: Nama file backup
    
    Returns:
        Dictionary backup atau None
    """
    db = await get_db()
    
    row = await db.fetch_one("SELECT * FROM backups WHERE filename = ?", (filename,))
    
    if not row:
        return None
    
    backup = dict(row)
    backup['metadata'] = json.loads(backup['metadata']) if backup['metadata'] else {}
    backup['created_at_formatted'] = datetime.fromtimestamp(backup['created_at']).strftime("%Y-%m-%d %H:%M:%S")
    backup['size_mb'] = round(backup['size'] / (1024 * 1024), 2) if backup['size'] else 0
    
    return backup


async def get_latest_backup(backup_type: Optional[str] = None) -> Optional[Dict]:
    """
    Dapatkan backup terbaru
    
    Args:
        backup_type: Filter tipe backup
    
    Returns:
        Dictionary backup atau None
    """
    backups = await get_backups(limit=1, backup_type=backup_type)
    return backups[0] if backups else None


async def cleanup_old_backups(days: int = 30) -> int:
    """
    Hapus record backup lama dari database (file fisik tetap ada)
    
    Args:
        days: Umur maksimal backup dalam hari
    
    Returns:
        Jumlah backup yang dihapus
    """
    db = await get_db()
    
    cutoff_time = time.time() - (days * 86400)
    
    result = await db.execute(
        "DELETE FROM backups WHERE created_at < ?",
        (cutoff_time,)
    )
    
    deleted = result.rowcount
    logger.info(f"🗑️ Cleaned up {deleted} old backup records (older than {days} days)")
    
    return deleted


async def delete_backup_record(backup_id: int) -> bool:
    """
    Hapus record backup dari database
    
    Args:
        backup_id: ID backup
    
    Returns:
        True jika berhasil
    """
    db = await get_db()
    
    result = await db.execute("DELETE FROM backups WHERE id = ?", (backup_id,))
    
    success = result.rowcount > 0
    if success:
        logger.info(f"🗑️ Deleted backup record {backup_id}")
    
    return success


async def get_backup_stats() -> Dict[str, Any]:
    """
    Dapatkan statistik backup
    
    Returns:
        Dictionary statistik backup
    """
    db = await get_db()
    
    # Total backups
    total = await db.fetch_one("SELECT COUNT(*) as count FROM backups")
    total_count = total['count'] if total else 0
    
    # By type
    auto = await db.fetch_one("SELECT COUNT(*) as count FROM backups WHERE type = 'auto'")
    manual = await db.fetch_one("SELECT COUNT(*) as count FROM backups WHERE type = 'manual'")
    
    # By status
    completed = await db.fetch_one("SELECT COUNT(*) as count FROM backups WHERE status = 'completed'")
    failed = await db.fetch_one("SELECT COUNT(*) as count FROM backups WHERE status = 'failed'")
    
    # Total size
    size_result = await db.fetch_one("SELECT SUM(size) as total_size FROM backups WHERE status = 'completed'")
    total_size_bytes = size_result['total_size'] if size_result and size_result['total_size'] else 0
    total_size_mb = round(total_size_bytes / (1024 * 1024), 2)
    
    # Last backup
    last = await db.fetch_one("SELECT MAX(created_at) as last FROM backups")
    last_backup = datetime.fromtimestamp(last['last']).strftime("%Y-%m-%d %H:%M:%S") if last and last['last'] else None
    
    return {
        'total_backups': total_count,
        'auto_backups': auto['count'] if auto else 0,
        'manual_backups': manual['count'] if manual else 0,
        'completed_backups': completed['count'] if completed else 0,
        'failed_backups': failed['count'] if failed else 0,
        'total_size_mb': total_size_mb,
        'last_backup': last_backup
    }


async def verify_backup_integrity(backup_path: Path) -> Dict[str, Any]:
    """
    Verifikasi integritas file backup
    
    Args:
        backup_path: Path file backup
    
    Returns:
        Dictionary hasil verifikasi
    """
    import zipfile
    import hashlib
    
    result = {
        'filename': backup_path.name,
        'valid': False,
        'size_bytes': 0,
        'size_mb': 0,
        'files': 0,
        'checksum': None,
        'error': None
    }
    
    if not backup_path.exists():
        result['error'] = "File not found"
        return result
    
    result['size_bytes'] = backup_path.stat().st_size
    result['size_mb'] = round(result['size_bytes'] / (1024 * 1024), 2)
    
    # Calculate checksum
    sha256 = hashlib.sha256()
    with open(backup_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    result['checksum'] = sha256.hexdigest()
    
    # Verify ZIP integrity
    try:
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            bad_file = zipf.testzip()
            if bad_file:
                result['error'] = f"Corrupted file: {bad_file}"
                return result
            result['files'] = len(zipf.namelist())
            result['valid'] = True
    except zipfile.BadZipFile as e:
        result['error'] = f"Bad ZIP file: {e}"
    except Exception as e:
        result['error'] = str(e)
    
    return result


async def get_backup_directory_info() -> Dict[str, Any]:
    """
    Dapatkan informasi direktori backup
    
    Returns:
        Dictionary informasi direktori
    """
    backup_dir = settings.backup.backup_dir if hasattr(settings, 'backup') else Path("data/backups")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    files = list(backup_dir.glob("amoria_backup_*.zip"))
    
    total_size = 0
    for f in files:
        total_size += f.stat().st_size
    
    return {
        'directory': str(backup_dir),
        'total_files': len(files),
        'total_size_mb': round(total_size / (1024 * 1024), 2),
        'files': sorted([{
            'name': f.name,
            'size_mb': round(f.stat().st_size / (1024 * 1024), 2),
            'modified': datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        } for f in files], key=lambda x: x['modified'], reverse=True)
    }


__all__ = [
    'create_backup_table',
    'add_backup_record',
    'update_backup_status',
    'get_backups',
    'get_backup_by_filename',
    'get_latest_backup',
    'cleanup_old_backups',
    'delete_backup_record',
    'get_backup_stats',
    'verify_backup_integrity',
    'get_backup_directory_info',
]
