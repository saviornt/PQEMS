import os
from cryptography.fernet import Fernet

def generate_key():
    """Generate and return a new key."""
    key = Fernet.generate_key()
    return key

def get_key():
    """Retrieve the encryption key from the environment or generate a new one."""
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        key = generate_key()
    return key

def save_key(key: bytes, file_path: str):
    """Save the key to a file."""
    with open(file_path, 'wb') as key_file:
        key_file.write(key)

def load_key(file_path: str) -> bytes:
    """Load the key from a file."""
    with open(file_path, 'rb') as key_file:
        return key_file.read()
