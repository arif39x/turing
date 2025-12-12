import ctypes
import sys
from typing import Union


def secure_zero(data: Union[bytearray, memoryview]) -> None:

    if not isinstance(data, (bytearray, memoryview)):
        raise TypeError("secure_zero requires bytearray or memoryview")

    length = len(data)

    if isinstance(data, bytearray):
        ptr = (ctypes.c_char * length).from_buffer(data)
        ctypes.memset(ptr, 0, length)
    else:
        for i in range(length):
            data[i] = 0


def mlock_memory(data: bytearray) -> bool:

    if sys.platform == "win32":
        return False

    try:
        import mmap
        length = len(data)
        ptr = (ctypes.c_char * length).from_buffer(data)
        addr = ctypes.addressof(ptr)

        libc = ctypes.CDLL(None)
        result = libc.mlock(addr, length)
        return result == 0
    except Exception:
        return False


def munlock_memory(data: bytearray) -> bool:
    if sys.platform == "win32":
        return False

    try:
        length = len(data)
        ptr = (ctypes.c_char * length).from_buffer(data)
        addr = ctypes.addressof(ptr)

        libc = ctypes.CDLL(None)
        result = libc.munlock(addr, length)
        return result == 0
    except Exception:
        return False
