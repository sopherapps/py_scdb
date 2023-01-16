import pytest
import pytest_asyncio
from pytest_lazyfixture import lazy_fixture

from py_scdb import Store, AsyncStore
from test.utils import store_path, async_store_path

records = [
    ("hey", "English"),
    ("hi", "English"),
    ("salut", "French"),
    ("bonjour", "French"),
    ("hola", "Spanish"),
    ("oi", "Portuguese"),
    ("mulimuta", "Runyoro"),
]
keys = [k for (k, _) in records]
updates = [
    ("hey", "Jane"),
    ("hi", "John"),
    ("hola", "Santos"),
    ("oi", "Ronaldo"),
    ("mulimuta", "Aliguma"),
]
search_records = [
    ("foo", "eng"),
    ("fore", "span"),
    ("food", "lug"),
    ("bar", "port"),
    ("band", "nyoro"),
    ("pig", "dan"),
]

store_fixture = [lazy_fixture("sync_store")]
searchable_store_fixture = [lazy_fixture("sync_searchable_store")]
records_fixture = [(lazy_fixture("sync_store"), k, v) for (k, v) in records[:2]]
searchable_records_fixture = [
    (lazy_fixture("sync_searchable_store"), k, v) for (k, v) in records[:2]
]
keys_fixture = [(lazy_fixture("sync_store"), k) for k in keys[:2]]
searchable_keys_fixture = [(lazy_fixture("sync_searchable_store"), k) for k in keys[:2]]
search_terms_fixture = [
    (lazy_fixture("sync_searchable_store"), term)
    for term in [
        "f",
        "fo",
        "foo",
        "for",
        "b",
        "ba",
        "bar",
        "ban",
        "pigg",
        "p",
        "pi",
        "pig",
    ]
]

async_store_fixture = [lazy_fixture("async_store")]
async_searchable_store_fixture = [lazy_fixture("async_searchable_store")]


@pytest.fixture()
def sync_store():
    """The key-value store"""
    _store = Store(store_path=store_path)
    yield _store
    _store.clear()


@pytest.fixture()
def sync_searchable_store():
    """The key-value store"""
    _store = Store(store_path=store_path, is_search_enabled=True)
    yield _store
    _store.clear()


@pytest_asyncio.fixture
async def async_store():
    """The asynchronous key-value store"""
    _store = AsyncStore(store_path=async_store_path)
    yield _store
    await _store.clear()


@pytest_asyncio.fixture
async def async_searchable_store():
    """The asynchronous key-value store"""
    _store = AsyncStore(store_path=async_store_path, is_search_enabled=True)
    yield _store
    await _store.clear()
