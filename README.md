# py_scdb

[![PyPI version](https://badge.fury.io/py/py_scdb.svg)](https://badge.fury.io/py/py_scdb) ![CI](https://github.com/sopherapps/py_scdb/actions/workflows/CI.yml/badge.svg)

A very simple and fast key-value *(as UTF-8 strings)* store but persisting data to disk, with a "localStorage-like" API.

This is the python version of the original [scdb](https://github.com/sopherapps/scdb)

**scdb may not be production-ready yet. It works, quite well but it requires more rigorous testing.**

## Purpose

Coming from front-end web
development, [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) was always
a convenient way of quickly persisting data to be used later by a given application even after a restart.
Its API was extremely simple i.e. `localStorage.getItem()`, `localStorage.setItem()`, `localStorage.removeItem()`
, `localStorage.clear()`.

Coming to the backend (or even desktop) development, such an embedded persistent data store with a simple API
was hard to come by.

scdb is meant to be like the 'localStorage' of backend and desktop (and possibly mobile) systems.
Of course to make it a little more appealing, it has some extra features like:

- Time-to-live (TTL) where a key-value pair expires after a given time
- Non-blocking reads from separate processes, and threads.
- Fast Sequential writes to the store, queueing any writes from multiple processes and threads.
- Optional searching of keys that begin with a given subsequence. This option is turned on when `scdb::new()` is called.
  Note: **When searching is enabled, `delete`, `get`, `compact`, `clear` become considerably slower.**

## Dependencies

- python +v3.7

## Quick Start (Synchronous)

- Install the package

```shell
pip install py_scdb
```

- Import the `Store` and use accordingly

```python
if __name__ == "__main__":
    from py_scdb import Store

    # These need to be UTF-8 strings
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
    
    store = Store(
        store_path="db", 
        max_keys=1000000, 
        redundant_blocks=1, 
        pool_capacity=10, 
        compaction_interval=1800,
        is_search_enabled=True,
    )
    
    # inserting without ttl
    for (k, v) in records[:3]:
        store.set(k=k, v=v)
    
    # inserting with ttl of 5 seconds
    for (k, v) in records[3:]:
        store.set(k=k, v=v, ttl=5)
            
    # updating - just set them again
    updates = [
          ("hey", "Jane"),
          ("hi", "John"),
          ("hola", "Santos"),
          ("oi", "Ronaldo"),
          ("mulimuta", "Aliguma"),
    ]
    for (k, v) in updates:
        store.set(k=k, v=v)
    
    # getting
    for k in keys:
        v = store.get(k=k)
        print(f"Key: {k}, Value: {v}")

    # searching without pagination
    results = store.search(term="h")
    print(f"Search 'h' (no pagination):\n{results}\n")

    # searching with pagination
    results = store.search(term="h", skip=1, limit=2)
    print(f"Search 'h' (skip=1, limit=2):\n{results}\n")
    
    # deleting
    for k in keys[:3]:
        store.delete(k=k)
      
    # clearing
    store.clear()
      
    # compacting (Use sparingly, say if database file is too big)
    store.compact()
```

- Run the module

```shell
python <module_name>.py 
# e.g. python main.py
```

## Quick Start (Asynchronous)

- Install the package

```shell
pip install py_scdb
```

- Import the `AsyncStore` and use accordingly

```python
import asyncio
from py_scdb import AsyncStore

# These need to be UTF-8 strings
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

async def run_async_example():
    store = AsyncStore(
        store_path="db", 
        max_keys=1000000, 
        redundant_blocks=1, 
        pool_capacity=10, 
        compaction_interval=1800,
        is_search_enabled=True,
    )
    
    # inserting without ttl
    for (k, v) in records[:3]:
        await store.set(k=k, v=v)
    
    # inserting with ttl of 5 seconds
    for (k, v) in records[3:]:
        await store.set(k=k, v=v, ttl=5)
            
    # updating - just set them again
    updates = [
        ("hey", "Jane"),
        ("hi", "John"),
        ("hola", "Santos"),
        ("oi", "Ronaldo"),
        ("mulimuta", "Aliguma"),
    ]
    for (k, v) in updates:
        await store.set(k=k, v=v)
    
    # getting
    for k in keys:
        v = await store.get(k=k)
        print(f"Key: {k}, Value: {v}")

    # searching without pagination
    results = await store.search(term="h")
    print(f"Search 'h' (no pagination):\n{results}\n")

    # searching with pagination
    results = await store.search(term="h", skip=1, limit=2)
    print(f"Search 'h' (skip=1, limit=2):\n{results}\n")
    
    # deleting
    for k in keys[:3]:
        await store.delete(k=k)
      
    # clearing
    await store.clear()
      
    # compacting (Use sparingly, say if database file is too big)
    await store.compact()


asyncio.run(run_async_example())
```

- Run the module

```shell
python <module_name>.py 
# e.g. python main.py
```

## Contributing

Contributions are welcome. The docs have to maintained, the code has to be made cleaner, more idiomatic and faster,
and there might be need for someone else to take over this repo in case I move on to other things. It happens!

Please look at the [CONTRIBUTIONS GUIDELINES](./docs/CONTRIBUTING.md)

You can also look in the [./docs](https://github.com/sopherapps/scdb/tree/master/docs) 
folder of the [rust scdb](https://github.com/sopherapps/scdb) to get up to speed with the internals of scdb e.g.

- [database file format](https://github.com/sopherapps/scdb/tree/master/docs/DB_FILE_FORMAT.md)
- [how it works](https://github.com/sopherapps/scdb/tree/master/docs/HOW_IT_WORKS.md)
- [inverted index file format](https://github.com/sopherapps/scdb/tree/master/docs/INVERTED_INDEX_FILE_FORMAT.md)
- [how the search works](https://github.com/sopherapps/scdb/tree/master/docs/HOW_INVERTED_INDEX_WORKS.md)

## Bindings

scdb is meant to be used in multiple languages of choice. However, the bindings for most of them are yet to be
developed.

For other programming languages, see the main [README](https://github.com/sopherapps/scdb/tree/master/README.md#bindings)

### How to Test
- Clone the repo and enter its root folder

```shell
git clone https://github.com/sopherapps/py_scdb.git && cd py_scdb
```

- Create a virtual environment and activate it

```shell
virtualenv -p /usr/bin/python3.7 env && source env/bin/activate
```

- Install the dependencies

```shell
pip install -r requirements.txt
```

- Install scdb package in the virtual environment

```shell
maturin develop
```

For optimized build use:

```shell
maturin develop -r
```

- Run the tests command

```shell
pytest --benchmark-disable
```

- Run benchmarks

```shell
pytest --benchmark-compare --benchmark-autosave
```

OR the summary

```shell
# synchronous API
pytest test/test_benchmarks.py --benchmark-columns=mean,min,max --benchmark-name=short --benchmark-sort=NAME
```

## Benchmarks

On an average PC (17Core, 16 GB RAM)

### Synchronous

```

--------------------------------------------------------- benchmark: 40 tests ---------------------------------------------------------
Name (time in us)                                                        Mean                     Min                     Max          
---------------------------------------------------------------------------------------------------------------------------------------
benchmark_clear[sync_store]                                          100.3807 (127.70)        83.0300 (116.78)       311.0190 (6.71)   
benchmark_clear_with_search[sync_searchable_store]                   171.0275 (217.57)       133.6630 (187.99)       433.9330 (9.36)   
benchmark_compact[sync_store]                                    110,236.5678 (>1000.0)  106,076.8240 (>1000.0)  117,694.6450 (>1000.0)
benchmark_compact_with_search[sync_searchable_store]             111,180.5895 (>1000.0)  102,213.0760 (>1000.0)  127,501.7640 (>1000.0)
benchmark_delete[sync_store-hey]                                       3.7683 (4.79)           3.4310 (4.83)          82.3730 (1.78)   
benchmark_delete[sync_store-hi]                                        3.7664 (4.79)           3.4440 (4.84)          54.3430 (1.17)   
benchmark_delete_with_search[sync_searchable_store-hey]               20.7839 (26.44)         15.0590 (21.18)        122.8020 (2.65)   
benchmark_delete_with_search[sync_searchable_store-hi]                20.7891 (26.45)         14.7560 (20.75)        123.6690 (2.67)   
benchmark_get[sync_store-hey]                                          0.7861 (1.0)            0.7110 (1.0)           64.0260 (1.38)   
benchmark_get[sync_store-hi]                                           0.7877 (1.00)           0.7190 (1.01)          55.0760 (1.19)   
benchmark_get_with_search[sync_searchable_store-hey]                   0.7991 (1.02)           0.7220 (1.02)          49.2670 (1.06)   
benchmark_get_with_search[sync_searchable_store-hi]                    0.7899 (1.00)           0.7230 (1.02)          46.3370 (1.0)    
benchmark_paginated_search[sync_searchable_store-b]                   12.9258 (16.44)         12.1430 (17.08)        156.1050 (3.37)   
benchmark_paginated_search[sync_searchable_store-ba]                  12.9307 (16.45)         12.1640 (17.11)        115.5400 (2.49)   
benchmark_paginated_search[sync_searchable_store-ban]                  7.0885 (9.02)           6.6530 (9.36)          71.0410 (1.53)   
benchmark_paginated_search[sync_searchable_store-bar]                  6.9927 (8.90)           6.6160 (9.31)          82.8730 (1.79)   
benchmark_paginated_search[sync_searchable_store-f]                   13.2767 (16.89)         12.0420 (16.94)     21,129.0600 (455.99) 
benchmark_paginated_search[sync_searchable_store-fo]                  12.9289 (16.45)         12.1860 (17.14)        439.6100 (9.49)   
benchmark_paginated_search[sync_searchable_store-foo]                 12.9970 (16.53)         12.3170 (17.32)        102.5070 (2.21)   
benchmark_paginated_search[sync_searchable_store-for]                  6.9771 (8.88)           6.6010 (9.28)          94.3090 (2.04)   
benchmark_paginated_search[sync_searchable_store-p]                    6.9895 (8.89)           6.5870 (9.26)         149.4620 (3.23)   
benchmark_paginated_search[sync_searchable_store-pi]                   6.9171 (8.80)           6.6080 (9.29)          69.2660 (1.49)   
benchmark_paginated_search[sync_searchable_store-pig]                  6.9475 (8.84)           6.5980 (9.28)          67.4790 (1.46)   
benchmark_paginated_search[sync_searchable_store-pigg]                 6.9717 (8.87)           6.6070 (9.29)         111.5230 (2.41)   
benchmark_search[sync_searchable_store-b]                             15.5810 (19.82)         14.6940 (20.67)        105.9520 (2.29)   
benchmark_search[sync_searchable_store-ba]                            15.6253 (19.88)         14.7780 (20.78)        107.5030 (2.32)   
benchmark_search[sync_searchable_store-ban]                           10.5073 (13.37)          9.9340 (13.97)        118.7900 (2.56)   
benchmark_search[sync_searchable_store-bar]                           10.8698 (13.83)          9.8550 (13.86)         97.3030 (2.10)   
benchmark_search[sync_searchable_store-f]                             20.7594 (26.41)         19.5820 (27.54)        116.9510 (2.52)   
benchmark_search[sync_searchable_store-fo]                            20.8279 (26.50)         19.6790 (27.68)        196.4210 (4.24)   
benchmark_search[sync_searchable_store-foo]                           15.7794 (20.07)         14.8380 (20.87)         94.2340 (2.03)   
benchmark_search[sync_searchable_store-for]                           10.4470 (13.29)          9.8640 (13.87)        128.4710 (2.77)   
benchmark_search[sync_searchable_store-p]                             10.3812 (13.21)          9.7870 (13.77)        102.3630 (2.21)   
benchmark_search[sync_searchable_store-pi]                            10.3460 (13.16)          9.8380 (13.84)         84.1260 (1.82)   
benchmark_search[sync_searchable_store-pig]                           10.4069 (13.24)          9.8400 (13.84)         78.9080 (1.70)   
benchmark_search[sync_searchable_store-pigg]                           6.9492 (8.84)           6.6000 (9.28)          86.0650 (1.86)   
benchmark_set[sync_store-hey-English]                                 10.6412 (13.54)          9.2990 (13.08)        110.4370 (2.38)   
benchmark_set[sync_store-hi-English]                                  10.7570 (13.68)          9.1760 (12.91)        100.9780 (2.18)   
benchmark_set_with_search[sync_searchable_store-hey-English]          37.2746 (47.42)         32.7920 (46.12)      8,647.2350 (186.62) 
benchmark_set_with_search[sync_searchable_store-hi-English]           28.0105 (35.63)         25.5050 (35.87)        105.3320 (2.27)   
---------------------------------------------------------------------------------------------------------------------------------------
```

## Acknowledgement

- The asyncio was got using [pyo3-asyncio](https://github.com/awestlake87/pyo3-asyncio)
- The python-rust bindings were got from [the pyo3 project](https://github.com/PyO3)

## License

Licensed under both the [MIT License](./LICENSE-MIT) and the [APACHE (2.0) License](./LICENSE-APACHE)

Copyright (c) 2022 [Martin Ahindura](https://github.com/tinitto)

Copyright (c) 2017-present PyO3 Project and Contributors

## Gratitude

> "Come to Me (Christ Jesus), all you who labor and are heavy laden, and I will give you rest. 
> Take My yoke upon you and learn from Me, for I am gentle and lowly in heart, 
> and you will find rest for your souls. For My yoke is easy and My burden is light."
>
> -- Matthew 11: 28-30

All glory be to God.

<a href="https://www.buymeacoffee.com/martinahinJ" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>