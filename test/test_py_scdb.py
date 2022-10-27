"""Tests for Store"""
import time

import pytest

from py_scdb import Store
from test.conftest import store_fixture, records
from test.utils import fill_store, get_db_file_size


@pytest.mark.parametrize("store", store_fixture)
def test_set_without_ttl(store: Store):
    """saves the key-value pairs indefinitely"""
    for (k, v) in records:
        store.set(k=k, v=v)
        assert store.get(k=k) == v


@pytest.mark.parametrize("store", store_fixture)
def test_set_with_ttl(store):
    """Saves the key-value pairs for upto ttl seconds"""
    ttl = 2

    # set first 3 without ttl
    for (k, v) in records[:3]:
        store.set(k=k, v=v)

    # set first 3 with ttl=2
    for (k, v) in records[3:]:
        store.set(k=k, v=v, ttl=ttl)

    time.sleep(ttl)

    # check the first 3 that had no ttl
    for (k, v) in records[:3]:
        assert store.get(k=k) == v

    # check the last 3 that had ttl
    for (k, v) in records[3:]:
        assert store.get(k=k) is None


@pytest.mark.parametrize("store", store_fixture)
def test_set_existing_key(store: Store):
    """get updates a given value for the given key if key already exists"""
    key = "foo"
    first_value = "bar"
    new_value = "booo"

    store.set(k=key, v=first_value)
    store.set(k=key, v=new_value)

    assert store.get(k=key) == new_value


@pytest.mark.parametrize("store", store_fixture)
def test_get_existing_key(store: Store):
    """Returns the value for the given key"""
    fill_store(store=store, data=records)
    for (k, v) in records:
        assert store.get(k=k) == v


@pytest.mark.parametrize("store", store_fixture)
def test_get_non_existing_key(store: Store):
    """Returns the None for a key that does not exist"""
    assert store.get(k="some-random-value") is None


@pytest.mark.parametrize("store", store_fixture)
def test_delete_existing_key(store: Store):
    """delete removes the key-value associated with that key"""
    fill_store(store=store, data=records)

    for (k, _) in records:
        store.delete(k=k)
        assert store.get(k=k) is None


@pytest.mark.parametrize("store", store_fixture)
def test_delete_non_existing_key(store: Store):
    """delete does nothing for non-existing keys"""
    assert store.delete(k="some-rando-key") is None


@pytest.mark.parametrize("store", store_fixture)
def test_clear(store):
    """Removes all key-value pairs from store"""
    fill_store(store=store, data=records)
    store.clear()

    for (k, _) in records:
        assert store.get(k=k) is None


@pytest.mark.parametrize("store", store_fixture)
def test_compact(store: Store):
    """Reduces the size of the database file if some keys have expired or were deleted"""
    ttl = 1

    initial_file_size = get_db_file_size()
    # add those that will expire after one second
    fill_store(store=store, data=records[:3], ttl=ttl)
    fill_store(store=store, data=records[3:])
    # delete the fourth
    store.delete(k=records[3][0])
    intermediate_file_size = get_db_file_size()

    time.sleep(ttl)

    store.compact()
    final_file_size = get_db_file_size()

    assert final_file_size < intermediate_file_size
    assert initial_file_size == final_file_size

    #  the store is still working as expected
    # the expired are not available
    for (k, _) in records[:3]:
        assert store.get(k=k) is None

    # the deleted are not available
    assert store.get(k=records[3][0]) is None

    # the rest are available
    for (k, v) in records[4:]:
        assert store.get(k=k) is None
