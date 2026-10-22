from medicine import Medicine
from hash_table import HashTable

TABLE_SIZE = 11


def load_sample_data(table):
    """Insert pre-defined records into the hash table."""
    samples = [
        Medicine("MED001", "Paracetamol 500mg", "Painkiller", 5.50, 120, "2027-06-30"),
        Medicine("MED002", "Amoxicillin 250mg", "Antibiotic", 12.80, 60, "2027-01-15"),
        Medicine("MED003", "Ibuprofen 400mg", "Painkiller", 8.90, 80, "2027-03-20"),
        Medicine("MED004", "Cetirizine 10mg", "Antihistamine", 6.20, 100, "2027-09-10"),
        Medicine("MED005", "Vitamin C 1000mg", "Supplement", 15.00, 200, "2028-02-28"),
        Medicine("MED006", "Omeprazole 20mg", "Antacid", 18.40, 45, "2027-05-05"),
    ]
    for m in samples:
        table.insert(m.product_id, m)


def insert_medicine(table):
    """Ask the user for details and insert a new medicine."""
    print("\n--- Insert New Medicine ---")
    product_id = input("Product ID: ").strip().upper()
    name = input("Name: ").strip()
    category = input("Category: ").strip()
    try:
        price = float(input("Price (RM): "))
        quantity = int(input("Quantity: "))
    except ValueError:
        print("Invalid number entered. Medicine not added.")
        return
    expiry = input("Expiry date (YYYY-MM-DD): ").strip()

    medicine = Medicine(product_id, name, category, price, quantity, expiry)
    index = table.insert(product_id, medicine)
    if index == -1:
        print("Could not insert: table is full or the ID already exists.")
    else:
        print(f"Inserted {product_id} at slot {index}.")


def search_medicine(table):
    """Search for a medicine by product ID."""
    print("\n--- Search Medicine ---")
    product_id = input("Enter Product ID: ").strip().upper()
    result = table.search(product_id)
    if result is None:
        print("Medicine not found.")
    else:
        print()
        print(result)


def list_all(table):
    """Show every stored medicine with its slot number."""
    print("\n--- All Medicines ---")
    print(f"{'Slot':<5}| {'ID':<8} | {'Name':<22} | {'Category':<13} | "
          f"{'Price':>9} | {'Qty':>4} | Expiry")
    print("-" * 85)
    for i, slot in enumerate(table.table):
        if slot is not None:
            print(f"{i:<5}| {slot.value.row()}")


def main():
    table = HashTable(TABLE_SIZE)
    load_sample_data(table)

    while True:
        print("\n===== Pharmacy Inventory System =====")
        print("1. Insert medicine")
        print("2. Search medicine")
        print("3. List all medicines")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            insert_medicine(table)
        elif choice == "2":
            search_medicine(table)
        elif choice == "3":
            list_all(table)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1-4.")


if __name__ == "__main__":
    main()
