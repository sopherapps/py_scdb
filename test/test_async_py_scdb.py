"""Tests for AsyncStore"""
import time

import pytest

from py_scdb import AsyncStore
from test.conftest import async_store_fixture, records, search_records
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
    ttl = 1

    # set first 3 without ttl
    for (k, v) in records[:3]:
        await store.set(k=k, v=v)

    # set first 3 with ttl=2
    for (k, v) in records[3:]:
        await store.set(k=k, v=v, ttl=ttl)

    time.sleep(ttl * 2)

    # check the first 3 that had no ttl
    for (k, v) in records[:3]:
        assert (await store.get(k=k)) == v

    # check the last 3 that had ttl
    for (k, v) in records[3:]:
        assert (await store.get(k=k)) is None


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_updating_ttl(store: AsyncStore):
    """Setting a key-value again updates its ttl also"""
    k1, v1 = "foo", "bar"
    k2, v2 = "foo2", "bar2"
    await store.set(k1, v1)  # no ttl
    await store.set(k2, v2, 1)  # with ttl

    time.sleep(2)
    assert (await store.get(k1)) == v1
    assert (await store.get(k2)) is None

    # update them, but reverse the ttl's
    await store.set(k2, v2)  # no ttl
    await store.set(k1, v1, 1)  # with ttl

    time.sleep(2)
    assert (await store.get(k2)) == v2
    assert (await store.get(k1)) is None


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
async def test_search_without_pagination(store: AsyncStore):
    """Returns the list of key-values whose keys start with given search term"""
    test_data = [
        ("f", [("foo", "eng"), ("fore", "span"), ("food", "lug")]),
        ("fo", [("foo", "eng"), ("fore", "span"), ("food", "lug")]),
        ("foo", [("foo", "eng"), ("food", "lug")]),
        ("food", [("food", "lug")]),
        ("for", [("fore", "span")]),
        ("b", [("bar", "port"), ("band", "nyoro")]),
        ("ba", [("bar", "port"), ("band", "nyoro")]),
        ("bar", [("bar", "port")]),
        ("ban", [("band", "nyoro")]),
        ("band", [("band", "nyoro")]),
        ("p", [("pig", "dan")]),
        ("pi", [("pig", "dan")]),
        ("pig", [("pig", "dan")]),
        ("pigg", []),
        ("bandana", []),
        ("bare", []),
    ]

    await fill_async_store(store=store, data=search_records)
    for (term, expected) in test_data:
        assert (await store.search(term=term, skip=0, limit=0)) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_search_with_pagination(store: AsyncStore):
    """Returns a slice of the list of key-values whose keys start with given search term, basing on skip and limit"""
    test_data = [
        ("fo", 0, 0, [("foo", "eng"), ("fore", "span"), ("food", "lug")]),
        ("fo", 0, 8, [("foo", "eng"), ("fore", "span"), ("food", "lug")]),
        ("fo", 1, 8, [("fore", "span"), ("food", "lug")]),
        ("fo", 1, 0, [("fore", "span"), ("food", "lug")]),
        ("fo", 0, 2, [("foo", "eng"), ("fore", "span")]),
        ("fo", 1, 2, [("fore", "span"), ("food", "lug")]),
        ("fo", 0, 1, [("foo", "eng")]),
        ("fo", 2, 1, [("food", "lug")]),
        ("fo", 1, 1, [("fore", "span")]),
    ]

    await fill_async_store(store=store, data=search_records)
    for (term, skip, limit, expected) in test_data:
        assert (await store.search(term=term, skip=skip, limit=limit)) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_search_after_expiration(store: AsyncStore):
    """Returns only non-expired key-values"""
    records_to_expire = [search_records[0], search_records[2], search_records[3]]
    await fill_async_store(store=store, data=search_records, ttl=None)
    await fill_async_store(store=store, data=records_to_expire, ttl=1)

    test_data = [
        ("f", [("fore", "span")]),
        ("fo", [("fore", "span")]),
        ("foo", []),
        ("for", [("fore", "span")]),
        ("b", [("band", "nyoro")]),
        ("ba", [("band", "nyoro")]),
        ("bar", []),
        ("ban", [("band", "nyoro")]),
        ("band", [("band", "nyoro")]),
        ("p", [("pig", "dan")]),
        ("pi", [("pig", "dan")]),
        ("pig", [("pig", "dan")]),
        ("pigg", []),
        ("food", []),
        ("bandana", []),
        ("bare", []),
    ]

    # wait for some items to expire
    time.sleep(2)

    for (term, expected) in test_data:
        assert (await store.search(term=term, skip=0, limit=0)) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_search_after_delete(store: AsyncStore):
    """Returns only existing key-values"""
    keys_to_delete = ["foo", "food", "bar", "band"]
    await fill_async_store(store=store, data=search_records)
    test_data = [
        ("f", [("fore", "span")]),
        ("fo", [("fore", "span")]),
        ("foo", []),
        ("for", [("fore", "span")]),
        ("b", []),
        ("ba", []),
        ("bar", []),
        ("ban", []),
        ("band", []),
        ("p", [("pig", "dan")]),
        ("pi", [("pig", "dan")]),
        ("pig", [("pig", "dan")]),
        ("pigg", []),
        ("food", []),
        ("bandana", []),
        ("bare", []),
    ]

    for k in keys_to_delete:
        await store.delete(k)

    for (term, expected) in test_data:
        assert (await store.search(term=term, skip=0, limit=0)) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("store", async_store_fixture)
async def test_search_after_clear(store: AsyncStore):
    """Returns an empty list when search is called after clear"""
    terms = [
        "f",
        "fo",
        "foo",
        "for",
        "b",
        "ba",
        "bar",
        "ban",
        "band",
        "p",
        "pi",
        "pig",
        "pigg",
        "food",
        "bandana",
        "bare",
    ]
    await fill_async_store(store=store, data=search_records)
    await store.clear()
    for term in terms:
        assert (await store.search(term=term, skip=0, limit=0)) == []


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
    # add those that will expire after one second
    await fill_async_store(store=store, data=records[:3], ttl=ttl)
    await fill_async_store(store=store, data=records[3:])

    # delete the fourth
    await store.delete(k=records[3][0])
    pre_compaction_file_size = get_async_db_file_size()

    time.sleep(ttl * 2)

    await store.compact()
    post_compaction_file_size = get_async_db_file_size()

    assert post_compaction_file_size < pre_compaction_file_size

    #  the store is still working as expected
    # the expired are not available
    for (k, _) in records[:4]:
        assert (await store.get(k=k)) is None

    # the rest are available
    for (k, v) in records[4:]:
        assert (await store.get(k=k)) == v
