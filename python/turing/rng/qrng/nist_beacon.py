import requests
import hashlib

from turing.core.exceptions import RNGError


class NISTBeaconRNG:
    def __init__(self, timeout: int = 10) -> None:

        self.base_url = "https://beacon.nist.gov/beacon/2.0/chain/last/pulse"
        self.timeout = timeout

    def generate(self, length: int) -> bytes:

        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            output_value = data["pulse"]["outputValue"]

            result = bytearray()
            counter = 0

            while len(result) < length:
                h = hashlib.sha256(f"{output_value}{counter}".encode()).digest()
                result.extend(h)
                counter += 1

            return bytes(result[:length])

        except Exception as e:
            raise RNGError(f"NIST Beacon failed: {e}")
