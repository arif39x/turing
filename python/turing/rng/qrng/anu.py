import requests
from typing import Optional

from turing.core.exceptions import RNGError


class ANURNG:

    def __init__(self, timeout: int = 10) -> None:

        self.base_url = "https://qrng.anu.edu.au/API/jsonI.php"
        self.timeout = timeout

    def generate(self, length: int) -> bytes:

        try:
            blocks_needed = (length + 1023) // 1024
            result = bytearray()

            for _ in range(blocks_needed):
                response = requests.get(
                    self.base_url,
                    params={"length": 1024, "type": "hex16"},
                    timeout=self.timeout
                )
                response.raise_for_status()

                data = response.json()
                if not data.get("success"):
                    raise RNGError("ANU QRNG returned failure")

                hex_data = "".join(data["data"])
                result.extend(bytes.fromhex(hex_data))

            return bytes(result[:length])

        except Exception as e:
            raise RNGError(f"ANU QRNG failed: {e}")
