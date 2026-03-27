from typing import Optional
from pathlib import Path

from turing.core.exceptions import HSMError
from turing.core.key import Key


class PKCS11HSM:

    def __init__(self, library_path: str, pin: str, slot: int = 0) -> None:
        self.library_path = library_path
        self.pin = pin
        self.slot = slot

    def generate_key(self, length: int) -> Key:
        raise NotImplementedError("PKCS#11 requires python-pkcs11 library")

    def store_key(self, key: Key, label: str) -> None:
        raise NotImplementedError("PKCS#11 requires python-pkcs11 library")

    def retrieve_key(self, label: str) -> Key:
        raise NotImplementedError("PKCS#11 requires python-pkcs11 library")
