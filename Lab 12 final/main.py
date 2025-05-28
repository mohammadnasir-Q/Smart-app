import os
import tkinter as tk
from controller.auth_controller import AuthController
from controller.admin_controller import AdminController
from controller.cashier_controller import CashierController
from view.login_view import LoginView
from view.admin_view import AdminView
from view.cashier_view import CashierView

class SmartMartApplication:
    def __init__(self):
        """Initialize the Smart Mart System application"""
        # Create necessary directories if they don't exist
        self.create_directories()
        
        # Create initial data files if they don't exist
        self.create_data_files()
        
        # Initialize controllers
        self.auth_controller = AuthController()
        
        # Start with login view
        self.show_login()
    
    def create_directories(self):
        """Create necessary directories if they don't exist"""
        directories = ["data", "images", "tests"]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def create_data_files(self):
        """Create initial data files if they don't exist"""
        # admin.txt
        if not os.path.exists("data/admin.txt"):
            with open("data/admin.txt", "w") as f:
                f.write("admin,admin123\n")
        
        # cashiers.txt
        if not os.path.exists("data/cashiers.txt"):
            with open("data/cashiers.txt", "w") as f:
                f.write("john,john123\n")
                f.write("mary,mary123\n")
                f.write("alex,alex123\n")
        
        # products.txt
        if not os.path.exists("data/products.txt"):
            with open("data/products.txt", "w") as f:
                # Electronics category
                f.write("Electronics,Laptop,1200.00,10\n")
                f.write("Electronics,Smartphone,800.00,15\n")
                f.write("Electronics,Tablet,500.00,20\n")
                f.write("Electronics,Headphones,150.00,30\n")
                f.write("Electronics,Smart Watch,250.00,25\n")
                # Clothing category
                f.write("Clothing,T-Shirt,20.00,50\n")
                f.write("Clothing,Jeans,50.00,40\n")
                f.write("Clothing,Jacket,80.00,30\n")
                f.write("Clothing,Sweater,40.00,35\n")
                f.write("Clothing,Dress,60.00,25\n")
                # Groceries category
                f.write("Groceries,Rice (1kg),5.00,100\n")
                f.write("Groceries,Pasta,3.00,80\n")
                f.write("Groceries,Milk,2.50,60\n")
                f.write("Groceries,Bread,2.00,70\n")
                f.write("Groceries,Eggs,3.50,50\n")
                # Home Decor category
                f.write("Home Decor,Lamp,45.00,20\n")
                f.write("Home Decor,Cushion,15.00,40\n")
                f.write("Home Decor,Vase,25.00,30\n")
                f.write("Home Decor,Picture Frame,20.00,35\n")
                f.write("Home Decor,Rug,75.00,15\n")
                # Books category
                f.write("Books,Fiction Novel,15.00,45\n")
                f.write("Books,Cookbook,25.00,30\n")
                f.write("Books,Biography,18.00,40\n")
                f.write("Books,Self-Help,22.00,35\n")
                f.write("Books,Academic,35.00,25\n")
        
        # bills.txt
        if not os.path.exists("data/bills.txt"):
            with open("data/bills.txt", "w") as f:
                pass  # Create empty file
    
    def show_login(self):
        """Show the login view"""
        self.current_view = LoginView(self.login)
        self.current_view.run()
    
    def login(self, username, password, role):
        """Handle login attempts"""
        success = self.auth_controller.login(username, password, role)
        
        if success:
            # Close login view
            self.current_view.close()
            
            # Show appropriate view based on role
            if self.auth_controller.is_admin():
                self.show_admin()
            elif self.auth_controller.is_cashier():
                self.show_cashier()
                
        return success
    
    def show_admin(self):
        """Show the admin view"""
        admin_controller = AdminController()
        self.current_view = AdminView(admin_controller, self.logout)
        self.current_view.run()
    
    def show_cashier(self):
        """Show the cashier view"""
        cashier_user = self.auth_controller.get_current_user()
        cashier_controller = CashierController(cashier_user)
        self.current_view = CashierView(cashier_controller, self.logout)
        self.current_view.run()
    
    def logout(self):
        """Handle logout and return to login screen"""
        self.auth_controller.logout()
        self.show_login()

if __name__ == "__main__":
    app = SmartMartApplication() 