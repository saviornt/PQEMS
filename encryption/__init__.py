"""
Encryption package initialization.

This package includes modules for handling encryption-related operations.
It supports various encryption algorithms, including the Kyber encryption
scheme for post-quantum cryptography, as well as compression methods using
quantum and classical approaches.
"""

from .kyber_encryption import KyberEncryption
from .quantum_compression import QuantumCompression

__all__ = [
    'KyberEncryption',
    'QuantumCompression',
]
