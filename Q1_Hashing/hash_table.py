HASH_MULTIPLIER = 31    # small prime; makes the position of each character matter

class Slot:
    """One occupied slot in the hash table: stores a key and its value."""

    def __init__(self, key, value):
        """Store the key used for lookup and the associated value."""
        self.key = key      # used to find the item (e.g. product ID)
        self.value = value  # the stored object (e.g. a Medicine)


class HashTable:
    """Generic hash table using open addressing with linear probing."""

    def __init__(self, size=10):
        """Create an empty table with `size` slots (None means empty)."""
        self.size = size                # total number of slots
        self.table = [None] * size      # None means the slot is empty
        self.count = 0                  # how many items are stored

    def _hash(self, key):
        """Convert a key into its home slot index (0 to size-1)."""
        hash_value = 0
        for char in str(key):
            hash_value = hash_value * HASH_MULTIPLIER + ord(char)  # combine characters
        return hash_value % self.size             # squeeze into table range

    def insert(self, key, value):
        """Insert using linear probing. Returns (index, home);
           index is -1 if the key is a duplicate or the table is full."""
        home = self._hash(key)

        for step in range(self.size):
            index = (home + step) % self.size     # linear probing
            slot = self.table[index]

            if slot is None:                      # empty slot found
                self.table[index] = Slot(key, value)
                self.count += 1
                return index, home

            if slot.key == key:                   # duplicate key
                return -1, home

        return -1, home                           # checked every slot: table full

    def delete(self, key):
        """Remove the item with this key. Return True if removed, False if not found.

        Rebuilds the table from the remaining items so the probe chains stay correct."""
        if self.search(key) is None:
            return False

        remaining = []                            # everything except the deleted item
        for slot in self.table:
            if slot is not None and slot.key != key:
                remaining.append((slot.key, slot.value))

        self.table = [None] * self.size           # start again with an empty table
        self.count = 0
        for k, v in remaining:
            self.insert(k, v)
        return True

    def search(self, key):
        """Return the value stored under key, or None if not found."""
        home = self._hash(key)
        for step in range(self.size):
            index = (home + step) % self.size
            slot = self.table[index]
            if slot is None:           # empty slot: key was never inserted
                return None
            if slot.key == key:
                return slot.value
        return None                    # checked every slot, not found
