use crate::macros::{acquire_lock, bytes_to_string, io_to_py_result, py_none};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use std::sync::{Arc, Mutex};

#[pyclass(subclass)]
pub(crate) struct AsyncStore {
    db: Arc<Mutex<scdb::Store>>,
}

#[pymethods]
impl AsyncStore {
    /// Initializes the Store
    #[args(
        store_path,
        max_keys = "None",
        redundant_blocks = "None",
        pool_capacity = "None",
        compaction_interval = "None"
    )]
    #[new]
    pub fn new(
        store_path: &str,
        max_keys: Option<u64>,
        redundant_blocks: Option<u16>,
        pool_capacity: Option<usize>,
        compaction_interval: Option<u32>,
    ) -> PyResult<Self> {
        let db = io_to_py_result!(scdb::Store::new(
            store_path,
            max_keys,
            redundant_blocks,
            pool_capacity,
            compaction_interval,
        ))?;
        Ok(Self {
            db: Arc::new(Mutex::new(db)),
        })
    }

    /// Sets the given key value in the store
    ///
    /// This is used to insert or update any key-value pair in the store
    pub fn set<'a>(
        &mut self,
        py: Python<'a>,
        k: String,
        v: String,
        ttl: Option<u64>,
    ) -> PyResult<&'a PyAny> {
        let locals = pyo3_asyncio::async_std::get_current_locals(py)?;
        let db = self.db.clone();

        pyo3_asyncio::async_std::future_into_py_with_locals(
            py,
            locals.clone(),
            pyo3_asyncio::async_std::scope(locals, async move {
                let mut db = acquire_lock!(db)?;
                io_to_py_result!(db.set(k.as_bytes(), v.as_bytes(), ttl))?;
                Ok::<Py<PyAny>, PyErr>(py_none!())
            }),
        )
    }

    /// Returns the value corresponding to the given key
    pub fn get<'a>(&mut self, py: Python<'a>, k: String) -> PyResult<&'a PyAny> {
        let locals = pyo3_asyncio::async_std::get_current_locals(py)?;
        let db = self.db.clone();

        pyo3_asyncio::async_std::future_into_py_with_locals(
            py,
            locals.clone(),
            pyo3_asyncio::async_std::scope(locals, async move {
                let mut db = acquire_lock!(db)?;
                let value = io_to_py_result!(db.get(k.as_bytes()))?;

                match value {
                    None => Ok(py_none!()),
                    Some(v) => {
                        let v = bytes_to_string!(v)?;
                        Ok(Python::with_gil(|py| v.into_py(py)))
                    }
                }
            }),
        )
    }

    /// Deletes the key-value for the given key
    pub fn delete<'a>(&mut self, py: Python<'a>, k: String) -> PyResult<&'a PyAny> {
        let locals = pyo3_asyncio::async_std::get_current_locals(py)?;
        let db = self.db.clone();

        pyo3_asyncio::async_std::future_into_py_with_locals(
            py,
            locals.clone(),
            pyo3_asyncio::async_std::scope(locals, async move {
                let mut db = acquire_lock!(db)?;
                io_to_py_result!(db.delete(k.as_bytes()))?;
                Ok::<Py<PyAny>, PyErr>(py_none!())
            }),
        )
    }

    /// Clears all data in the store
    pub fn clear<'a>(&mut self, py: Python<'a>) -> PyResult<&'a PyAny> {
        let locals = pyo3_asyncio::async_std::get_current_locals(py)?;
        let db = self.db.clone();

        pyo3_asyncio::async_std::future_into_py_with_locals(
            py,
            locals.clone(),
            pyo3_asyncio::async_std::scope(locals, async move {
                let mut db = acquire_lock!(db)?;
                io_to_py_result!(db.clear())?;
                Ok::<Py<PyAny>, PyErr>(py_none!())
            }),
        )
    }

    /// Manually removes dangling key-value pairs in the database file. Like vacuuming.
    pub fn compact<'a>(&mut self, py: Python<'a>) -> PyResult<&'a PyAny> {
        let locals = pyo3_asyncio::async_std::get_current_locals(py)?;
        let db = self.db.clone();

        pyo3_asyncio::async_std::future_into_py_with_locals(
            py,
            locals.clone(),
            pyo3_asyncio::async_std::scope(locals, async move {
                let mut db = acquire_lock!(db)?;
                io_to_py_result!(db.compact())?;
                Ok::<Py<PyAny>, PyErr>(py_none!())
            }),
        )
    }
}
