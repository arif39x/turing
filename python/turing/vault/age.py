import subprocess
from pathlib import Path
from typing import Optional

from turing.core.exceptions import VaultError


class AgeEncryption:

    @staticmethod
    def encrypt_file(
            input_path: Path,
            output_path: Path,
            passphrase: Optional[str] = None,
            recipient: Optional[str] = None
    ) -> None:

        try:
            cmd = ["age", "-o", str(output_path)]

            if passphrase:
                cmd.extend(["-p"])
                proc = subprocess.Popen(
                    cmd + [str(input_path)],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                proc.communicate(input=passphrase.encode())
            elif recipient:
                cmd.extend(["-r", recipient, str(input_path)])
                subprocess.run(cmd, check=True, capture_output=True)
            else:
                raise VaultError("Must provide passphrase or recipient")

        except subprocess.CalledProcessError as e:
            raise VaultError(f"age encryption failed: {e}")

    @staticmethod
    def decrypt_file(
            input_path: Path,
            output_path: Path,
            passphrase: Optional[str] = None,
            identity_path: Optional[Path] = None
    ) -> None:
        try:
            cmd = ["age", "-d", "-o", str(output_path)]

            if passphrase:
                proc = subprocess.Popen(
                    cmd + [str(input_path)],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                proc.communicate(input=passphrase.encode())
            elif identity_path:
                cmd.extend(["-i", str(identity_path), str(input_path)])
                subprocess.run(cmd, check=True, capture_output=True)
            else:
                raise VaultError("Must provide passphrase or identity")

        except subprocess.CalledProcessError as e:
            raise VaultError(f"age decryption failed: {e}")
