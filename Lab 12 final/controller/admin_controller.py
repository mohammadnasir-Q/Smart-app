from model.user_model import UserModel
from model.product_model import ProductModel

class AdminController:
    def __init__(self):
        self.user_model = UserModel()
        self.product_model = ProductModel()
    
    # Cashier management
    def get_all_cashiers(self):
        """Get all cashier accounts"""
        return self.user_model.get_all_cashiers()
    
    def add_cashier(self, username, password):
        """Add a new cashier account"""
        return self.user_model.add_cashier(username, password)
    
    def update_cashier(self, old_username, new_username, new_password):
        """Update an existing cashier account"""
        return self.user_model.update_cashier(old_username, new_username, new_password)
    
    def delete_cashier(self, username):
        """Delete a cashier account"""
        return self.user_model.delete_cashier(username)
    
    # Product management
    def get_all_products(self):
        """Get all products"""
        return self.product_model.get_all_products()
    
    def get_categories(self):
        """Get all product categories"""
        return self.product_model.get_categories()
    
    def get_products_by_category(self, category):
        """Get products by category"""
        return self.product_model.get_products_by_category(category)
    
    def add_product(self, category, name, price, stock):
        """Add a new product"""
        return self.product_model.add_product(category, name, price, stock)
    
    def update_product(self, category, name, new_category, new_name, new_price, new_stock):
        """Update an existing product"""
        return self.product_model.update_product(category, name, new_category, new_name, new_price, new_stock)
    
    def delete_product(self, category, name):
        """Delete a product"""
        return self.product_model.delete_product(category, name)
    
    def update_stock(self, category, name, new_stock):
        """Update a product's stock"""
        return self.product_model.update_stock(category, name, new_stock) 