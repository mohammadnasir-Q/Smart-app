from model.product_model import ProductModel
from model.bill_model import Bill, BillModel

class CashierController:
    def __init__(self, cashier_user):
        self.product_model = ProductModel()
        self.bill_model = BillModel()
        self.current_bill = Bill(cashier_user)
    
    def get_categories(self):
        """Get all product categories"""
        return self.product_model.get_categories()
    
    def get_products_by_category(self, category):
        """Get products by category"""
        return self.product_model.get_products_by_category(category)
    
    def add_to_cart(self, product, quantity):
        """Add a product to the current bill"""
        return self.current_bill.add_item(product, quantity)
    
    def remove_from_cart(self, index):
        """Remove a product from the current bill"""
        return self.current_bill.remove_item(index)
    
    def get_cart_items(self):
        """Get all items in the current bill"""
        return self.current_bill.items
    
    def calculate_total(self):
        """Calculate the total amount of the current bill"""
        return self.current_bill.calculate_total()
    
    def apply_payment_method(self, method):
        """Apply payment method and calculate final amount"""
        return self.current_bill.apply_payment_method(method)
    
    def save_bill(self):
        """Save the current bill"""
        return self.bill_model.save_bill(self.current_bill)
    
    def new_bill(self, cashier_user):
        """Create a new bill"""
        self.current_bill = Bill(cashier_user)
        return self.current_bill 