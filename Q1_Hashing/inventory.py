from medicine import Medicine
from hash_table import HashTable
from performance_test import compare_search

TABLE_SIZE = 401
GENERATED_START = 1100      # first generated product ID
GENERATED_END = 1294        # one past the last generated ID (194 records)
GENERATED_PRICE = 9.00      # price given to every generated medicine
GENERATED_QUANTITY = 20     # stock given to every generated medicine


def load_sample_data(table, array):
    """Insert the pre-defined medicines into both the hash table and the array."""
    samples = [
        Medicine("1001", "Paracetamol 500mg", "Painkiller", 5.50, 120),
        Medicine("1048", "Amoxicillin 250mg", "Antibiotic", 12.80, 60),
        Medicine("1026", "Ibuprofen 400mg", "Painkiller", 8.90, 80),
        Medicine("1023", "Cetirizine 10mg", "Antihistamine", 6.20, 100),
        Medicine("1036", "Vitamin C 1000mg", "Supplement", 15.00, 200),
        Medicine("1010", "Omeprazole 20mg", "Antacid", 18.40, 45),
    ]
    for i in range(GENERATED_START, GENERATED_END):
        samples.append(Medicine(str(i), f"Medicine {i}", "General",
                                GENERATED_PRICE, GENERATED_QUANTITY))

    for m in samples:
        index, _ = table.insert(m.product_id, m)  # _ = home slot, not needed here
        if index != -1:
            array.append(m)


def insert_medicine(table, array):
    """Read a new medicine from the user, validate it, insert it into both
       structures and report whether a collision occurred."""
    print("\n--- Insert New Medicine ---")
    product_id = input("Enter Product ID: ").strip()
    if not (product_id.isdigit() and len(product_id) == 4 and product_id[0] == "1"):
        print("Invalid ID: it must be 4 digits starting with 1 (e.g. 1023).")
        return

    # Check the two failure cases first, so we can give a clear reason
    if table.search(product_id) is not None:
        print(f"{product_id} already exists. Medicine not inserted.")
        return
    if table.count == table.size:
        print(f"Could not insert {product_id}: table is full.")
        return

    name = input("Enter Product Name: ").strip()
    category = input("Enter Category: ").strip()
    try:
        price = float(input("Enter Price: "))
        quantity = int(input("Enter Stock Quantity: "))
    except ValueError:
        print("Invalid number entered. Medicine not added.")
        return

    if price < 0 or quantity < 0 or name == "":
        print("Invalid input: name required, price and quantity cannot be negative.")
        return

    medicine = Medicine(product_id, name, category, price, quantity)
    index, home = table.insert(product_id, medicine)
    array.append(medicine)  # keep the array identical to the table

    if index != home:
        probes = (index - home) % table.size  # how many slots it moved forward
        print(f"\nCollision for {product_id}: home slot {home} was occupied; "
              f"stored at slot {index} after {probes} probe(s).")
    else:
        print(f"Inserted {product_id} at home slot {home} (no collision).")

    print(f"Product inserted successfully, {product_id} at slot [{index}].")


def search_medicine(table, array):
    """Search a product ID in both structures and show the time each one took."""
    print("\n--- Search Medicine ---")
    product_id = input("Enter Product ID to search: ").strip()

    result, hash_time, array_time = compare_search(table, array, product_id)

    if result is None:
        print("Product not found.")
    else:
        print("Product Found!\n")
        print(result)
    print()
    print(f"Search completed in {hash_time:.6f} seconds (Hash Table)")
    print(f"Search completed in {array_time:.6f} seconds (Array - same record)")


def edit_medicine(table):
    """Edit the name, category, price and quantity of an existing medicine."""
    print("\n--- Edit Medicine ---")
    product_id = input("Enter Product ID to edit: ").strip()
    medicine = table.search(product_id)
    if medicine is None:
        print("Product not found.")
        return

    print("\nCurrent details:")
    print(medicine)
    print("\n(Press Enter to keep the current value)")
    name = input("Enter new Name: ").strip() or medicine.name
    category = input("Enter new Category: ").strip() or medicine.category
    price_text = input("Enter new Price: ").strip()
    qty_text = input("Enter new Stock Quantity: ").strip()

    try:
        price = float(price_text) if price_text else medicine.price
        quantity = int(qty_text) if qty_text else medicine.quantity
    except ValueError:
        print("Invalid number entered. No changes made.")
        return
    if price < 0 or quantity < 0:
        print("Price and quantity cannot be negative. No changes made.")
        return

    medicine.name = name
    medicine.category = category
    medicine.price = price
    medicine.quantity = quantity
    print("Product updated successfully.")


def delete_medicine(table, array):
    """Delete a medicine completely from the hash table and the array."""
    print("\n--- Delete Medicine ---")
    product_id = input("Enter Product ID to delete: ").strip()
    medicine = table.search(product_id)
    if medicine is None:
        print("Product not found.")
        return

    print(medicine)
    if input("Delete this product? (y/n): ").strip().lower() != "y":
        print("Deletion cancelled.")
        return

    table.delete(product_id)     # remove from the hash table
    array.remove(medicine)       # remove from the array
    print(f"Product {product_id} deleted.")


def list_all(table):
    """Display every stored medicine together with its slot number."""
    print("\n--- All Products ---")
    print(f"{'Slot':<5}| {'ID':<8} | {'Name':<22} | {'Category':<13} | "
          f"{'Price':>9} | {'Qty':>4}")
    print("-" * 78)
    for i, slot in enumerate(table.table): # the list of slots in the hash table
        if slot is not None:
            print(f"{i:<5}| {slot.value.row()}")


def main():
    """Create the structures, load sample data and run the menu loop."""
    table = HashTable(TABLE_SIZE)
    array = []                       # the one-dimensional array
    load_sample_data(table, array)

    while True:
        print("\n\n===== Pharmacy Inventory System =====")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. List all products")
        print("6. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            insert_medicine(table, array)
        elif choice == "2":
            search_medicine(table, array)
        elif choice == "3":
            edit_medicine(table)
        elif choice == "4":
            delete_medicine(table, array)
        elif choice == "5":
            list_all(table)
        elif choice == "6":
            print("Exiting Inventory System. Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1-6.")


if __name__ == "__main__":
    main()
