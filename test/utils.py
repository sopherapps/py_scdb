import os
from os import path
from typing import List, Tuple, Optional

from py_scdb import AsyncStore, Store

_root_directory = path.dirname(path.dirname(__file__))
_store_path = path.join(_root_directory, "testdb")
_async_store_path = path.join(_root_directory, "async_testdb")


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
    db_file_path = os.path.join(_store_path, "dump.scdb")
    return os.stat(db_file_path).st_size


def get_async_db_file_size() -> int:
    """Returns the size of the database file"""
    db_file_path = os.path.join(_async_store_path, "dump.scdb")
    return os.stat(db_file_path).st_size
