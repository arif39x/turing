use pyo3::prelude::*;
use subtle::ConstantTimeEq;

#[pyfunction]
pub fn xor_bytes(a: &[u8], b: &[u8]) -> PyResult<Vec<u8>> {
    if a.len() != b.len() {
        return Err(pyo3::exceptions::PyValueError::new_err("constant_time_xor requires equal length inputs"));
    }
    
    let result: Vec<u8> = a.iter().zip(b.iter()).map(|(x, y)| x ^ y).collect();
    Ok(result)
}

#[pyfunction]
pub fn ct_eq(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() {
        return false;
    }
    a.ct_eq(b).into()
}
