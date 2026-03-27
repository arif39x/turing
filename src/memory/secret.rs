use pyo3::prelude::*;
use zeroize::Zeroizing;

#[pyclass]
pub struct SecretKey {
    data: Option<Zeroizing<Vec<u8>>>,
}

#[pymethods]
impl SecretKey {
    #[new]
    pub fn new(data: &[u8]) -> Self {
        SecretKey {
            data: Some(Zeroizing::new(data.to_vec())),
        }
    }

    pub fn raw_bytes<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, pyo3::types::PyBytes>> {
        match &self.data {
            Some(d) => Ok(pyo3::types::PyBytes::new(py, d.as_slice())),
            None => Err(pyo3::exceptions::PyRuntimeError::new_err("Key has been burned")),
        }
    }

    pub fn burn(&mut self) {
        self.data = None;
    }

    pub fn __len__(&self) -> usize {
        match &self.data {
            Some(d) => d.len(),
            None => 0,
        }
    }
}
