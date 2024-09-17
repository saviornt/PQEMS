from setuptools import setup, find_packages

setup(
    name="Post-Quantum Encryption Management System",
    version="0.1.0",
    author="David Wadsworth",
    author_email="david.wadsworth80@gmail.com",
    description="A post-quantum encryption and quantum compression management system project.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/saviornt/PQEMS",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "setuptools",
        "wheel",
        "python-dotenv",                    # Reads key-value pairs from a .env file and can set them as environment variables.
        "pkg-config",
        "qiskit>=1.2.1",                    # Quantum compression (Qiskit)
        "qiskit-aer>=0.15.1",               # IBM Aer Simulator
        "qiskit-ibm-provider>=0.11.0"       # IBM Quantum computer provider
        "pycryptodome>=3.20.0",             # Kyber encryption
        "liboqs>=0.9.1",                    # Post-quantum cryptography (Kyber)
        "cryptography>=43.0.1",             # General cryptography
        "pymongo>=4.8.0",                   # MongoDB support for database encryption
        "psycopg[binary,pool]>=3.2.2",      # PostgreSQL support
        "mysql-connector-python>=9.0.0",    # MySQL connector for Python
        "numpy==2.1.1",                     # For efficient numerical processing (required by Qiskit)
        "numba==0.60.0",                    # For JIT compilation (will help with GPU acceleration)
        "pycuda==2024.1.2",                 # Python wrapper for NVIDIA CUDA for GPU-based processing
        "torch>=2.4.1",                     # Provides GPU acceleration for non-CUDA machines.
        "reedsolo==1.7.0",                  # Classical error correction library (Reed-Solomon)
        "loguru==0.7.2",                    # Simplified logging library
        "pywin32==306",                     # Windows API, needed for DPAPI (no TPM)
        "tpm2-pytss>=2.3.0",                # TPM2 support for machines with an installed TPM
        "keyring>=25.3.0",                  # Used to support secure key storage on macOS Darwin (no TPM)
        "SecretStorage>=3.3.3",             # Linux API to securely store passwords on Linux (no TPM)
    ],
    entry_points={
        'console_scripts': [
            'quantum-encryption=main:main',
        ],
    },
)
