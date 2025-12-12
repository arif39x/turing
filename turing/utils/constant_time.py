import ctypes


def constant_time_xor(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise ValueError("constant_time_xor requires equal length inputs")

    result = bytearray(len(a))

    for i in range(len(a)):
        result[i] = a[i] ^ b[i]

    return bytes(result)


def constant_time_compare(a: bytes, b: bytes) -> bool:
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a, b):
        result |= x ^ y

    return result == 0
