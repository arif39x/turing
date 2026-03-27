# TURING: Cryptographically Pure One-Time Pad (Rust/Python Hybrid)

> **Note:** This project is a hybrid Python and Rust `maturin` library. It guarantees hardware-level constant-time execution and strict memory wipe security via `pyo3`, `zeroize`, and the `subtle` crates.

## What is this?

TURING is a command-line tool that implements the **One-Time Pad (OTP)** encryption protocol—the only mathematically proven unbreakable encryption method (perfect secrecy) when deployed correctly.

TURING solves the biggest engineering weaknesses of traditional software OTP tools by pushing all performance-sensitive and memory-sensitive operations to a natively compiled **Rust core**:

- **Absolutely Constant-Time Operations:** Cryptographic XOR primitives are backed by the Rust `subtle` crate to proactively prevent timing side-channel attacks across native pointers.
- **Hardware Memory Pining & Wiping:** Secret keys the Python Garbage Collector typically leaves lingering in unallocated RAM are strictly eliminated using automatic structural drops via the `zeroize` crate, backed directly by underlying POSIX `mlock()` and `munlock()` syscalls.

## Purpose and Use Cases

TURING is built to safeguard short, extremely sensitive snippets of data over fully compromised internet networks where post-quantum confidentiality must be guaranteed.

**Primary Use Cases:**

- **Whistleblowing & Journalism:** Protect highly volatile diplomatic/source text where metadata interception is absolute.
- **"Store Now, Decrypt Later" Threats:** OTP is completely unsusceptible to future offline quantum computer decryption.
- **Root-of-Trust Distribution:** Exchanging asymmetric master keys, sensitive corporate credential dumps, seed phrases, or HSM pins.
- **Experimental Cryptography:** Leverages integrations like local Hardware Security Modules (YubiHSM/PKCS11) or cloud-based True Quantum Random Number Generators (QRNG).

## Installation & Build

For local development build, ensure you have the Rust toolchain (`cargo`) and Python 3.12+ installed.

```bash
# Set up a fresh Python sandbox environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and build the Rust extension natively
pip install maturin
pip install -e .
maturin develop --release
```

_Note: Packaged binary Python wheel formats are automatically compiled and attached dynamically in release pipelines, allowing end-users to just `pip install turing` directly without Rust installed._

## Usage Commands

TURING ships with an intuitive, colorful CLI.

### **1. Encryption**

**Basic encryption strings (Outputs raw hex):**

```bash
turing encrypt "Secret message" --paranoia high
```

**Save the ciphertext raw binary directly to a file:**

```bash
turing encrypt "Classified data" -o encrypted.bin --paranoia nuclear
```

**Sample true randomness from a Quantum RNG endpoint:**

```bash
turing encrypt "Top secret!" --qr --paranoia nuclear
```

**Generate the key and automatically store it in your Turing vault:**

```bash
turing encrypt "Message" --vault my_vault --burn-after
```

**Full featured end-to-end encryption pipeline:**

```bash
turing encrypt "Hello World" -o cipher.bin --paranoia high --qr --vault secure --burn-after
```

### **2. Decryption**

**Decrypt using a provided raw Hex Key in memory:**

```bash
turing decrypt a3f2e1d4... --key 9b8c7d6e...
```

**Decrypt ciphertext using an exact Key retrieved dynamically from your Vault:**

```bash
turing decrypt a3f2e1d4... --vault my_vault
```

**Decrypt from file sources directly and safely export plaintext:**

```bash
turing decrypt $(cat cipher.hex) --key $(cat key.hex) -o plaintext.txt
```

### **3. Key Generation & Vaults**

**Generate a stand-alone key with specific byte lengths:**

```bash
turing keygen 256 -o my_key.bin --qr --paranoia high
```

**Initialize a new secure local key Vault:**

```bash
turing vault-init my_vault --passphrase --shamir 3
```
