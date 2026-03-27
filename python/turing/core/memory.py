import sys

from turing.turing_core import mlock as _rs_mlock
from turing.turing_core import munlock as _rs_munlock

def mlock_memory(data: bytearray) -> bool:
    if sys.platform == "win32":
        return False
    try:
        return _rs_mlock(data)
    except Exception:
        return False

def munlock_memory(data: bytearray) -> bool:
    if sys.platform == "win32":
        return False
    try:
        return _rs_munlock(data)
    except Exception:
        return False
