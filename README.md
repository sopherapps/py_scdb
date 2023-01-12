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
        max_index_key_len=3,
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
        max_index_key_len=3,
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
pytest test/test_benchmarks.py --benchmark-columns=mean,min,max --benchmark-name=short 
```

## Benchmarks

On an average PC (17Core, 16 GB RAM)

### Synchronous

```
------------------------------------------------------ benchmark: 47 tests -------------------------------------------------------
Name (time in ns)                                           Mean                         Min                         Max          
----------------------------------------------------------------------------------------------------------------------------------
benchmark_get[sync_store-hey]                           800.4672 (1.03)             698.0000 (1.0)           59,185.0000 (1.48)   
benchmark_get[sync_store-oi]                            776.5698 (1.0)              699.0000 (1.00)          39,861.0000 (1.0)    
benchmark_get[sync_store-salut]                         785.0628 (1.01)             702.0000 (1.01)          49,960.0000 (1.25)   
benchmark_get[sync_store-bonjour]                       780.4937 (1.01)             703.0000 (1.01)          71,929.0000 (1.80)   
benchmark_get[sync_store-mulimuta]                      783.5682 (1.01)             705.0000 (1.01)          50,234.0000 (1.26)   
benchmark_get[sync_store-hi]                            790.7354 (1.02)             709.0000 (1.02)          70,327.0000 (1.76)   
benchmark_get[sync_store-hola]                          802.1952 (1.03)             721.0000 (1.03)          61,532.0000 (1.54)   
benchmark_paginated_search[sync_store-for]            6,962.4849 (8.97)           6,547.0000 (9.38)          56,507.0000 (1.42)   
benchmark_paginated_search[sync_store-pigg]           6,919.7214 (8.91)           6,556.0000 (9.39)         130,593.0000 (3.28)   
benchmark_paginated_search[sync_store-bar]            7,079.0014 (9.12)           6,556.0000 (9.39)          86,028.0000 (2.16)   
benchmark_paginated_search[sync_store-pi]             6,936.8665 (8.93)           6,556.0000 (9.39)         167,335.0000 (4.20)   
benchmark_search[sync_store-pigg]                     6,902.7711 (8.89)           6,613.0000 (9.47)          61,975.0000 (1.55)   
benchmark_paginated_search[sync_store-pig]            7,028.6412 (9.05)           6,643.0000 (9.52)          89,304.0000 (2.24)   
benchmark_paginated_search[sync_store-ban]            7,234.7422 (9.32)           6,653.0000 (9.53)          82,575.0000 (2.07)   
benchmark_paginated_search[sync_store-p]              7,027.5200 (9.05)           6,688.0000 (9.58)          58,940.0000 (1.48)   
benchmark_search[sync_store-for]                     10,294.3237 (13.26)          9,821.0000 (14.07)         71,856.0000 (1.80)   
benchmark_search[sync_store-p]                       10,391.7488 (13.38)          9,822.0000 (14.07)        111,787.0000 (2.80)   
benchmark_search[sync_store-ban]                     10,403.6132 (13.40)          9,831.0000 (14.08)         89,734.0000 (2.25)   
benchmark_search[sync_store-pig]                     10,374.8678 (13.36)          9,841.0000 (14.10)         60,577.0000 (1.52)   
benchmark_search[sync_store-pi]                      10,380.7388 (13.37)          9,941.0000 (14.24)        108,986.0000 (2.73)   
benchmark_search[sync_store-bar]                     10,449.2485 (13.46)          9,983.0000 (14.30)         71,575.0000 (1.80)   
benchmark_paginated_search[sync_store-fo]            12,587.1956 (16.21)         12,075.0000 (17.30)         69,118.0000 (1.73)   
benchmark_paginated_search[sync_store-ba]            13,841.9919 (17.82)         12,089.0000 (17.32)     22,140,639.0000 (555.45) 
benchmark_paginated_search[sync_store-f]             12,743.9164 (16.41)         12,150.0000 (17.41)        167,326.0000 (4.20)   
benchmark_paginated_search[sync_store-b]             12,762.3290 (16.43)         12,185.0000 (17.46)        141,532.0000 (3.55)   
benchmark_paginated_search[sync_store-foo]           12,808.0472 (16.49)         12,268.0000 (17.58)        160,061.0000 (4.02)   
benchmark_delete[sync_store-oi]                      21,704.5624 (27.95)         13,880.0000 (19.89)        112,458.0000 (2.82)   
benchmark_delete[sync_store-hi]                      20,088.1860 (25.87)         14,064.0000 (20.15)         93,398.0000 (2.34)   
benchmark_delete[sync_store-mulimuta]                21,373.7075 (27.52)         14,105.0000 (20.21)         64,670.0000 (1.62)   
benchmark_delete[sync_store-salut]                   21,230.0633 (27.34)         14,236.0000 (20.40)        111,376.0000 (2.79)   
benchmark_delete[sync_store-hey]                     19,834.3945 (25.54)         14,298.0000 (20.48)         81,824.0000 (2.05)   
benchmark_delete[sync_store-hola]                    21,709.5685 (27.96)         14,315.0000 (20.51)      9,488,572.0000 (238.04) 
benchmark_delete[sync_store-bonjour]                 21,215.8223 (27.32)         14,406.0000 (20.64)         76,129.0000 (1.91)   
benchmark_search[sync_store-ba]                      15,359.4292 (19.78)         14,754.0000 (21.14)        127,285.0000 (3.19)   
benchmark_search[sync_store-b]                       15,462.2251 (19.91)         14,840.0000 (21.26)         74,957.0000 (1.88)   
benchmark_search[sync_store-foo]                     15,673.4764 (20.18)         14,889.0000 (21.33)         77,673.0000 (1.95)   
benchmark_search[sync_store-f]                       20,645.8552 (26.59)         19,583.0000 (28.06)         83,335.0000 (2.09)   
benchmark_search[sync_store-fo]                      20,593.4482 (26.52)         19,716.0000 (28.25)        114,361.0000 (2.87)   
benchmark_set[sync_store-hi-English]                 26,811.3686 (34.53)         24,591.0000 (35.23)        102,322.0000 (2.57)   
benchmark_set[sync_store-oi-Portuguese]              26,792.9735 (34.50)         24,691.0000 (35.37)        105,970.0000 (2.66)   
benchmark_set[sync_store-salut-French]               34,000.6656 (43.78)         31,847.0000 (45.63)        114,291.0000 (2.87)   
benchmark_set[sync_store-hola-Spanish]               34,219.5426 (44.06)         31,857.0000 (45.64)        103,374.0000 (2.59)   
benchmark_set[sync_store-bonjour-French]             34,491.8102 (44.42)         32,046.0000 (45.91)        123,111.0000 (3.09)   
benchmark_set[sync_store-mulimuta-Runyoro]           33,995.6793 (43.78)         32,332.0000 (46.32)        117,633.0000 (2.95)   
benchmark_set[sync_store-hey-English]                34,103.0846 (43.92)         32,513.0000 (46.58)        107,059.0000 (2.69)   
benchmark_clear[sync_store]                         168,770.7111 (217.33)       128,008.0000 (183.39)       471,408.0000 (11.83)  
benchmark_compact[sync_store]                   106,328,709.5000 (>1000.0)  103,646,207.0000 (>1000.0)  108,741,183.0000 (>1000.0)
----------------------------------------------------------------------------------------------------------------------------------
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