class BillItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.subtotal = product.price * quantity

class Bill:
    def __init__(self, cashier):
        self.cashier = cashier
        self.items = []
        self.total = 0.0
        self.payment_method = None
        self.discount = 0.0
        self.final_amount = 0.0
    
    def add_item(self, product, quantity):
        if quantity > product.stock:
            return False, f"Insufficient stock. Available: {product.stock}"
        
        item = BillItem(product, quantity)
        self.items.append(item)
        self.calculate_total()
        return True, f"{quantity} x {product.name} added to bill"
    
    def remove_item(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]
            self.calculate_total()
            return True, "Item removed from bill"
        return False, "Invalid item index"
    
    def calculate_total(self):
        self.total = sum(item.subtotal for item in self.items)
        return self.total
    
    def apply_payment_method(self, method):
        self.payment_method = method
        if method.lower() == "card":
            self.discount = self.total * 0.10  # 10% discount for card payment
        else:
            self.discount = 0.0
            
        self.final_amount = self.total - self.discount
        return self.final_amount

class BillModel:
    def __init__(self):
        self.bills_file = "data/bills.txt"
    
    def save_bill(self, bill):
        """Save bill details to bills.txt"""
        try:
            # Get the current bill number
            bill_number = self.get_next_bill_number()
            
            # Save bill summary
            with open(self.bills_file, 'a') as file:
                file.write(f"Bill {bill_number}: {bill.final_amount:.2f}\n")
                
            # Update product stock
            from model.product_model import ProductModel
            product_model = ProductModel()
            
            for item in bill.items:
                product = item.product
                new_stock = product.stock - item.quantity
                product_model.update_stock(product.category, product.name, new_stock)
                
            return True, f"Bill {bill_number} saved successfully"
        except Exception as e:
            return False, f"Error saving bill: {str(e)}"
    
    def get_next_bill_number(self):
        """Get the next bill number by counting existing bills"""
        try:
            with open(self.bills_file, 'r') as file:
                lines = file.readlines()
                return len(lines) + 1
        except FileNotFoundError:
            return 1 