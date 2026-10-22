import time
from medicine import Medicine
from hash_table import HashTable

NUM_RECORDS = 5000
TABLE_SIZE = 10007        # larger than the record count, keeps probing short
ROUNDS = 5


def build_data():
    """Create the same list of medicines for both structures."""
    return [Medicine(f"MED{i:05d}", f"Medicine {i}", "General", 10.0, 50, "2028-01-01")
            for i in range(NUM_RECORDS)]


def array_search(array, key):
    """Linear search through a one-dimensional list."""
    for item in array:
        if item.product_id == key:
            return item
    return None


def time_it(func, *args):
    """Return how many nanoseconds func(*args) took."""
    start = time.perf_counter_ns()
    func(*args)
    return time.perf_counter_ns() - start


def main():
    data = build_data()
    table = HashTable(TABLE_SIZE)
    for m in data:
        table.insert(m.product_id, m)

    # Keys to search: first, middle, last (array worst case) and one missing
    targets = [data[0].product_id, data[NUM_RECORDS // 2].product_id,
               data[-1].product_id, "MED99999"]

    print(f"Records: {NUM_RECORDS} | Hash table size: {TABLE_SIZE}\n")
    print(f"{'Key':<10} | {'Array (ns)':>12} | {'Hash Table (ns)':>16}")
    print("-" * 45)
    for key in targets:
        # average over several rounds to reduce random timing noise
        arr = sum(time_it(array_search, data, key) for _ in range(ROUNDS)) // ROUNDS
        hsh = sum(time_it(table.search, key) for _ in range(ROUNDS)) // ROUNDS
        print(f"{key:<10} | {arr:>12} | {hsh:>16}")


if __name__ == "__main__":
    main()
