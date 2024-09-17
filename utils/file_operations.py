import os
from encryption import KyberEncryption, QuantumCompression
from error_correction import ErrorCorrection
from loguru import logger

# Create logs directory if it does not exist
logs_dir = 'logs'
os.makedirs(logs_dir, exist_ok=True)

# Configure logger
logger.add(os.path.join(logs_dir, "file_operations.log"), rotation="1 week", retention="1 month", level="DEBUG")


class FileOperations:
    def __init__(self):
        self.encryption = KyberEncryption()
        self.compression = QuantumCompression()
        self.error_correction = ErrorCorrection()
        logger.info("FileOperations initialized.")

    def read_file(self, filepath):
        """
        Read file, decrypt, decompress, and apply error correction.
        :param filepath: Path to the file.
        :return: The original data.
        """
        try:
            logger.info(f"Reading file from {filepath}.")
            with open(filepath, 'rb') as file:
                encrypted_data = file.read()

            logger.info(f"File read successfully from {filepath}, applying decryption.")
            decrypted_data = self.encryption.decrypt(encrypted_data)

            logger.info("Decryption successful, applying decompression.")
            decompressed_data = self.compression.decompress(decrypted_data)

            logger.info("Decompression successful, applying error correction.")
            corrected_data = self.error_correction.decode(decompressed_data)

            logger.info("Error correction complete, returning original data.")
            return corrected_data
        except Exception as e:
            logger.error(f"Error in reading file {filepath}: {e}")
            raise

    def write_file(self, filepath, data):
        """
        Compress, encrypt, apply error correction, and write data to file.
        :param filepath: Path to the file.
        :param data: The original data to be saved.
        """
        try:
            logger.info(f"Compressing data for {filepath}.")
            compressed_data = self.compression.compress(data)

            logger.info("Compression successful, applying error correction.")
            corrected_data = self.error_correction.encode(compressed_data)

            logger.info("Error correction successful, applying encryption.")
            encrypted_data = self.encryption.encrypt(corrected_data)

            logger.info(f"Writing encrypted data to {filepath}.")
            with open(filepath, 'wb') as file:
                file.write(encrypted_data)

            logger.info(f"File successfully written to {filepath}.")
        except Exception as e:
            logger.error(f"Error in writing file {filepath}: {e}")
            raise

    def read_file_in_chunks(self, filepath, chunk_size=1024):
        """
        Read large files in chunks.
        :param filepath: Path to the file.
        :param chunk_size: Size of the chunk to read.
        """
        try:
            logger.info(f"Reading file in chunks from {filepath}.")
            with open(filepath, 'rb') as file:
                while chunk := file.read(chunk_size):
                    yield chunk
        except Exception as e:
            logger.error(f"Error reading file in chunks {filepath}: {e}")
            raise

    def write_file_in_chunks(self, filepath, data_generator, chunk_size=1024):
        """
        Write large files in chunks.
        :param filepath: Path to the file.
        :param data_generator: A generator or iterable of data chunks.
        :param chunk_size: Size of each chunk to write.
        """
        try:
            logger.info(f"Writing file in chunks to {filepath}.")
            with open(filepath, 'wb') as file:
                for chunk in data_generator:
                    # Split the data into smaller chunks of 'chunk_size' and write.
                    for i in range(0, len(chunk), chunk_size):
                        file.write(chunk[i:i + chunk_size])

            logger.info(f"File successfully written in chunks to {filepath}.")
        except Exception as e:
            logger.error(f"Error writing file in chunks {filepath}: {e}")
            raise
