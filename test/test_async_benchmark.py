"""Benchmarks tests for AsyncStore"""

import pytest

from test.conftest import async_store_fixture, records, async_keys_fixture, async_records_fixture
from test.utils import fill_async_store


@pytest.mark.asyncio
@pytest.mark.parametrize("store, k, v", async_records_fixture)
async def test_benchmark_async_set(aio_benchmark, store, k, v):
    """Benchmarks the set operation"""
    aio_benchmark(store.set, k=k, v=v)


@pytest.mark.asyncio
@pytest.mark.parametrize("store, k", async_keys_fixture)
async def test_benchmark_async_get(aio_benchmark, store, k):
    """Benchmarks the get operation"""
    await fill_async_store(store=store, data=records)
    aio_benchmark(store.get, k=k)


@pytest.mark.asyncio
@pytest.mark.parametrize("store, k", async_keys_fixture)
async def test_benchmark_async_delete(aio_benchmark, store, k):
    """Benchmarks the delete operation"""
    await fill_async_store(store=store, data=records)
    aio_benchmark(store.delete, k=k)


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_benchmark_async_clear(aio_benchmark, store):
    """Benchmarks the clear operation"""
    await fill_async_store(store=store, data=records)
    aio_benchmark(store.clear)


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_benchmark_async_compact(aio_benchmark, store):
    """Benchmarks the compact operation"""
    await fill_async_store(store=store, data=records)
    aio_benchmark(store.compact)
