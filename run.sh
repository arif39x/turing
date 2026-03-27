#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"

VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "[*] No virtual environment found. Initializing..."
    python3 -m venv "$VENV_DIR"
    
    echo "[*] Installing dependencies..."
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install maturin
    
    echo "[*] Compiling the Rust cryptographic core..."
    pip install -e .
    maturin develop --release
    echo "[+] Build complete!"
    echo "------------------------------------------------"
else
    source "$VENV_DIR/bin/activate"
fi

if [ $# -eq 0 ]; then
    turing --help
else
    turing "$@"
fi
