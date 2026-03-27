import requests
from typing import Optional

from turing.core.exceptions import RNGError


class IDQuantiqueRNG:


    def __init__(self, api_key: str, timeout: int = 10) -> None:

        self.api_key = api_key
        self.base_url = "https://api.idquantique.com/v1/random"
        self.timeout = timeout

    def generate(self, length: int) -> bytes:

        try:
            response = requests.get(
                self.base_url,
                params={"length": length},
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.content[:length]

        except Exception as e:
            raise RNGError(f"IDQuantique QRNG failed: {e}")
