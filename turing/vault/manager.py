import json
from pathlib import Path
from typing import Optional, Dict
import getpass

from turing.config import Config
from turing.core.key import Key
from turing.core.exceptions import VaultError
from turing.vault.age import AgeEncryption
from turing.vault.shamir import ShamirSecret


class VaultManager:
    def __init__(self, config: Optional[Config] = None) -> None:

        self.config = config or Config()
        self.vault_dir = self.config.vault_dir
        self.vault_dir.mkdir(parents=True, exist_ok=True)

    def create_vault(
            self,
            name: str,
            use_passphrase: bool = True,
            shamir_threshold: Optional[int] = None
    ) -> None:
        vault_path = self.vault_dir / name
        vault_path.mkdir(exist_ok=True)

        metadata = {
            "name": name,
            "use_passphrase": use_passphrase,
            "shamir_threshold": shamir_threshold,
        }

        (vault_path / "metadata.json").write_text(json.dumps(metadata))

    def store_key(
            self,
            vault_name: str,
            key: Key,
            burn_after: bool = False
    ) -> None:
        vault_path = self.vault_dir / vault_name
        if not vault_path.exists():
            raise VaultError(f"Vault '{vault_name}' does not exist")

        metadata = json.loads((vault_path / "metadata.json").read_text())

        key_file = vault_path / f"key_{key._id}.bin"
        key_file.write_bytes(key.raw())

        if metadata["use_passphrase"]:
            passphrase = getpass.getpass("Enter vault passphrase: ")
            encrypted_file = vault_path / f"key_{key._id}.age"

            AgeEncryption.encrypt_file(key_file, encrypted_file, passphrase=passphrase)
            key_file.unlink()

        if burn_after:
            key.burn()

    def retrieve_key(self, vault_name: str, key_id: Optional[str] = None) -> Key:
        vault_path = self.vault_dir / vault_name
        if not vault_path.exists():
            raise VaultError(f"Vault '{vault_name}' does not exist")

        metadata = json.loads((vault_path / "metadata.json").read_text())

        if key_id:
            encrypted_file = vault_path / f"key_{key_id}.age"
        else:
            age_files = list(vault_path.glob("key_*.age"))
            if not age_files:
                raise VaultError("No keys found in vault")
            encrypted_file = age_files[-1]

        if metadata["use_passphrase"]:
            passphrase = getpass.getpass("Enter vault passphrase: ")
            decrypted_file = encrypted_file.with_suffix(".bin")

            AgeEncryption.decrypt_file(encrypted_file, decrypted_file, passphrase=passphrase)
            key_data = decrypted_file.read_bytes()
            decrypted_file.unlink()

            return Key(key_data)

        raise VaultError("Non-passphrase vaults not yet implemented")
