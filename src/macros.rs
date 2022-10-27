/// Coverts an io::Result<T> into a PyResult<T>
macro_rules! io_to_py_result {
    ($res:expr) => {
        $res.map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))
    };
}

/// Coverts a byte array to a py string
macro_rules! bytes_to_string {
    ($bytes:expr) => {
        String::from_utf8($bytes)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
    };
}

/// Acquires the lock on a Mutex and returns an io Error if it fails
macro_rules! acquire_lock {
    ($v:expr) => {
        $v.lock()
            .map_err(|e| pyo3::exceptions::PyBaseException::new_err(e.to_string()))
    };
}

/// Generates a Python None value
macro_rules! py_none {
    () => {
        Python::with_gil(|py| py.None())
    };
}

pub(crate) use acquire_lock;
pub(crate) use bytes_to_string;
pub(crate) use io_to_py_result;
pub(crate) use py_none;
