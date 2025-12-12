from typing import Optional

from turing.core.exceptions import HSMError
from turing.core.key import Key


class YubiHSM:
    def __init__(self, connector_url: str = "http://localhost:12345", auth_key: int = 1,
                 password: str = "password") -> None:

        self.connector_url = connector_url
        self.auth_key = auth_key
        self.password = password

    def generate_key(self, length: int) -> Key:
        raise NotImplementedError("YubiHSM requires yubihsm library")

    def store_key(self, key: Key, object_id: int) -> None:
        raise NotImplementedError("YubiHSM requires yubihsm library")

    def retrieve_key(self, object_id: int) -> Key:
        raise NotImplementedError("YubiHSM requires yubihsm library")
