import secrets


class SystemRNG:

    def generate(self, length: int) -> bytes:
        return secrets.token_bytes(length)
