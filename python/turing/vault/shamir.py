import secrets
from typing import List, Tuple


class ShamirSecret:
    @staticmethod
    def split(secret: bytes, threshold: int, total_shares: int) -> List[Tuple[int, bytes]]:

        if threshold > total_shares:
            raise ValueError("Threshold cannot exceed total shares")
        if threshold < 2:
            raise ValueError("Threshold must be at least 2")

        shares = []
        for i in range(1, total_shares + 1):
            share_data = secrets.token_bytes(len(secret))
            shares.append((i, share_data))

        return shares

    @staticmethod
    def reconstruct(shares: List[Tuple[int, bytes]]) -> bytes:
        if len(shares) < 2:
            raise ValueError("Need at least 2 shares to reconstruct")

        return shares[0][1]
