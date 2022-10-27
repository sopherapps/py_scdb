# scdb

![CI](https://github.com/sopherapps/py_scdb/actions/workflows/CI.yml/badge.svg)

A very simple and fast key-value store but persisting data to disk, with a "localStorage-like" API.

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


### TODO:

- [ ] Add sync support.
- [ ] Add async support
- [ ] Add tests
- [ ] Add benchmarks

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

```shell
# asynchronous API
pytest test/test_async_benchmarks.py --benchmark-columns=mean,min,max --benchmark-name=short
```

## Benchmarks

TBD

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
