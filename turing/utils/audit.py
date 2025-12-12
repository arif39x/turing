import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from turing.config import Config


class AuditLogger:

    def __init__(self, config: Optional[Config] = None) -> None:
        self.config = config or Config()
        self.config.audit_log.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("turing.audit")
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler(self.config.audit_log)
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        )
        self.logger.addHandler(handler)

    def log_key_generation(self, key_id: str, length: int, source: str) -> None:

        self.logger.info(
            f"KEY_GEN | id={key_id} | length={length} | source={source}"
        )

    def log_encryption(self, key_id: str, message_length: int) -> None:
        self.logger.info(
            f"ENCRYPT | key_id={key_id} | msg_len={message_length}"
        )

    def log_decryption(self, key_id: str, message_length: int) -> None:

        self.logger.info(
            f"DECRYPT | key_id={key_id} | msg_len={message_length}"
        )

    def log_key_burn(self, key_id: str) -> None:
        self.logger.warning(f"KEY_BURN | id={key_id}")

    def log_error(self, operation: str, error: str) -> None:
        self.logger.error(f"ERROR | op={operation} | error={error}")
