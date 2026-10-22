class Medicine:
    def __init__(self, product_id, name, category, price, quantity, expiry_date):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.expiry_date = expiry_date

    def __str__(self):
        return (f"{self.product_id}"
                f"\n{self.name}"
                f"\n{self.category}"
                f"\nRM{self.price:.2f}"
                f"\nQuantity: {self.quantity}"
                f"\nExpiry Date: {self.expiry_date}")

    def row(self):
        """One-line view, used when listing many medicines."""
        return (f"{self.product_id:<8} | {self.name:<22} | {self.category:<13} | "
                f"RM{self.price:>7.2f} | {self.quantity:>4} | {self.expiry_date}")


# quick self-test (only runs when this file is run directly)
if __name__ == "__main__":
    m = Medicine("MED001", "Paracetamol 500mg", "Painkiller", 5.50, 120, "2027-06-30")
    print(m)
    print(m.row())
