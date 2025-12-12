from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Config:

    vault_dir: Path = Path.home() / ".turing" / "vaults"
    audit_log: Path = Path.home() / ".turing" / "audit.log"

    mlock_enabled: bool = True
    constant_time_validation: bool = True

    qrng_timeout: int = 10
    qrng_anu_url: str = "https://qrng.anu.edu.au/API/jsonI.php?length=1024&type=hex16"
    qrng_idq_url: str = "https://api.idquantique.com/v1/random"
    qrng_nist_url: str = "https://beacon.nist.gov/beacon/2.0/chain/last/pulse"

    chacha_rounds: int = 20

    hsm_enabled: bool = False
    hsm_pkcs11_lib: Optional[str] = None
    hsm_pin: Optional[str] = None

    shamir_total_shares: int = 5
    shamir_threshold: int = 3

    burn_on_error: bool = True

    @classmethod
    def from_paranoia(cls, level: str) -> "Config":
        if level == "nuclear":
            return cls(
                mlock_enabled=True,
                constant_time_validation=True,
                qrng_timeout=30,
                chacha_rounds=20,
                burn_on_error=True,
            )
        elif level == "high":
            return cls(
                mlock_enabled=True,
                constant_time_validation=True,
                burn_on_error=True,
            )
        else:
            return cls(
                mlock_enabled=False,
                constant_time_validation=True,
                burn_on_error=False,
            )
