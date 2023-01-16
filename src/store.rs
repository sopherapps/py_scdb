use crate::macros::{bytes_to_string, io_to_py_result};
use pyo3::prelude::*;

#[pyclass(subclass)]
pub(crate) struct Store {
    db: scdb::Store,
}

#[pymethods]
impl Store {
    /// Initializes the Store
    #[args(
        store_path,
        max_keys = "None",
        redundant_blocks = "None",
        pool_capacity = "None",
        compaction_interval = "None",
        is_search_enabled = "false"
    )]
    #[new]
    pub fn new(
        store_path: &str,
        max_keys: Option<u64>,
        redundant_blocks: Option<u16>,
        pool_capacity: Option<usize>,
        compaction_interval: Option<u32>,
        is_search_enabled: bool,
    ) -> PyResult<Self> {
        let db = io_to_py_result!(scdb::Store::new(
            store_path,
            max_keys,
            redundant_blocks,
            pool_capacity,
            compaction_interval,
            is_search_enabled,
        ))?;
        Ok(Self { db })
    }

    /// Sets the given key value in the store
    ///
    /// This is used to insert or update any key-value pair in the store
    pub fn set(&mut self, k: &str, v: &str, ttl: Option<u64>) -> PyResult<()> {
        io_to_py_result!(self.db.set(k.as_bytes(), v.as_bytes(), ttl))
    }

    /// Returns the value corresponding to the given key
    pub fn get(&mut self, py: Python, k: &str) -> PyResult<Py<PyAny>> {
        let value = io_to_py_result!(self.db.get(k.as_bytes()))?;
        match value {
            None => Ok(py.None()),
            Some(v) => {
                let v = bytes_to_string!(v)?;
                Ok(v.into_py(py))
            }
        }
    }

    /// Searches for key-values whose key start with the given `term`.
    ///
    /// In order to do pagination, we use `skip` to skip the first `skip` records
    /// and `limit` to return not more than the given number of items
    pub fn search(&mut self, term: &str, skip: u64, limit: u64) -> PyResult<Vec<(String, String)>> {
        let res = self.db.search(term.as_bytes(), skip, limit);
        let res: Vec<(Vec<u8>, Vec<u8>)> = io_to_py_result!(res)?;
        res.into_iter().map(|(k, v)| {
            let k = bytes_to_string!(k)?;
            let v = bytes_to_string!(v)?;
            Ok((k, v))
        }).collect()
    }

    /// Deletes the key-value for the given key
    pub fn delete(&mut self, k: &str) -> PyResult<()> {
        io_to_py_result!(self.db.delete(k.as_bytes()))
    }

    /// Clears all data in the store
    pub fn clear(&mut self) -> PyResult<()> {
        io_to_py_result!(self.db.clear())
    }

    /// Manually removes dangling key-value pairs in the database file. Like vacuuming.
    pub fn compact(&mut self) -> PyResult<()> {
        io_to_py_result!(self.db.compact())
    }
}
