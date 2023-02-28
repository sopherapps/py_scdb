from typing import Optional, List, Tuple

class Store:
    """
    The key-value store that saves key-value pairs on disk

    Store behaves like a HashMap that saves keys and value as strings
    on disk. It allows for specifying how long each key-value pair should be
    kept for i.e. the time-to-live in seconds. If None is provided, they last indefinitely.

    :param store_path: The path to a directory where scdb should store its data
    :param max_keys: The maximum number of key-value pairs to store in store; default: 1 million
    :param redundant_blocks: The store has an index to hold all the keys. This index is split
                            into a fixed number of blocks basing on the virtual memory page size
                            and the total number of keys to be held i.e. `max_keys`.
                            Sometimes, there may be hash collision errors as the store's
                            current stored keys approach `max_keys`. The closer it gets, the
                            more it becomes likely see those errors. Adding redundant blocks
                            helps mitigate this. Just be careful to not add too many (i.e. more than 2)
                            since the higher the number of these blocks, the slower the store becomes.
                            Default: 1
    :param pool_capacity: The number of buffers to hold in memory as cache's for the store. Each buffer
                        has the size equal to the virtual memory's page size, usually 4096 bytes.
                        Increasing this number will speed this store up but of course, the machine
                        has a limited RAM. When this number increases to a value that clogs the RAM, performance
                        suddenly degrades, and keeps getting worse from there on.
                        Default: 5
    :param compaction_interval: The interval at which the store is compacted to remove dangling
                                keys. Dangling keys result from either getting expired or being deleted.
                                When a `delete` operation is done, the actual key-value pair
                                is just marked as `deleted` but is not removed.
                                Something similar happens when a key-value is updated.
                                A new key-value pair is created and the old one is left unindexed.
                                Compaction is important because it reclaims this space and reduces the size
                                of the database file.
                                Default: 3600s (1 hour)
    :param is_search_enabled: Whether the search capability of the store is enabled.
                              Note that when search is enabled, `set`, `delete`, `clear`, `compact`
                              operations become slower.
                              Default: False
    """

    def __init__(
        self,
        store_path: str,
        max_keys: Optional[int] = None,
        redundant_blocks: Optional[int] = None,
        pool_capacity: Optional[int] = None,
        compaction_interval: Optional[int] = None,
        is_search_enabled: bool = False,
    ) -> None: ...
    def set(self, k: str, v: str, ttl: Optional[int] = None) -> None:
        """
        Inserts or updates the key-value pair

        :param k: the key as a UTF-8 string
        :param v: the value as a UTF-8 string
        :param ttl: the number of seconds the key-value pair should be persisted for
        """
    def get(self, k: str) -> Optional[str]:
        """
        Gets the value associated with the given key

        :param k: the key as a UTF-8 string
        :return: the value if it exists or None if it doesn't
        """
    def search(self, term: str, skip: int = 0, limit: int = 0) -> List[Tuple[str, str]]:
        """
        Finds all key-values whose keys start with the substring `term`.

        It skips the first `skip` (default: 0) number of results and returns not more than
        `limit` (default: 0) number of items. This is to avoid using up more memory than can be handled by the
        host machine.
        If `limit` is 0, all items are returned since it would make no sense for someone to search
        for zero items.

        :param term: the starting substring to check all keys against
        :param skip: the number of the first matched key-value pairs to skip
        :param limit: the maximum number of records to return at any one given time
        :return: the list of key-value pairs whose key starts with the `term`
        """
    def delete(self, k: str) -> None:
        """
        Removes the key-value for the given key from the store

        :param k: the key as a UTF-8 string
        """
    def clear(self) -> None:
        """
        Removes all data in the store
        """
    def compact(self) -> None:
        """
        Manually removes dangling key-value pairs in the database file.
        This is like vacuuming.

        Dangling keys result from either getting expired or being deleted.
        When a `delete` operation is done, the actual key-value pair
        is just marked as `deleted` but is not removed.

        Something similar happens when a key-value is updated.
        A new key-value pair is created and the old one is left un-indexed.
        Compaction is important because it reclaims this space and reduces the size
        of the database file.

        This is done automatically for you at the set `compaction_interval` but you
        may wish to do it manually for some reason.

        This is a very expensive operation so use it sparingly.
        """

class AsyncStore:
    """
    The key-value store that saves key-value pairs (as a UTF-8 string) on disk.
    This handles its operations asynchronously.

    Store behaves like a HashMap that saves keys and value as strings
    on disk. It allows for specifying how long each key-value pair should be
    kept for i.e. the time-to-live in seconds. If None is provided, they last indefinitely.

    :param store_path: The path to a directory where scdb should store its data
    :param max_keys: The maximum number of key-value pairs to store in store; default: 1 million
    :param redundant_blocks: The store has an index to hold all the keys. This index is split
                            into a fixed number of blocks basing on the virtual memory page size
                            and the total number of keys to be held i.e. `max_keys`.
                            Sometimes, there may be hash collision errors as the store's
                            current stored keys approach `max_keys`. The closer it gets, the
                            more it becomes likely see those errors. Adding redundant blocks
                            helps mitigate this. Just be careful to not add too many (i.e. more than 2)
                            since the higher the number of these blocks, the slower the store becomes.
                            Default: 1
    :param pool_capacity: The number of buffers to hold in memory as cache's for the store. Each buffer
                        has the size equal to the virtual memory's page size, usually 4096 bytes.
                        Increasing this number will speed this store up but of course, the machine
                        has a limited RAM. When this number increases to a value that clogs the RAM, performance
                        suddenly degrades, and keeps getting worse from there on.
                        Default: 5
    :param compaction_interval: The interval at which the store is compacted to remove dangling
                                keys. Dangling keys result from either getting expired or being deleted.
                                When a `delete` operation is done, the actual key-value pair
                                is just marked as `deleted` but is not removed.
                                Something similar happens when a key-value is updated.
                                A new key-value pair is created and the old one is left unindexed.
                                Compaction is important because it reclaims this space and reduces the size
                                of the database file.
                                Default: 3600s (1 hour)
    :param is_search_enabled: Whether the search capability of the store is enabled.
                              Note that when search is enabled, `set`, `delete`, `clear`, `compact`
                              operations become slower.
                              Default: False
    """

    def __init__(
        self,
        store_path: str,
        max_keys: Optional[int] = None,
        redundant_blocks: Optional[int] = None,
        pool_capacity: Optional[int] = None,
        compaction_interval: Optional[int] = None,
        is_search_enabled: bool = False,
    ) -> None: ...
    async def set(self, k: str, v: str, ttl: Optional[int] = None) -> None:
        """
        Inserts or updates the key-value pair

        :param k: the key as a UTF-8 string
        :param v: the value as a UTF-8 string
        :param ttl: the number of seconds the key-value pair should be persisted for
        """
    async def get(self, k: str) -> Optional[str]:
        """
        Gets the value associated with the given key

        :param k: the key as a UTF-8 string
        :return: the value if it exists or None if it doesn't
        """
    async def search(
        self, term: str, skip: int = 0, limit: int = 0
    ) -> List[Tuple[str, str]]:
        """
        Finds all key-values whose keys start with the substring `term`.

        It skips the first `skip` (default: 0) number of results and returns not more than
        `limit` (default: 0) number of items. This is to avoid using up more memory than can be handled by the
        host machine.
        If `limit` is 0, all items are returned since it would make no sense for someone to search
        for zero items.

        :param term: the starting substring to check all keys against
        :param skip: the number of the first matched key-value pairs to skip
        :param limit: the maximum number of records to return at any one given time
        :return: the list of key-value pairs whose key starts with the `term`
        """
    async def delete(self, k: str) -> None:
        """
        Removes the key-value for the given key from the store

        :param k: the key as a UTF-8 string
        """
    async def clear(self) -> None:
        """
        Removes all data in the store
        """
    async def compact(self) -> None:
        """
        Manually removes dangling key-value pairs in the database file.
        This is like vacuuming.

        Dangling keys result from either getting expired or being deleted.
        When a `delete` operation is done, the actual key-value pair
        is just marked as `deleted` but is not removed.

        Something similar happens when a key-value is updated.
        A new key-value pair is created and the old one is left un-indexed.
        Compaction is important because it reclaims this space and reduces the size
        of the database file.

        This is done automatically for you at the set `compaction_interval` but you
        may wish to do it manually for some reason.

        This is a very expensive operation so use it sparingly.
        """
