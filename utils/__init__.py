"""
Encryption package initialization.

This package includes modules for handling encryption-related operations.
It supports various encryption algorithms, including the Kyber encryption
scheme for post-quantum cryptography, as well as compression methods using
quantum and classical approaches.
"""

from .error_correction import ErrorCorrection

__all__ = [
    'ErrorCorrection',
]
