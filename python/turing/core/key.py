import secrets
from typing import Optional

from turing.core.exceptions import KeyReuseError, KeyLengthError


class Key:
    __slots__ = ("_secret_key", "_burned", "_length", "_id")

    def __init__(self, data: bytes) -> None:
        self._burned = False
        self._id = secrets.token_hex(8)
        self._secret_key = None

        if not data:
            raise KeyLengthError("Key data cannot be empty")

        from turing.turing_core import SecretKey

        self._length = len(data)
        self._secret_key = SecretKey(data)

    def raw(self) -> bytes:

        if self._burned:
            raise KeyReuseError(f"Key {self._id} has been burned")
        try:
            return self._secret_key.raw_bytes()
        except RuntimeError:
            raise KeyReuseError(f"Key {self._id} has been burned")

    def burn(self) -> None:
        if not self._burned:
            if getattr(self, '_secret_key', None):
                self._secret_key.burn()
            self._burned = True

    def __len__(self) -> int:
        return self._length

    def __del__(self) -> None:
        self.burn()

    def __repr__(self) -> str:
        status = "BURNED" if self._burned else "ACTIVE"
        return f"<Key id={self._id} length={self._length} status={status}>"


class KeyPair:
    __slots__ = ("send_key", "recv_key")

    def __init__(self, send_key: Key, recv_key: Key) -> None:
        self.send_key = send_key
        self.recv_key = recv_key

    def burn(self) -> None:
        self.send_key.burn()
        self.recv_key.burn()

    def __del__(self) -> None:
        self.burn()
