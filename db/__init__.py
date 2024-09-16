"""
Database package initialization.

This package includes modules for handling database connections, backups,
and encryption. It supports various database types including SQLite,
PostgreSQL, MySQL, and MongoDB.
"""

from .database_handler import DatabaseHandler
from .db_backup import BackupHandler
from .db_encryption import DBEncryption

__all__ = [
    'DatabaseHandler',
    'BackupHandler',
    'DBEncryption',
]
