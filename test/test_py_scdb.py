"""Tests for Store"""

import time

import pytest

from py_scdb import Store
from test.conftest import (
    store_fixture,
    records,
    search_records,
    searchable_store_fixture,
)
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
    ttl = 1

    # set first 3 without ttl
    for (k, v) in records[:3]:
        store.set(k=k, v=v)

    # set first 3 with ttl=2
    for (k, v) in records[3:]:
        store.set(k=k, v=v, ttl=ttl)

    time.sleep(ttl * 2)

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
def test_get_value_that_is_empty_string(store: Store):
    """Does not error with out of bounds when the value is an empty string thanks to scdb v0.2.1"""
    key = "foo"
    value = ""

    fill_store(store=store, data=[(key, value)])
    for _ in range(3):
        assert store.get(k=key) == value


@pytest.mark.parametrize("store", store_fixture)
def test_search_disabled(store: Store):
    """Raises exception when a search-disabled store's search method is called"""
    fill_store(store=store, data=search_records)
    with pytest.raises(Exception):
        store.search(term="f", skip=0, limit=0)


@pytest.mark.parametrize("store", searchable_store_fixture)
def test_search_without_pagination(store: Store):
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

    fill_store(store=store, data=search_records)
    for (term, expected) in test_data:
        assert store.search(term=term, skip=0, limit=0) == expected


@pytest.mark.parametrize("store", searchable_store_fixture)
def test_search_with_pagination(store: Store):
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

    fill_store(store=store, data=search_records)
    for (term, skip, limit, expected) in test_data:
        assert store.search(term=term, skip=skip, limit=limit) == expected


@pytest.mark.parametrize("store", searchable_store_fixture)
def test_search_after_expiration(store: Store):
    """Returns only non-expired key-values"""
    records_to_expire = [search_records[0], search_records[2], search_records[3]]
    fill_store(store=store, data=search_records, ttl=None)
    fill_store(store=store, data=records_to_expire, ttl=1)

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
        assert store.search(term=term, skip=0, limit=0) == expected


@pytest.mark.parametrize("store", searchable_store_fixture)
def test_search_after_delete(store: Store):
    """Returns only existing key-values"""
    keys_to_delete = ["foo", "food", "bar", "band"]
    fill_store(store=store, data=search_records)
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
        store.delete(k)

    for (term, expected) in test_data:
        assert store.search(term=term, skip=0, limit=0) == expected


@pytest.mark.parametrize("store", searchable_store_fixture)
def test_search_after_clear(store: Store):
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
    fill_store(store=store, data=search_records)
    store.clear()
    for term in terms:
        assert store.search(term=term, skip=0, limit=0) == []


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

    fill_store(store=store, data=records[3:])
    # add those that will expire after one second
    fill_store(store=store, data=records[:3], ttl=ttl)

    # delete the fourth
    store.delete(k=records[3][0])
    pre_compaction_file_size = get_db_file_size()

    time.sleep(ttl * 2)

    store.compact()

    post_compaction_file_size = get_db_file_size()

    assert post_compaction_file_size < pre_compaction_file_size

    #  the store is still working as expected
    # the expired and the deleted are not available
    for (k, _) in records[:4]:
        assert store.get(k=k) is None

    # the rest are available
    for (k, v) in records[4:]:
        assert store.get(k=k) == v
