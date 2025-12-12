import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from turing.cli.style import error, success, warning, info
from turing.core.otp import encrypt, decrypt
from turing.core.key import Key
from turing.core.exceptions import TuringError
from turing.rng.provider import RNGProvider
from turing.vault.manager import VaultManager
from turing.config import Config

app = typer.Typer(
    name="turing",
    help="TURING: Cryptographically pure One-Time Pad system",
    add_completion=False,
)
console = Console()


@app.command(name="encrypt")  # Add name parameter
def encrypt_cmd(
    message: str = typer.Argument(..., help="Message to encrypt"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
    paranoia: str = typer.Option("high", "--paranoia", help="Paranoia level: low/high/nuclear"),
    qr: bool = typer.Option(False, "--qr", help="Use quantum RNG"),
    burn_after: bool = typer.Option(False, "--burn-after", help="Destroy key after use"),
    vault: Optional[str] = typer.Option(None, "--vault", help="Vault name for key storage"),
) -> None:
    try:
        config = Config.from_paranoia(paranoia)
        provider = RNGProvider(use_qrng=qr, config=config)

        message_bytes = message.encode("utf-8")
        key_material = provider.generate(len(message_bytes))
        key = Key(key_material)

        ciphertext = encrypt(message_bytes, key)

        if vault:
            vm = VaultManager(config)
            vm.store_key(vault, key, burn_after=burn_after)

        if output:
            output.write_bytes(ciphertext)
            success(f"Encrypted to {output}")
        else:
            console.print(ciphertext.hex())

        if not burn_after and not vault:
            warning("Key not stored. Manual key management required.")
            console.print(f"Key (hex): {key.raw().hex()}")

    except TuringError as e:
        error(str(e))
        sys.exit(1)
    except Exception as e:
        error(f"Unexpected error: {e}")
        sys.exit(2)


@app.command(name="decrypt")  # Add name parameter
def decrypt_cmd(
    ciphertext_hex: str = typer.Argument(..., help="Ciphertext in hex"),
    key_hex: Optional[str] = typer.Option(None, "--key", help="Key in hex"),
    vault: Optional[str] = typer.Option(None, "--vault", help="Vault name for key retrieval"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
) -> None:
    try:
        ciphertext = bytes.fromhex(ciphertext_hex)

        if vault:
            config = Config()
            vm = VaultManager(config)
            key = vm.retrieve_key(vault)
        elif key_hex:
            key = Key(bytes.fromhex(key_hex))
        else:
            error("Must provide --key or --vault")
            sys.exit(1)

        plaintext = decrypt(ciphertext, key)

        if output:
            output.write_bytes(plaintext)
            success(f"Decrypted to {output}")
        else:
            console.print(plaintext.decode("utf-8"))

    except TuringError as e:
        error(str(e))
        sys.exit(1)
    except Exception as e:
        error(f"Unexpected error: {e}")
        sys.exit(2)


@app.command()
def keygen(
    length: int = typer.Argument(..., help="Key length in bytes"),
    output: Path = typer.Option(..., "--output", "-o", help="Output file"),
    qr: bool = typer.Option(False, "--qr", help="Use quantum RNG"),
    paranoia: str = typer.Option("high", "--paranoia", help="Paranoia level"),
) -> None:

    try:
        config = Config.from_paranoia(paranoia)
        provider = RNGProvider(use_qrng=qr, config=config)
        key_material = provider.generate(length)

        output.write_bytes(key_material)
        success(f"Generated {length}-byte key to {output}")

    except Exception as e:
        error(f"Key generation failed: {e}")
        sys.exit(1)


@app.command()
def vault_init(
    name: str = typer.Argument(..., help="Vault name"),
    passphrase: bool = typer.Option(True, "--passphrase", help="Use passphrase encryption"),
    shamir: Optional[int] = typer.Option(None, "--shamir", help="Shamir threshold (e.g., 3 for 3-of-5)"),
) -> None:
    try:
        config = Config()
        vm = VaultManager(config)
        vm.create_vault(name, use_passphrase=passphrase, shamir_threshold=shamir)
        success(f"Vault '{name}' created")

    except Exception as e:
        error(f"Vault creation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    app()
