import qrcode
from pathlib import Path
from typing import Optional

from turing.core.key import Key


class OfflineTransport:
    @staticmethod
    def export_file(key: Key, path: Path) -> None:

        path.write_bytes(key.raw())
        path.chmod(0o600)

    @staticmethod
    def import_file(path: Path) -> Key:

        return Key(path.read_bytes())

    @staticmethod
    def export_qr(key: Key, output_path: Optional[Path] = None) -> None:

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(key.raw().hex())
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        if output_path:
            img.save(output_path)
        else:
            img.show()
