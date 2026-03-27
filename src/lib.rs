use pyo3::prelude::*;

mod memory;
mod crypto;

#[pymodule]
fn turing_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<memory::secret::SecretKey>()?;
    m.add_function(wrap_pyfunction!(crypto::xor::xor_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(crypto::xor::ct_eq, m)?)?;
    m.add_function(wrap_pyfunction!(crypto::otp::otp_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(crypto::otp::otp_decrypt, m)?)?;
    m.add_function(wrap_pyfunction!(memory::mlock::mlock, m)?)?;
    m.add_function(wrap_pyfunction!(memory::mlock::munlock, m)?)?;
    Ok(())
}
