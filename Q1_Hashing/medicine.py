class Medicine:
    """Entity class representing one product sold in the pharmacy."""

    def __init__(self, product_id, name, category, price, quantity):
        """Create a medicine; product_id is the unique 4-digit hash key."""
        self.product_id = product_id      # str, 4-digit ID like "1023", unique key
        self.name = name                  # str
        self.category = category          # str
        self.price = price                # float, RM per unit
        self.quantity = quantity          # int, units in stock

    def __str__(self):
        """Return a multi-line detailed description of the medicine."""
        return (f"Product ID: {self.product_id}"
                f"\nName: {self.name}"
                f"\nCategory: {self.category}"
                f"\nPrice: RM{self.price:.2f}"
                f"\nQuantity: {self.quantity}")

    def row(self):
        """Return a one-line, column-aligned description used in the list view."""
        return (f"{self.product_id:<8} | {self.name:<22} | {self.category:<13} | "
                f"RM{self.price:>7.2f} | {self.quantity:>4}")
