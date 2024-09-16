import os
import shutil
from kyber_encryption import KyberEncryption
from loguru import logger
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create logs directory if it does not exist
logs_dir = 'logs'
os.makedirs(logs_dir, exist_ok=True)

# Configure logger
logger.add(os.path.join(logs_dir, "db_encryption.log"), rotation="1 week", retention="1 month", level="DEBUG")

class DBEncryption:
    """
    A class to handle encryption and decryption of database backups using Kyber encryption.
    """
    
    def __init__(self):
        """
        Initialize the DBEncryption class with a Kyber encryption instance.
        """
        self.kyber = KyberEncryption()  # Initialize the Kyber encryption class

    def encrypt_file(self, input_file, output_file):
        """
        Encrypt a file using Kyber encryption.
        
        Parameters:
        - input_file (str): Path to the input file to be encrypted.
        - output_file (str): Path to the output file to save the encrypted data.
        """
        try:
            with open(input_file, 'rb') as f:
                data = f.read()
                
            encrypted_data = self.kyber.encrypt(data)
            
            with open(output_file, 'wb') as f:
                f.write(encrypted_data)
                
            logger.info(f"File encrypted successfully: {input_file} -> {output_file}")
        except Exception as e:
            logger.error(f"Failed to encrypt file {input_file}: {e}")
            raise

    def decrypt_file(self, input_file, output_file):
        """
        Decrypt a file using Kyber encryption.
        
        Parameters:
        - input_file (str): Path to the encrypted file.
        - output_file (str): Path to the output file to save the decrypted data.
        """
        try:
            with open(input_file, 'rb') as f:
                encrypted_data = f.read()
                
            decrypted_data = self.kyber.decrypt(encrypted_data)
            
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
                
            logger.info(f"File decrypted successfully: {input_file} -> {output_file}")
        except Exception as e:
            logger.error(f"Failed to decrypt file {input_file}: {e}")
            raise

    def backup_and_encrypt(self, db_file, backup_file):
        """
        Backup and encrypt the database file.
        
        Parameters:
        - db_file (str): Path to the database file to backup.
        - backup_file (str): Path to the backup file to save the encrypted backup.
        """
        try:
            shutil.copy(db_file, backup_file)
            self.encrypt_file(backup_file, backup_file)
            logger.info(f"Database file backed up and encrypted: {db_file} -> {backup_file}")
        except Exception as e:
            logger.error(f"Failed to backup and encrypt database file {db_file}: {e}")
            raise

    def decrypt_and_restore(self, backup_file, restore_file):
        """
        Decrypt and restore the database file from a backup.
        
        Parameters:
        - backup_file (str): Path to the encrypted backup file.
        - restore_file (str): Path to the restored database file.
        """
        try:
            decrypted_backup_file = backup_file + '.decrypted'
            self.decrypt_file(backup_file, decrypted_backup_file)
            shutil.copy(decrypted_backup_file, restore_file)
            os.remove(decrypted_backup_file)
            logger.info(f"Database file decrypted and restored: {backup_file} -> {restore_file}")
        except Exception as e:
            logger.error(f"Failed to decrypt and restore database file {backup_file}: {e}")
            raise
