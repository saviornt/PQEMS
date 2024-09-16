import os
import shutil
from datetime import datetime
from loguru import logger
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create logs directory if it does not exist
logs_dir = 'logs'
os.makedirs(logs_dir, exist_ok=True)

# Configure logger
logger.add(os.path.join(logs_dir, "db_backup.log"), rotation="1 week", retention="1 month", level="DEBUG")

class BackupHandler:
    """
    A class to handle database backups and restorations.
    """
    
    def __init__(self, db_path):
        """
        Initialize the BackupHandler with the path to the database file.
        
        Parameters:
        - db_path (str): The path to the database file to be backed up.
        """
        self.db_path = db_path
        self.backup_dir = 'backups'
        os.makedirs(self.backup_dir, exist_ok=True)

    def backup(self):
        """
        Create a backup of the database file.
        
        This method copies the database file to the backup directory with a timestamp.
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.db")
            shutil.copy2(self.db_path, backup_file)
            logger.info(f"Backup created successfully: {backup_file}")
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")

    def restore(self, backup_file):
        """
        Restore the database from a specified backup file.
        
        Parameters:
        - backup_file (str): The path to the backup file to restore from.
        
        Raises:
        - FileNotFoundError: If the specified backup file does not exist.
        """
        if not os.path.exists(backup_file):
            logger.error(f"Backup file does not exist: {backup_file}")
            raise FileNotFoundError(f"Backup file not found: {backup_file}")

        try:
            shutil.copy2(backup_file, self.db_path)
            logger.info(f"Database restored successfully from: {backup_file}")
        except Exception as e:
            logger.error(f"Failed to restore database: {e}")

    def list_backups(self):
        """
        List all backup files in the backup directory.
        
        Returns:
        - list: A list of backup file names.
        """
        try:
            backups = [f for f in os.listdir(self.backup_dir) if f.startswith('backup_')]
            if backups:
                logger.info(f"Backups available: {', '.join(backups)}")
            else:
                logger.info("No backup files found.")
            return backups
        except Exception as e:
            logger.error(f"Failed to list backups: {e}")
            return []

    def delete_backup(self, backup_file):
        """
        Delete a specified backup file.
        
        Parameters:
        - backup_file (str): The name of the backup file to delete.
        
        Raises:
        - FileNotFoundError: If the specified backup file does not exist.
        """
        backup_path = os.path.join(self.backup_dir, backup_file)
        if not os.path.exists(backup_path):
            logger.error(f"Backup file does not exist: {backup_path}")
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        try:
            os.remove(backup_path)
            logger.info(f"Backup file deleted: {backup_path}")
        except Exception as e:
            logger.error(f"Failed to delete backup file: {e}")
