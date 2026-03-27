import pytest
from turing.core.key import Key
from turing.core.otp import encrypt, decrypt, OTP
from turing.core.exceptions import KeyLengthError

def test_otp_module_level():
    k = Key(b"test1234")
    pt = b"msg!"
    ct = encrypt(pt, k)
    assert decrypt(ct, k) == pt

    with pytest.raises(KeyLengthError):
        encrypt(b"toolongmsg", k)

def test_otp_class():
    k = Key(b"test1234")
    otp = OTP(k)
    assert otp.remaining == 8
    
    ct1 = otp.encrypt(b"msg")
    assert otp.remaining == 5
    
    otp_dec = OTP(k)
    assert otp_dec.decrypt(ct1) == b"msg"
    
    with pytest.raises(KeyLengthError):
        otp.encrypt(b"tooooooo_long")
