from os import path

import pytest
import pytest_asyncio
from pytest_lazyfixture import lazy_fixture

from py_scdb import Store, AsyncStore

_root_directory = path.dirname(path.dirname(__file__))

_store_path = path.join(_root_directory, "testdb")
_async_store_path = path.join(_root_directory, "async_testdb")

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

store_fixture = [lazy_fixture("store")]
records_fixture = [lazy_fixture(("store", k, v)) for (k, v) in records]
updates_fixture = [lazy_fixture(("store", k, v)) for (k, v) in updates]
keys_fixture = [lazy_fixture(("store", k)) for k in keys]

async_store_fixture = [lazy_fixture("async_store")]
async_records_fixture = [lazy_fixture(("async_store", k, v)) for (k, v) in records]
async_updates_fixture = [lazy_fixture(("async_store", k, v)) for (k, v) in updates]
async_keys_fixture = [lazy_fixture(("async_store", k)) for k in keys]


@pytest.fixture()
def store():
    """The key-value store"""
    _store = Store(store_path=_store_path)
    yield _store
    _store.clear()


@pytest_asyncio.fixture
async def async_store():
    """The asynchronous key-value store"""
    _store = AsyncStore(store_path=_async_store_path)
    yield _store
    await _store.clear()


@pytest.fixture()
def aio_benchmark(benchmark):
    """
    A fixture for benchmarking coroutines courtesy of [Marcello Bello](https://github.com/mbello)
    as shared in this issue:
    https://github.com/ionelmc/pytest-benchmark/issues/66#issuecomment-575853801
    """
    import asyncio
    import threading

    class Sync2Async:
        def __init__(self, coro, *args, **kwargs):
            self.coro = coro
            self.args = args
            self.kwargs = kwargs
            self.custom_loop = None
            self.thread = None

        def start_background_loop(self) -> None:
            asyncio.set_event_loop(self.custom_loop)
            self.custom_loop.run_forever()

        def __call__(self):
            evloop = None
            awaitable = self.coro(*self.args, **self.kwargs)
            try:
                evloop = asyncio.get_running_loop()
            except:
                pass
            if evloop is None:
                return asyncio.run(awaitable)
            else:
                if not self.custom_loop or not self.thread or not self.thread.is_alive():
                    self.custom_loop = asyncio.new_event_loop()
                    self.thread = threading.Thread(target=self.start_background_loop, daemon=True)
                    self.thread.start()

                return asyncio.run_coroutine_threadsafe(awaitable, self.custom_loop).result()

    def _wrapper(func, *args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            benchmark(Sync2Async(func, *args, **kwargs))
        else:
            benchmark(func, *args, **kwargs)

    return _wrapper
