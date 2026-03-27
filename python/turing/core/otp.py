from turing.core.key import Key
from turing.core.exceptions import KeyLengthError
from turing.turing_core import otp_encrypt as _rs_otp_encrypt
from turing.turing_core import otp_decrypt as _rs_otp_decrypt


def encrypt(plaintext: bytes, key: Key) -> bytes:
    if len(key) < len(plaintext):
        raise KeyLengthError(
            f"Key length ({len(key)}) must be >= plaintext length ({len(plaintext)})"
        )

    key_bytes = key.raw()[:len(plaintext)]
    return bytes(_rs_otp_encrypt(plaintext, key_bytes))


def decrypt(ciphertext: bytes, key: Key) -> bytes:
    if len(key) < len(ciphertext):
        raise KeyLengthError(
            f"Key length ({len(key)}) must be >= ciphertext length ({len(ciphertext)})"
        )

    key_bytes = key.raw()[:len(ciphertext)]
    return bytes(_rs_otp_decrypt(ciphertext, key_bytes))


class OTP:

    __slots__ = ("_key", "_offset")

    def __init__(self, key: Key) -> None:
        self._key = key
        self._offset = 0

    def encrypt(self, plaintext: bytes) -> bytes:
        remaining = len(self._key) - self._offset
        if remaining < len(plaintext):
            raise KeyLengthError(
                f"Insufficient key material: {remaining} bytes remaining, {len(plaintext)} needed"
            )

        key_bytes = self._key.raw()[self._offset:self._offset + len(plaintext)]
        self._offset += len(plaintext)

        return bytes(_rs_otp_encrypt(plaintext, key_bytes))

    def decrypt(self, ciphertext: bytes) -> bytes:

        remaining = len(self._key) - self._offset
        if remaining < len(ciphertext):
            raise KeyLengthError(
                f"Insufficient key material: {remaining} bytes remaining, {len(ciphertext)} needed"
            )

        key_bytes = self._key.raw()[self._offset:self._offset + len(ciphertext)]
        self._offset += len(ciphertext)

        return bytes(_rs_otp_decrypt(ciphertext, key_bytes))

    @property
    def remaining(self) -> int:
        return len(self._key) - self._offset
