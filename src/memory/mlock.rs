use pyo3::prelude::*;
use pyo3::buffer::PyBuffer;

#[pyfunction]
pub fn mlock(data: &Bound<'_, pyo3::types::PyAny>) -> PyResult<bool> {
    let buf = PyBuffer::<u8>::get_bound(data)?;
    #[cfg(unix)]
    {
        let ptr = buf.buf_ptr();
        let len = buf.len_bytes();
        Ok(unsafe { libc::mlock(ptr, len) == 0 })
    }
    #[cfg(not(unix))]
    {
        Ok(false)
    }
}

#[pyfunction]
pub fn munlock(data: &Bound<'_, pyo3::types::PyAny>) -> PyResult<bool> {
    let buf = PyBuffer::<u8>::get_bound(data)?;
    #[cfg(unix)]
    {
        let ptr = buf.buf_ptr();
        let len = buf.len_bytes();
        Ok(unsafe { libc::munlock(ptr, len) == 0 })
    }
    #[cfg(not(unix))]
    {
        Ok(false)
    }
}
