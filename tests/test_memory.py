import pytest
from turing.core.memory import mlock_memory, munlock_memory

def test_mlock_munlock():
    data = bytearray(b"test1234")
    # depending on OS limits, this might return True or False, but it shouldn't crash
    res = mlock_memory(data)
    assert isinstance(res, bool)
    
    res2 = munlock_memory(data)
    assert isinstance(res2, bool)


