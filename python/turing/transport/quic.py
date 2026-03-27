import asyncio
from pathlib import Path
from typing import Optional

from aioquic.asyncio import connect, serve
from aioquic.quic.configuration import QuicConfiguration

from turing.core.key import Key


class QUICTransport:
    def __init__(self, cert_path: Optional[Path] = None, key_path: Optional[Path] = None) -> None:
        self.cert_path = cert_path
        self.key_path = key_path

    async def send_key(self, key: Key, host: str, port: int) -> None:

        raise NotImplementedError("QUIC transport requires full aioquic integration")

    async def receive_key(self, host: str, port: int) -> Key:

        raise NotImplementedError("QUIC transport requires full aioquic integration")
