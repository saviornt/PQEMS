from cryptography.fernet import Fernet
from .key_management import get_key

class KyberEncryption:
    def __init__(self):
        self.key = get_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt the data."""
        return self.cipher.encrypt(data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypt the data."""
        return self.cipher.decrypt(encrypted_data)
