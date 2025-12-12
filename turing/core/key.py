import ctypes
import secrets
from typing import Optional

from turing.core.exceptions import KeyReuseError, KeyLengthError
from turing.utils.burn import secure_zero


class Key:
    __slots__ = ("_data", "_burned", "_length", "_id")

    def __init__(self, data: bytes) -> None:

        if not data:
            raise KeyLengthError("Key data cannot be empty")

        self._length = len(data)
        self._data: Optional[bytearray] = bytearray(data)
        self._burned = False
        self._id = secrets.token_hex(8)

    def raw(self) -> bytes:

        if self._burned or self._data is None:
            raise KeyReuseError(f"Key {self._id} has been burned")
        return bytes(self._data)

    def burn(self) -> None:
        if self._data is not None and not self._burned:
            secure_zero(self._data)
            self._data = None
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
