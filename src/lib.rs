mod store;
mod async_store;

use pyo3::prelude::*;
use crate::async_store::AsyncStore;
use crate::store::Store;

/// A Python module implemented in Rust.
#[pymodule]
fn py_scdb(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Store>()?;
    m.add_class::<AsyncStore>()?;
    Ok(())
}