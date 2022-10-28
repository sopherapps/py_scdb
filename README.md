# py_scdb

[![PyPI version](https://badge.fury.io/py/py_scdb.svg)](https://badge.fury.io/py/py_scdb) ![CI](https://github.com/sopherapps/py_scdb/actions/workflows/CI.yml/badge.svg)

A very simple and fast key-value *(as UTF-8 strings)* store but persisting data to disk, with a "localStorage-like" API.

This is the python version of the original [scdb](https://github.com/sopherapps/scdb)

**scdb may not be production-ready yet. It works, quite well but it requires more vigorous testing.**

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
        compaction_interval=1800)
    
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
        compaction_interval=1800)
    
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
pytest test/test_benchmarks.py --benchmark-columns=mean,min,max --benchmark-name=short 
```

## Benchmarks

On an average PC.

### Synchronous

```
---------------------------------------------------- benchmark: 23 tests -----------------------------------------------------
Name (time in ns)                                         Mean                        Min                        Max          
------------------------------------------------------------------------------------------------------------------------------
benchmark_get[sync_store-oi]                          791.6189 (1.02)            696.0000 (1.0)          82,662.0000 (3.66)   
benchmark_get[sync_store-salut]                       785.4837 (1.01)            705.0000 (1.01)         26,959.0000 (1.19)   
benchmark_get[sync_store-hey]                         784.9184 (1.01)            706.0000 (1.01)         49,103.0000 (2.17)   
benchmark_get[sync_store-bonjour]                     788.7490 (1.01)            707.0000 (1.02)         38,032.0000 (1.68)   
benchmark_get[sync_store-mulimuta]                    813.3644 (1.04)            710.0000 (1.02)         43,976.0000 (1.95)   
benchmark_get[sync_store-hola]                        778.5139 (1.0)             717.0000 (1.03)         22,595.0000 (1.0)    
benchmark_get[sync_store-hi]                          799.0443 (1.03)            720.0000 (1.03)         41,808.0000 (1.85)   
benchmark_delete[sync_store-oi]                     3,621.6866 (4.65)          3,411.0000 (4.90)         79,191.0000 (3.50)   
benchmark_delete[sync_store-mulimuta]               3,692.2154 (4.74)          3,452.0000 (4.96)         65,033.0000 (2.88)   
benchmark_delete[sync_store-hi]                     3,672.9944 (4.72)          3,464.0000 (4.98)         53,222.0000 (2.36)   
benchmark_delete[sync_store-hola]                   3,662.2025 (4.70)          3,484.0000 (5.01)         53,862.0000 (2.38)   
benchmark_delete[sync_store-hey]                    3,692.2129 (4.74)          3,486.0000 (5.01)         59,462.0000 (2.63)   
benchmark_delete[sync_store-bonjour]                3,733.3740 (4.80)          3,489.0000 (5.01)         56,492.0000 (2.50)   
benchmark_delete[sync_store-salut]                  3,703.2190 (4.76)          3,496.0000 (5.02)         67,755.0000 (3.00)   
benchmark_set[sync_store-salut-French]             10,501.6776 (13.49)         8,502.0000 (12.22)     3,728,135.0000 (165.00) 
benchmark_set[sync_store-hola-Spanish]             10,070.0885 (12.94)         8,619.0000 (12.38)       103,351.0000 (4.57)   
benchmark_set[sync_store-bonjour-French]           11,022.1169 (14.16)         8,646.0000 (12.42)     8,880,446.0000 (393.03) 
benchmark_set[sync_store-hi-English]               11,689.5849 (15.02)         8,658.0000 (12.44)    21,890,731.0000 (968.83) 
benchmark_set[sync_store-oi-Portuguese]             9,977.9048 (12.82)         8,733.0000 (12.55)        71,176.0000 (3.15)   
benchmark_set[sync_store-hey-English]              10,487.5903 (13.47)         8,831.0000 (12.69)     2,436,681.0000 (107.84) 
benchmark_set[sync_store-mulimuta-Runyoro]          9,909.8211 (12.73)         9,273.0000 (13.32)       101,878.0000 (4.51)   
benchmark_clear[sync_store]                        99,848.0430 (128.25)       81,451.0000 (117.03)      320,574.0000 (14.19)  
benchmark_compact[sync_store]                  27,771,153.0357 (>1000.0)  22,487,888.0000 (>1000.0)  36,291,919.0000 (>1000.0)
------------------------------------------------------------------------------------------------------------------------------
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