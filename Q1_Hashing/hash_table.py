class Slot:
    """One slot in the hash table: holds a key and its associated value."""

    def __init__(self, key, value):
        self.key = key      # used to find the item (e.g. product ID)
        self.value = value  # the stored object (e.g. a Medicine)


class HashTable:
    """Generic hash table using open addressing with linear probing."""

    def __init__(self, size=11):
        self.size = size                # total number of slots
        self.table = [None] * size      # None means the slot is empty
        self.count = 0                  # how many items are stored

    def _hash(self, key):
        """Convert a key into its home slot index (0 to size-1)."""
        hash_value = 0
        for char in str(key):
            hash_value = hash_value * 31 + ord(char)   # combine characters
        return hash_value % self.size                  # squeeze into table range

    def insert(self, key, value):
        """Insert a key-value pair using linear probing.

        Returns the slot index where it was stored,
        or -1 if the table is full or the key already exists.
        """
        if self.count == self.size:
            return -1                                  # table is full

        home = self._hash(key)
        for step in range(self.size):
            index = (home + step) % self.size          # next slot, wraps around
            slot = self.table[index]

            if slot is None:                           # empty slot found
                self.table[index] = Slot(key, value)
                self.count += 1
                return index

            if slot.key == key:                        # duplicate key
                return -1

        return -1

    def search(self, key):
        """Return the value stored under key, or None if not found.
        Follows the same probe path as insert."""
        home = self._hash(key)
        for step in range(self.size):
            index = (home + step) % self.size
            slot = self.table[index]
            if slot is None:  # empty slot: key was never inserted
                return None
            if slot.key == key:
                return slot.value
        return None  # checked every slot, not found

    def display(self):
        """Print every slot, for checking and for report screenshots."""
        for i, slot in enumerate(self.table):
            if slot is None:
                print(f"Slot {i:>2}: empty")
            else:
                print(f"Slot {i:>2}: {slot.key}")


# Quick self-test (runs only when this file is run directly)
if __name__ == "__main__":
    t = HashTable(5)
    for k in ["MED001", "MED002", "MED003", "MED004"]:
        print(k, "home:", t._hash(k), "stored at:", t.insert(k, "x"))
    print("Search MED003:", t.search("MED003"))
    print("Search MED999:", t.search("MED999"))
    t.display()
