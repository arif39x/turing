use pyo3::prelude::*;

#[pyfunction]
pub fn otp_encrypt(plaintext: &[u8], key: &[u8]) -> PyResult<Vec<u8>> {
    if plaintext.len() > key.len() {
        return Err(pyo3::exceptions::PyValueError::new_err("Key length must be >= plaintext length"));
    }
    
    // OTP uses XOR, which is its own inverse, but we wrap the subtlety anyway just in case
    let result: Vec<u8> = plaintext.iter().zip(key.iter()).map(|(p, k)| p ^ k).collect();
    Ok(result)
}

#[pyfunction]
pub fn otp_decrypt(ciphertext: &[u8], key: &[u8]) -> PyResult<Vec<u8>> {
    if ciphertext.len() > key.len() {
        return Err(pyo3::exceptions::PyValueError::new_err("Key length must be >= ciphertext length"));
    }
    
    let result: Vec<u8> = ciphertext.iter().zip(key.iter()).map(|(c, k)| c ^ k).collect();
    Ok(result)
}
