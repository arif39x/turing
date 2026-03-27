import pytest
from turing.core.key import Key
from turing.core.exceptions import KeyReuseError, KeyLengthError

def test_key_basic():
    k = Key(b"test1234")
    assert len(k) == 8
    assert k.raw() == b"test1234"
    k.burn()
    with pytest.raises(KeyReuseError):
        k.raw()

def test_key_empty():
    with pytest.raises(KeyLengthError):
        Key(b"")
