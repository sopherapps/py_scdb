from typing import List, Tuple, Optional

from py_scdb import AsyncStore, Store
from test.conftest import _store_path, _async_store_path


async def fill_async_store(store: AsyncStore, data: List[Tuple[str, str]], ttl: Optional[int] = None):
    """Fills the async store with records"""
    for (key, value) in data:
        await store.set(k=key, v=value, ttl=ttl)


def fill_store(store: Store, data: List[Tuple[str, str]], ttl: Optional[int] = None):
    """Fills the store with records"""
    for (key, value) in data:
        store.set(k=key, v=value, ttl=ttl)


def get_db_file_size() -> int:
    """Returns the size of the database file"""
    return os.stat(_store_path).st_size


def get_async_db_file_size() -> int:
    """Returns the size of the database file"""
    return os.stat(_async_store_path).st_size
