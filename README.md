# Post-Quantum Encryption Management System
---
## Project Goals
  
The goals of this project are simple in theory, yet difficult in practice: To provide an all-inclusive management system for data 
security based around the NIST Post-Quantum Cryptography Standards, whether it be for entries in a database or for files themselves. 
  
To do this, we use old ideas, but with a new twist. For example, the old idea is that one should use a key-pair (public key, private key) 
to "lock" the encryption so that one needs the keys in order to decrypt the data.  
  
- Key-pair generation: Rather than using the classical RSA or Diffie-Hellman for key generation, we will instead use Kyber.
- Key storage: Storage of the keys should use TPM2.0 modules or failing that,  either Windows DPAPI, Linux LibSecret, or Apple Keychain.
- Encryption/Decryption: Encryption of the data will use RLWE, Ring Learning with Errors.
  
---
  
## Windows Installation (via WSL2)

### Prerequisites

This project requires the NVIDIA CUDA Tookkit and **WSL2** (Windows Subsystem for Linux 2.0) to run Linux-based packages and to build tpm2-tss.

### Steps to Install CUDA Toolkit

1. Visit NVIDIA's website at: https://developer.nvidia.com/cuda-downloads

2. Download and install the CUDA Toolkit for your system (Linux or Windows)

### Steps to Install `tpm2-tss`

1. Launch PowerShell with admin priviledges and install pkgconfiglite using the following:
    ```bash
    choco install pkgconfiglite

1. **Enable the Universe Repository in WSL**

    Open your WSL Ubuntu terminal and run the following command to enable the Universe repository, which is necessary for some of the dependencies:

    ```bash
    sudo add-apt-repository universe
    sudo apt-get update

2. **Install Required Dependencies**

    Install all the required dependencies by running:
    ```bash
    sudo apt-get install autoconf-archive autoconf automake libtool pkg-config gcc libssl-dev libjson-c-dev libcurl4-openssl-dev uuid-dev pkgconf

3. **Clone the TPM2-TSS Repository**

    Clone the tpm2-tss GitHub repository to your local machine:
    ```bash
    git clone https://github.com/tpm2-software/tpm2-tss.git
    cd tpm2-tss

4. **Build and Install tpm2-tss**

    Run the following commands to build and install tpm2-tss:
    ```bash
    ./bootstrap
    ./configure
    make -j$(nproc)
    sudo make install
    sudo ldconfig
    ```

    The sudo ldconfig command refreshes the shared library cache to ensure that your system recognizes the newly installed library.


### Notes:

- It's important to emphasize that **WSL2** must be installed on Windows before running these commands.
