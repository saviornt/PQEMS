import os
import random
import platform
import subprocess
import sys
import base64
import hashlib
import oqs
import numpy as np
from qiskit import QuantumCircuit, transpile, assemble
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

def create_random_file(filename, size_in_mb=50):
    size_bytes = size_in_mb * 1024 * 1024
    with open(filename, 'wb') as f:
        f.write(os.urandom(size_bytes))
    print(f"{filename} created with size {size_in_mb} MB.")

def file_hash(filename, hash_algorithm='sha256'):
    hash_func = hashlib.new(hash_algorithm)
    with open(filename, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def compare_files(file1, file2):
    f1_size = os.path.getsize(file1)
    f1_hash = file_hash(file1)
    f2_size = os.path.getsize(file2)
    f2_hash = file_hash(file2)
    
    print(f"File 1: Size = {f1_size} bytes, Hash = {f1_hash}")
    print(f"File 2: Size = {f2_size} bytes, Hash = {f2_hash}")
    
    return f1_size, f1_hash, f2_size, f2_hash

# Function to perform quantum compression and error correction using Qiskit
def quantum_compression_error_correction(input_file, compressed_file, error_corrected_file):
    # Create a simple quantum circuit
    circuit = QuantumCircuit(8, 8)
    circuit.h(range(8)) # Apply Hadamard gates
    circuit.barrier()
    circuit.measure(range(8), range(8))

    # Execute the circuit
    simulator = AerSimulator()
    backend = simulator.run("qasm_simulator")
    job = transpile(circuit, backend) 
    result = job.result()

    # Get the counts
    counts = result.get_counts()
    print("Quantum Circuit Results:", counts)

    # Save compressed data as an example (demonstration only)
    with open(input_file, "rb") as f:
        data = f.read()
    
    # Simulate compression (for demonstation purposes, not real compression)
    with open(compressed_file, "wb") as f:
        f.write(data[:len(data)//2])
    
    # Simulate error correction (for demonstraton purposes, not real error correction)
    with open(error_corrected_file, "wb") as f:
        f.write(data[:len(data)//2])
    
    print("Quantum compression and error correction completed")

# Function to handle post-quantum encryption and secure key storage
def pqc_kyber(input_file):
    # Initialize Kyber KEM algorithm
    kem = oqs.KeyEncapsulation("Kyber1024")

    # Generate keypair
    public_key = kem.generate_keypair()

    # Encapsulate the secret
    ciphertext, shared_secret_enc = kem.encap_secret(public_key)
    print("Shared Secret (Encapsulator):", shared_secret_enc.hex())

    # Store the shared secret using TPM or DPAPI depending on the OS
    if platform.system() == "Linux":
        
        # Store the key with tpm2-tools
        print("Linux detected: Using TPM2 tools")
        with open("shared_secret.bin", "wb") as f:
            f.write(shared_secret_enc)
        
        # Store the key using TPM
        os.system("tpm2_nvdefine 0x1500016 -s 64 -a 'ownerread|ownerwrite'")
        os.system("tpm2_nvwrite 0x1500016 -i shared_secret.bin")
        print("Shared secret securely stored using TPM 2.0")

    elif platform.system() == "Windows":
        print("Windows detected: Using DPAPI")
        import ctypes
        from ctypes import wintypes

        # Use Windows Data Protection API (DPAPI) to securely store the key
        CRYPTPROTECT_UI_FORBIDDEN = 0x01
        crypt32 = ctypes.windll.crypt32
        kernel32 = ctypes.windll.kernel32

        class DATA_BLOB(ctypes.Structure):
            _fields_ = [("cbData", wintypes.DWORD),
                        ("pbData", ctypes.POINTER(ctypes.c_byte))]
        
        def protect_data(data: bytes) -> bytes:
            blob_in = DATA_BLOB(len(data), ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_byte)))
            blob_out = DATA_BLOB()

            result = crypt32.CryptProtectData(ctypes.byref(blob_in), None, None, None, None, CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(blob_out))
            if not result:
                raise ctypes.WinError()
            
            encrypted_data = ctypes.string_at(blob_out.pbData, blob_out.cbData)
            kernel32.LocalFree(blob_out.pbData)
            return encrypted_data
    
        encrypted_shared_secret = protect_data(shared_secret_enc)
        with open("shared_secret_encrypted.bin", "wb") as f:
            f.write(encrypted_shared_secret)
        print("Shared secret securely stored using DPAPI")
    
    # Simulate decapsulation and key retrieval
    shared_secret_dec = kem.decap_secret(ciphertext)
    print("Shared Secret (Decapsulator):", shared_secret_dec.hex())

    # Compare shared secrets to verify correctness
    assert shared_secret_enc == shared_secret_dec
    print("Quantum-safe encryption and decryption using Kyber with TPM/DPAPI was successfull!!")

    return shared_secret_enc, encrypted_shared_secret

# Function to decrypt the encrypted file using Kyber
def decrypt_file(encrypted_file, decrypted_file, shared_secret_enc):
    kem = oqs.KeyEncapsulation("Kyber1024")

    # Decapsulate the shared secret
    shared_secret_dec = kem.decap_secret(shared_secret_enc)
    print("Shared Secret (Decapsulator):", shared_secret_dec.hex())

    # Simulate the decryption (actual decryption should be implemented)
    with open(encrypted_file, "rb") as f:
        encrypted_data = f.read()
    
    # Simulate decryption (for demonstration purposes, not real decryption)
    with open(decrypt_file, "wb") as f:
        f.write(encrypted_data)
    
    print(f"File decrypted and saved as {decrypted_file}")

# Function to decompress the file and perform classical error correction
def decompress_and_correct(input_file, decompressed_file):
    # Read the compressed file
    with open(input_file, "rb") as f:
        compressed_data = f.read()
    
    # Simulate decompression (for demonstration purposes, not real decompression)
    decompressed_data = compressed_data * 2  # Placeholder for real decompression
    
    # Simulate classical error correction (for demonstration purposes, not real correction)
    error_corrected_data = decompressed_data[:len(decompressed_data) // 2]
    
    # Save the decompressed and corrected data
    with open(decompressed_file, "wb") as f:
        f.write(error_corrected_data)
    
    print(f"File decompressed and error-corrected, saved as {decompressed_file}")

if __name__ == "__main__":
    # Step 1: Create 50MB file of random characters
    original_filename = "random_file.bin"
    compressed_filename = "compressed_file.bin"
    error_corrected_filename = "error_corrected_file.bin"
    decrypted_filename = "decrypted_file.bin"
    final_filename = "final_file.bin"

    create_random_file(original_filename)

    # Step 2: Perform quantum compression and error correction
    quantum_compression_error_correction(original_filename, compressed_filename, error_corrected_filename)

    # Step 3: Perform post-quantum encryption and secure key storage
    shared_secret_enc, encrypted_shared_secret = pqc_kyber(error_corrected_filename)

    # Step 4: Decrypt the encrypted file
    decrypt_file(error_corrected_filename, decrypted_filename, shared_secret_enc)

    # Step 5: Decompress the file and perform classical error correction
    decompress_and_correct(compressed_filename, final_filename)