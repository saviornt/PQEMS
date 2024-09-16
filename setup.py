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
        "pkg-config"
        "qiskit>=1.2.1",                # Quantum compression (Qiskit)
        "pycryptodome>=3.20.0",         # Kyber encryption
        "liboqs>=0.9.1",                # Post-quantum cryptography (Kyber)
        "cryptography>=43.0.1",         # General cryptography
        "pymongo>=4.8.0",               # MongoDB support for database encryption
        "psycopg[binary,pool]>=3.2.2",  # PostgreSQL support
        "numpy==2.1.1",                 # For efficient numerical processing (required by Qiskit)
        "numba==0.60.0",                # For JIT compilation (will help with GPU acceleration)
        "pycuda==2024.1.2",             # Python wrapper for NVIDIA CUDA for GPU-based processing
        "reedsolo==1.7.0",              # Classical error correction library (Reed-Solomon)
        "loguru==0.7.2",                # Simplified logging library
    ],
    extras_require={
        "windows": [
            "pywin32==306",             # Windows specific package for DPAPI
        ],
        "macos": [],
        "linux": [
            "python-tpm2-pytss==2.3.0", # TPM2 support for Linux
        ],
    },
    entry_points={
        'console_scripts': [
            'quantum-encryption=main:main',
        ],
    },
)
