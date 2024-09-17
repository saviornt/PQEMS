import platform
import liboqs  # For Kyber key generation
from loguru import logger
import os
# Check if TPM, DPAPI, Libsecret, or macOS Keychain can be used for secure storage
from tpm2_pytss import ESAPI, TSS2_Exception  # TPM library for Linux
import win32crypt  # DPAPI for Windows
import secretstorage  # Libsecret for Linux
import subprocess  # For macOS Keychain

# Create logs directory if it does not exist
logs_dir = 'logs'
os.makedirs(logs_dir, exist_ok=True)

# Configure logger
logger.add(os.path.join(logs_dir, "key_management.log"), rotation="1 week", retention="1 month", level="DEBUG")

class KeyManager:
    def __init__(self):
        """
        Initialize KeyManager. Detects hardware and operating system to determine the best method for secure key storage.
        """
        self.tpm_available = self._detect_tpm()

        # Platform detection
        self.platform = platform.system()
        if self.tpm_available:
            logger.info("TPM available, will use TPM for key management.")
        elif self.platform == 'Windows':
            logger.info("Windows detected, will use DPAPI for key management.")
        elif self.platform == 'Linux':
            logger.info("Linux detected, will use Libsecret for key management.")
        elif self.platform == 'Darwin':
            logger.info("macOS detected, will use Keychain for key management.")
        else:
            raise NotImplementedError("Unsupported platform.")

    def _detect_tpm(self):
        """
        Check if TPM is available on the system.
        :return: True if TPM is available, False otherwise.
        """
        try:
            with ESAPI() as tpm:
                tpm.get_random(32)  # Example TPM operation to test availability
                logger.info("TPM is available.")
                return True
        except TSS2_Exception as e:
            logger.warning(f"TPM not available: {e}")
            return False

    def generate_kyber_keypair(self):
        """
        Generate a Kyber key pair using liboqs.
        :return: public_key, private_key
        """
        logger.debug("Generating Kyber keypair...")
        kem = liboqs.KeyEncapsulation('Kyber512')
        public_key = kem.export_public_key()
        private_key = kem.export_secret_key()
        logger.info("Kyber keypair generated.")
        return public_key, private_key

    def store_key(self, key_data, key_name):
        """
        Store the given key securely depending on the platform and hardware availability (TPM, DPAPI, Libsecret, or Keychain).
        :param key_data: The key data to be stored.
        :param key_name: A unique identifier for the key.
        """
        if self.tpm_available:
            self._store_key_tpm(key_data, key_name)
        elif self.platform == 'Windows':
            self._store_key_dpapi(key_data, key_name)
        elif self.platform == 'Linux':
            self._store_key_libsecret(key_data, key_name)
        elif self.platform == 'Darwin':
            self._store_key_mac_keychain(key_data, key_name)
        else:
            raise NotImplementedError("No secure key storage method available for this platform.")

    def _store_key_tpm(self, key_data, key_name):
        """
        Store the key using TPM on Linux systems.
        :param key_data: The key to store.
        :param key_name: The name to associate with the key in TPM.
        """
        logger.debug(f"Storing key in TPM with name: {key_name}")
        try:
            with ESAPI() as tpm:
                # Example TPM NV index for storage
                nv_index = 0x1500016
                tpm.create_nv_index(nv_index, 0x01, key_data.encode('utf-8'))
                logger.info(f"Key {key_name} stored in TPM.")
        except TSS2_Exception as e:
            logger.error(f"Failed to store key in TPM: {e}")

    def _store_key_dpapi(self, key_data, key_name):
        """
        Store the key securely using DPAPI on Windows.
        :param key_data: The key to store.
        :param key_name: The name of the key to store.
        """
        logger.debug(f"Storing key in Windows DPAPI with name: {key_name}")
        try:
            encrypted_key = win32crypt.CryptProtectData(
                key_data.encode('utf-8'),
                None,  # Optional description
                None,  # Optional entropy
                None,  # Optional reserved
                None,  # Optional prompt
                0      # Flags
            )
            with open(f"{key_name}.dpapi", 'wb') as file:
                file.write(encrypted_key)
            logger.info(f"Key {key_name} stored using DPAPI.")
        except Exception as e:
            logger.error(f"Failed to store key using DPAPI: {e}")

    def _store_key_libsecret(self, key_data, key_name):
        """
        Store the key securely using Libsecret on Linux.
        :param key_data: The key to store.
        :param key_name: The name of the key.
        """
        logger.debug(f"Storing key in Libsecret with name: {key_name}")
        try:
            connection = secretstorage.dbus_init()
            collection = secretstorage.get_default_collection(connection)
            if not collection.is_locked():
                collection.unlock()
            item = collection.create_item(
                key_name,
                {'application': 'my_app'},
                key_data.encode('utf-8'),
                replace=True
            )
            logger.info(f"Key {key_name} stored in Libsecret.")
        except Exception as e:
            logger.error(f"Failed to store key using Libsecret: {e}")

    def _store_key_mac_keychain(self, key_data, key_name):
        """
        Store the key securely using macOS Keychain.
        :param key_data: The key to store.
        :param key_name: The name of the key.
        """
        logger.debug(f"Storing key in macOS Keychain with name: {key_name}")
        try:
            command = [
                'security', 'add-generic-password',
                '-a', key_name,
                '-s', key_name,
                '-w', key_data
            ]
            subprocess.run(command, check=True)
            logger.info(f"Key {key_name} stored in macOS Keychain.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to store key using Keychain: {e}")

    def load_key(self, key_name):
        """
        Load the key securely depending on the platform and hardware availability (TPM, DPAPI, Libsecret, or Keychain).
        :param key_name: The name of the key to load.
        :return: The key data or None if not found.
        """
        if self.tpm_available:
            return self._load_key_tpm(key_name)
        elif self.platform == 'Windows':
            return self._load_key_dpapi(key_name)
        elif self.platform == 'Linux':
            return self._load_key_libsecret(key_name)
        elif self.platform == 'Darwin':
            return self._load_key_mac_keychain(key_name)
        else:
            raise NotImplementedError("No secure key loading method available for this platform.")

    def _load_key_tpm(self, key_name):
        """
        Load the key securely from TPM on Linux systems.
        :param key_name: The name of the key in TPM.
        :return: The key data or None if not found.
        """
        logger.debug(f"Loading key from TPM with name: {key_name}")
        try:
            with ESAPI() as tpm:
                # Example TPM NV index for retrieval
                nv_index = 0x1500016
                key_data = tpm.read_nv_index(nv_index).decode('utf-8')
                logger.info(f"Key {key_name} loaded from TPM.")
                return key_data
        except TSS2_Exception as e:
            logger.error(f"Failed to load key from TPM: {e}")
            return None

    def _load_key_dpapi(self, key_name):
        """
        Load the key securely using DPAPI on Windows.
        :param key_name: The name of the key.
        :return: The key data or None if not found.
        """
        logger.debug(f"Loading key from Windows DPAPI with name: {key_name}")
        try:
            with open(f"{key_name}.dpapi", 'rb') as file:
                encrypted_key = file.read()
            key_data = win32crypt.CryptUnprotectData(
                encrypted_key,
                None,  # Optional description
                None,  # Optional entropy
                None,  # Optional reserved
                None,  # Optional prompt
                0      # Flags
            )[1].decode('utf-8')
            logger.info(f"Key {key_name} loaded from DPAPI.")
            return key_data
        except Exception as e:
            logger.error(f"Failed to load key using DPAPI: {e}")
            return None

    def _load_key_libsecret(self, key_name):
        """
        Load the key securely using Libsecret on Linux.
        :param key_name: The name of the key.
        :return: The key data or None if not found.
        """
        logger.debug(f"Loading key from Libsecret with name: {key_name}")
        try:
            connection = secretstorage.dbus_init()
            collection = secretstorage.get_default_collection(connection)
            if collection.is_locked():
                collection.unlock()
            item = collection.get_item_by_label(key_name)
            key_data = item.get_secret().decode('utf-8')
            logger.info(f"Key {key_name} loaded from Libsecret.")
            return key_data
        except Exception as e:
            logger.error(f"Failed to load key using Libsecret: {e}")
            return None

    def _load_key_mac_keychain(self, key_name):
        """
        Load the key securely using macOS Keychain.
        :param key_name: The name of the key.
        :return: The key data or None if not found.
        """
        logger.debug(f"Loading key from macOS Keychain with name: {key_name}")
        try:
            command = [
                'security', 'find-generic-password',
                '-a', key_name,
                '-s', key_name,
                '-w'
            ]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            key_data = result.stdout.strip()
            logger.info(f"Key {key_name} loaded from macOS Keychain.")
            return key_data
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to load key using Keychain: {e}")
            return None
