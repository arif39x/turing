from typing import Optional

from turing.config import Config
from turing.rng.system import SystemRNG
from turing.rng.chaes import ChaCha20RNG
from turing.rng.qrng.anu import ANURNG
from turing.core.exceptions import RNGError


class RNGProvider:

    def __init__(self, use_qrng: bool = False, config: Optional[Config] = None) -> None:
        self.config = config or Config()
        self.use_qrng = use_qrng

        self._system_rng = SystemRNG()
        self._chacha_rng = ChaCha20RNG()
        self._qrng = ANURNG(timeout=self.config.qrng_timeout) if use_qrng else None

    def generate(self, length: int) -> bytes:
        if self.use_qrng and self._qrng:
            try:
                return self._qrng.generate(length)
            except Exception:
                pass

        try:
            return self._system_rng.generate(length)
        except Exception:
            pass

        try:
            return self._chacha_rng.generate(length)
        except Exception as e:
            raise RNGError(f"All RNG sources failed: {e}")
