"""Benchmark tests for Store"""

import pytest

from test.conftest import (
    records_fixture,
    keys_fixture,
    records,
    store_fixture,
    search_records,
    search_terms_fixture,
)
from test.utils import fill_store


@pytest.mark.parametrize("store, k, v", records_fixture)
def test_benchmark_set(benchmark, store, k, v):
    """Benchmarks the set operation"""
    benchmark(store.set, k=k, v=v)


@pytest.mark.parametrize("store, k", keys_fixture)
def test_benchmark_get(benchmark, store, k):
    """Benchmarks the get operation"""
    fill_store(store=store, data=records)
    benchmark(store.get, k=k)


@pytest.mark.parametrize("store, term", search_terms_fixture)
def test_benchmark_search(benchmark, store, term):
    """Benchmarks the get operation"""
    fill_store(store=store, data=search_records)
    benchmark(store.search, term=term, skip=0, limit=0)


@pytest.mark.parametrize("store, term", search_terms_fixture)
def test_benchmark_paginated_search(benchmark, store, term):
    """Benchmarks the get operation"""
    fill_store(store=store, data=search_records)
    benchmark(store.search, term=term, skip=1, limit=1)


@pytest.mark.parametrize("store, k", keys_fixture)
def test_benchmark_delete(benchmark, store, k):
    """Benchmarks the delete operation"""
    fill_store(store=store, data=records)
    benchmark(store.delete, k=k)


@pytest.mark.parametrize("store", store_fixture)
def test_benchmark_clear(benchmark, store):
    """Benchmarks the clear operation"""
    fill_store(store=store, data=records)
    benchmark(store.clear)


@pytest.mark.parametrize("store", store_fixture)
def test_benchmark_compact(benchmark, store):
    """Benchmarks the compact operation"""
    fill_store(store=store, data=records)
    benchmark(store.compact)
