"""Tests for AsyncStore"""
import time

import pytest

from py_scdb import AsyncStore
from test.conftest import async_store_fixture, records
from test.utils import fill_async_store, get_async_db_file_size


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_set_without_ttl(store: AsyncStore):
    """saves the key-value pairs indefinitely"""
    for (k, v) in records:
        await store.set(k=k, v=v)
        assert (await store.get(k=k)) == v


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_set_with_ttl(store: AsyncStore):
    """Saves the key-value pairs for upto ttl seconds"""
    ttl = 2

    # set first 3 without ttl
    for (k, v) in records[:3]:
        await store.set(k=k, v=v)

    # set first 3 with ttl=2
    for (k, v) in records[3:]:
        await store.set(k=k, v=v, ttl=ttl)

    time.sleep(ttl)

    # check the first 3 that had no ttl
    for (k, v) in records[:3]:
        assert (await store.get(k=k)) == v

    # check the last 3 that had ttl
    for (k, v) in records[3:]:
        assert (await store.get(k=k)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_set_existing_key(store: AsyncStore):
    """get updates a given value for the given key if key already exists"""
    key = "foo"
    first_value = "bar"
    new_value = "booo"

    await store.set(k=key, v=first_value)
    await store.set(k=key, v=new_value)

    assert (await store.get(k=key)) == new_value


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_get_existing_key(store: AsyncStore):
    """Returns the value for the given key"""
    await fill_async_store(store=store, data=records)
    for (k, v) in records:
        assert (await store.get(k=k)) == v


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_get_non_existing_key(store: AsyncStore):
    """Returns the None for a key that does not exist"""
    assert (await store.get(k="some-random-value")) is None


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_delete_existing_key(store: AsyncStore):
    """delete removes the key-value associated with that key"""
    await fill_async_store(store=store, data=records)

    for (k, _) in records:
        await store.delete(k=k)
        assert (await store.get(k=k)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_delete_non_existing_key(store: AsyncStore):
    """delete does nothing for non-existing keys"""
    assert (await store.delete(k="some-rando-key")) is None


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_clear(store: AsyncStore):
    """Removes all key-value pairs from store"""
    await fill_async_store(store=store, data=records)
    await store.clear()

    for (k, _) in records:
        assert (await store.get(k=k)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_compact(store: AsyncStore):
    """Reduces the size of the database file if some keys have expired or were deleted"""
    ttl = 1
    initial_file_size = get_async_db_file_size()
    # add those that will expire after one second
    await fill_async_store(store=store, data=records[:3], ttl=ttl)
    await fill_async_store(store=store, data=records[3:])
    # delete the fourth
    await store.delete(k=records[3][0])
    intermediate_file_size = get_async_db_file_size()

    time.sleep(ttl)

    await store.compact()
    final_file_size = get_async_db_file_size()

    assert final_file_size < intermediate_file_size
    assert initial_file_size == final_file_size

    #  the store is still working as expected
    # the expired are not available
    for (k, _) in records[:3]:
        assert (await store.get(k=k)) is None

    # the deleted are not available
    assert (await store.get(k=records[3][0])) is None

    # the rest are available
    for (k, v) in records[4:]:
        assert (await store.get(k=k)) is None
