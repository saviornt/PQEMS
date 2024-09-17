from loguru import logger
from key_management import KeyManager
import liboqs  # For Kyber encryption
import pickle
import json
import os

# Create logs directory if it does not exist
logs_dir = 'logs'
os.makedirs(logs_dir, exist_ok=True)

# Configure logger
logger.add(os.path.join(logs_dir, "kyber_encryption.log"), rotation="1 week", retention="1 month", level="DEBUG")

class KyberEncryption:
    def __init__(self):
        """
        Initialize KyberEncryption by setting up the KeyManager and retrieving the key pair.
        """
        self.key_manager = KeyManager()
        self.public_key, self.private_key = self.key_manager.generate_kyber_keypair()
        self._store_keys()

    def _store_keys(self):
        """
        Store the generated public and private keys using the KeyManager.
        """
        key_name_public = 'kyber_public_key'
        key_name_private = 'kyber_private_key'
        self.key_manager.store_key(self.public_key.decode('utf-8'), key_name_public)
        self.key_manager.store_key(self.private_key.decode('utf-8'), key_name_private)
        logger.info("Keys have been stored.")

    def prepare_message(self, data):
        """
        Convert various data types to bytes for encryption.
        :param data: The data to convert (str, dict, float, etc.).
        :return: Byte representation of the data.
        """
        if isinstance(data, str):
            return data.encode('utf-8')
        elif isinstance(data, (bytes, bytearray)):
            return data
        elif isinstance(data, (dict, list)):
            return json.dumps(data).encode('utf-8')
        elif isinstance(data, (int, float)):
            return str(data).encode('utf-8')
        else:
            return pickle.dumps(data)

    def process_decrypted_data(self, data):
        """
        Convert bytes back to original data type after decryption.
        :param data: Decrypted byte data.
        :return: Original data.
        """
        try:
            # Try to decode as JSON
            return json.loads(data.decode('utf-8'))
        except json.JSONDecodeError:
            try:
                # Try to decode as a number
                return float(data.decode('utf-8'))
            except ValueError:
                try:
                    # Try to deserialize as a complex object
                    return pickle.loads(data)
                except Exception as e:
                    # Log and raise an error for unsupported formats
                    logger.error(f"Failed to process decrypted data: {e}")
                    return data.decode('utf-8')

    def encrypt(self, data):
        """
        Encrypt data using Kyber encryption.
        :param data: Data to encrypt (can be str, dict, int, float, etc.).
        :return: Encrypted data.
        """
        message = self.prepare_message(data)
        public_key = self.key_manager.load_key('kyber_public_key')
        if public_key is None:
            logger.error("Public key not found.")
            raise ValueError("Public key not found.")
        
        kem = liboqs.KeyEncapsulation('Kyber512')
        kem.import_public_key(public_key.encode('utf-8'))
        ciphertext, _ = kem.encrypt(message)
        logger.info("Data encrypted.")
        return ciphertext

    def decrypt(self, ciphertext):
        """
        Decrypt data using Kyber encryption.
        :param ciphertext: Encrypted data.
        :return: Decrypted data.
        """
        private_key = self.key_manager.load_key('kyber_private_key')
        if private_key is None:
            logger.error("Private key not found.")
            raise ValueError("Private key not found.")
        
        kem = liboqs.KeyEncapsulation('Kyber512')
        kem.import_secret_key(private_key.encode('utf-8'))
        decrypted_message, _ = kem.decrypt(ciphertext)
        logger.info("Data decrypted.")
        return self.process_decrypted_data(decrypted_message)
