mod async_store;
mod macros;
mod store;

use crate::async_store::AsyncStore;
use crate::store::Store;
use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
fn py_scdb(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Store>()?;
    m.add_class::<AsyncStore>()?;
    Ok(())
}
