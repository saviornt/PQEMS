import os
from pathlib import Path

# --- General Settings ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Environment Settings ---
# Load environment variables from a .env file
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

# DEBUG mode (set to True in development and False in production)
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# --- Database Configuration ---
# MongoDB Settings
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'pqems_db')

# PostgreSQL Database Settings
POSTGRES_DB = os.getenv('POSTGRES_DB', 'pqems')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'admin_password')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# --- Security and Encryption ---
# Post-Quantum Encryption using Kyber and other algorithms
# Keys, encryption, and other security-related settings
ENCRYPTION_ALGORITHM = os.getenv('ENCRYPTION_ALGORITHM', 'kyber')
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'your_encryption_key_here')

# --- Quantum Computing Settings ---
# Qiskit backend for quantum processing
QISKIT_BACKEND = os.getenv('QISKIT_BACKEND', 'ibmq_qasm_simulator')

# --- Multiprocessing and Resource Management ---
CPU_COUNT = os.cpu_count()  # Total number of CPUs available
GPU_ENABLED = os.getenv('GPU_ENABLED', 'False') == 'True'  # Check if GPU acceleration is enabled

# --- Logging Configuration ---
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # Log level can be 'DEBUG', 'INFO', 'WARNING', etc.
LOG_FORMAT = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"

# --- File Management ---
# Path to store temporary or output files
TEMP_DIR = os.getenv('TEMP_DIR', os.path.join(BASE_DIR, 'temp'))
OUTPUT_DIR = os.getenv('OUTPUT_DIR', os.path.join(BASE_DIR, 'output'))

# --- Other Configuration Settings ---
# You can add other custom configurations like API keys, timeout settings, etc.
