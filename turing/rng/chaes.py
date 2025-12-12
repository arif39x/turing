import secrets
import hashlib
from typing import Optional


class ChaCha20RNG:
    __slots__ = ("_counter", "_key", "_nonce")

    def __init__(self, seed: Optional[bytes] = None) -> None:

        if seed is None:
            seed = secrets.token_bytes(32)

        self._key = hashlib.sha256(seed).digest()
        self._nonce = secrets.token_bytes(12)
        self._counter = 0

    def generate(self, length: int) -> bytes:

        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend

        output = bytearray()

        while len(output) < length:
            cipher = Cipher(
                algorithms.ChaCha20(self._key, self._nonce),
                mode=None,
                backend=default_backend()
            )
            encryptor = cipher.encryptor()

            block = encryptor.update(b'\x00' * min(64, length - len(output)))
            output.extend(block)

            self._counter += 1
            self._nonce = (int.from_bytes(self._nonce, 'little') + 1).to_bytes(12, 'little')

        return bytes(output[:length])
