import time


def array_search(array, key):
    """Linear search through a one-dimensional list; return the Medicine or None."""
    for item in array:
        if item.product_id == key:
            return item
    return None


def compare_search(table, array, key):
    """Search the same key in the hash table and the array, timing each once.
       Return (record or None, hash table seconds, array seconds)."""
    start = time.perf_counter()
    result = table.search(key)
    hash_time = time.perf_counter() - start

    start = time.perf_counter()
    array_search(array, key)
    array_time = time.perf_counter() - start

    return result, hash_time, array_time
