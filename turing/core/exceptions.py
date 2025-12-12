class TuringError(Exception):
    pass


class KeyLengthError(TuringError):
    pass


class KeyReuseError(TuringError):
    pass


class ValidationError(TuringError):
    pass


class VaultError(TuringError):
    pass


class RNGError(TuringError):
    pass


class HSMError(TuringError):
    pass