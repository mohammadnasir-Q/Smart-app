import tkinter as tk
from tkinter import ttk
from view.base_view import BaseView

class AdminView(BaseView):
    def __init__(self, admin_controller, logout_callback=None):
        """Initialize the admin view"""
        super().__init__("Admin Panel", "900x700")
        
        self.admin_controller = admin_controller
        self.logout_callback = logout_callback
        
        # Create notebook for different tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create dashboard tab
        self.create_dashboard_tab()
        
        # Create cashier management tab
        self.create_cashier_tab()
        
        # Create product management tab
        self.create_product_tab()
        
        # Create stock management tab
        self.create_stock_tab()
        
        # Create toolbar with logout button
        self.create_toolbar()
    
    def create_toolbar(self):
        """Create toolbar with logout button"""
        toolbar = ttk.Frame(self.main_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        # Logged in as label
        ttk.Label(toolbar, text="Admin Panel", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Logout button
        logout_btn = ttk.Button(toolbar, text="Logout", command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=5)
    
    def create_dashboard_tab(self):
        """Create dashboard tab with summary information"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Welcome message
        welcome_frame = ttk.Frame(dashboard_frame)
        welcome_frame.pack(pady=20, fill=tk.X)
        welcome_label = ttk.Label(welcome_frame, text="Welcome to Admin Panel", font=("Arial", 16, "bold"))
        welcome_label.pack()
        
        # Summary panels
        summary_frame = ttk.Frame(dashboard_frame)
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure grid
        summary_frame.columnconfigure(0, weight=1)
        summary_frame.columnconfigure(1, weight=1)
        summary_frame.rowconfigure(0, weight=1)
        summary_frame.rowconfigure(1, weight=1)
        
        # Cashier summary
        cashier_frame = self.create_summary_panel(summary_frame, "Cashier Accounts", 0, 0)
        # Product summary
        product_frame = self.create_summary_panel(summary_frame, "Product Categories", 0, 1)
        # Category summary
        category_frame = self.create_summary_panel(summary_frame, "Total Products", 1, 0)
        # Stock summary
        stock_frame = self.create_summary_panel(summary_frame, "Low Stock Items", 1, 1)
        
        # Refresh dashboard
        self.refresh_dashboard()
    
    def create_summary_panel(self, parent, title, row, column):
        """Create a summary panel for the dashboard"""
        frame = ttk.Frame(parent, relief=tk.RIDGE, borderwidth=2)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        
        # Title
        ttk.Label(frame, text=title, font=("Arial", 12, "bold")).pack(pady=5)
        
        # Content label
        content_label = ttk.Label(frame, text="Loading...", font=("Arial", 16))
        content_label.pack(pady=20)
        
        # Store the content label for updating
        frame.content_label = content_label
        
        return frame
    
    def refresh_dashboard(self):
        """Refresh dashboard with latest data"""
        # Update cashier count
        cashiers = self.admin_controller.get_all_cashiers()
        cashier_frame = self.notebook.nametowidget(self.notebook.select()).winfo_children()[1].winfo_children()[0]
        cashier_frame.content_label.config(text=str(len(cashiers)))
        
        # Update category count
        categories = self.admin_controller.get_categories()
        product_frame = self.notebook.nametowidget(self.notebook.select()).winfo_children()[1].winfo_children()[1]
        product_frame.content_label.config(text=str(len(categories)))
        
        # Update product count
        products = self.admin_controller.get_all_products()
        category_frame = self.notebook.nametowidget(self.notebook.select()).winfo_children()[1].winfo_children()[2]
        category_frame.content_label.config(text=str(len(products)))
        
        # Update low stock count
        low_stock = [p for p in products if p.stock < 10]
        stock_frame = self.notebook.nametowidget(self.notebook.select()).winfo_children()[1].winfo_children()[3]
        stock_frame.content_label.config(text=str(len(low_stock)))
    
    def create_cashier_tab(self):
        """Create cashier management tab"""
        cashier_frame = ttk.Frame(self.notebook)
        self.notebook.add(cashier_frame, text="Cashier Management")
        
        # Split into left and right panes
        cashier_frame.columnconfigure(0, weight=2)
        cashier_frame.columnconfigure(1, weight=3)
        cashier_frame.rowconfigure(0, weight=1)
        
        # Left pane - Add/Edit cashier
        left_frame = ttk.Frame(cashier_frame, relief=tk.RIDGE, borderwidth=2)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(left_frame, text="Cashier Details", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Form for cashier details
        form_frame = ttk.Frame(left_frame)
        form_frame.pack(padx=10, pady=10, fill=tk.X)
        
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.cashier_username = ttk.Entry(form_frame)
        self.cashier_username.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.cashier_password = ttk.Entry(form_frame, show="*")
        self.cashier_password.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Buttons for actions
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(pady=10)
        
        self.add_cashier_btn = ttk.Button(btn_frame, text="Add Cashier", command=self.add_cashier)
        self.add_cashier_btn.pack(side=tk.LEFT, padx=5)
        
        self.update_cashier_btn = ttk.Button(btn_frame, text="Update Cashier", command=self.update_cashier)
        self.update_cashier_btn.pack(side=tk.LEFT, padx=5)
        self.update_cashier_btn.config(state=tk.DISABLED)
        
        self.delete_cashier_btn = ttk.Button(btn_frame, text="Delete Cashier", command=self.delete_cashier)
        self.delete_cashier_btn.pack(side=tk.LEFT, padx=5)
        self.delete_cashier_btn.config(state=tk.DISABLED)
        
        self.clear_cashier_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_cashier_form)
        self.clear_cashier_btn.pack(side=tk.LEFT, padx=5)
        
        # Right pane - Cashier list
        right_frame = ttk.Frame(cashier_frame, relief=tk.RIDGE, borderwidth=2)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(right_frame, text="Cashier Accounts", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Treeview for cashier list
        self.cashier_tree = ttk.Treeview(right_frame, columns=("username", "password"), show="headings")
        self.cashier_tree.heading("username", text="Username")
        self.cashier_tree.heading("password", text="Password")
        self.cashier_tree.column("username", width=150)
        self.cashier_tree.column("password", width=150)
        self.cashier_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind treeview selection
        self.cashier_tree.bind("<<TreeviewSelect>>", self.on_cashier_select)
        
        # Load cashiers
        self.refresh_cashier_list()
    
    def refresh_cashier_list(self):
        """Refresh the cashier list"""
        # Clear the tree
        for item in self.cashier_tree.get_children():
            self.cashier_tree.delete(item)
            
        # Load cashiers
        cashiers = self.admin_controller.get_all_cashiers()
        for cashier in cashiers:
            masked_password = "*" * len(cashier.password)
            self.cashier_tree.insert("", tk.END, values=(cashier.username, masked_password))
    
    def on_cashier_select(self, event=None):
        """Handle cashier selection in treeview"""
        selected = self.cashier_tree.focus()
        if selected:
            values = self.cashier_tree.item(selected, "values")
            self.cashier_username.delete(0, tk.END)
            self.cashier_password.delete(0, tk.END)
            self.cashier_username.insert(0, values[0])
            # Password is masked in the tree view, so don't set it
            
            # Enable update and delete buttons
            self.update_cashier_btn.config(state=tk.NORMAL)
            self.delete_cashier_btn.config(state=tk.NORMAL)
    
    def add_cashier(self):
        """Add a new cashier"""
        username = self.cashier_username.get().strip()
        password = self.cashier_password.get().strip()
        
        if not username or not password:
            self.show_message("Error", "Username and password are required", "error")
            return
        
        success, message = self.admin_controller.add_cashier(username, password)
        if success:
            self.show_message("Success", message)
            self.clear_cashier_form()
            self.refresh_cashier_list()
            self.refresh_dashboard()
        else:
            self.show_message("Error", message, "error")
    
    def update_cashier(self):
        """Update an existing cashier"""
        selected = self.cashier_tree.focus()
        if not selected:
            self.show_message("Error", "No cashier selected", "error")
            return
        
        old_username = self.cashier_tree.item(selected, "values")[0]
        new_username = self.cashier_username.get().strip()
        new_password = self.cashier_password.get().strip()
        
        if not new_username or not new_password:
            self.show_message("Error", "Username and password are required", "error")
            return
        
        success, message = self.admin_controller.update_cashier(old_username, new_username, new_password)
        if success:
            self.show_message("Success", message)
            self.clear_cashier_form()
            self.refresh_cashier_list()
        else:
            self.show_message("Error", message, "error")
    
    def delete_cashier(self):
        """Delete an existing cashier"""
        selected = self.cashier_tree.focus()
        if not selected:
            self.show_message("Error", "No cashier selected", "error")
            return
        
        username = self.cashier_tree.item(selected, "values")[0]
        
        success, message = self.admin_controller.delete_cashier(username)
        if success:
            self.show_message("Success", message)
            self.clear_cashier_form()
            self.refresh_cashier_list()
            self.refresh_dashboard()
        else:
            self.show_message("Error", message, "error")
    
    def clear_cashier_form(self):
        """Clear the cashier form"""
        self.cashier_username.delete(0, tk.END)
        self.cashier_password.delete(0, tk.END)
        self.update_cashier_btn.config(state=tk.DISABLED)
        self.delete_cashier_btn.config(state=tk.DISABLED)
        
        # Clear selection in treeview
        for selected in self.cashier_tree.selection():
            self.cashier_tree.selection_remove(selected)
    
    def create_product_tab(self):
        """Create product management tab"""
        product_frame = ttk.Frame(self.notebook)
        self.notebook.add(product_frame, text="Product Management")
        
        # Split into left and right panes
        product_frame.columnconfigure(0, weight=2)
        product_frame.columnconfigure(1, weight=3)
        product_frame.rowconfigure(0, weight=1)
        
        # Left pane - Add/Edit product
        left_frame = ttk.Frame(product_frame, relief=tk.RIDGE, borderwidth=2)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(left_frame, text="Product Details", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Form for product details
        form_frame = ttk.Frame(left_frame)
        form_frame.pack(padx=10, pady=10, fill=tk.X)
        
        ttk.Label(form_frame, text="Category:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.product_category = ttk.Combobox(form_frame)
        self.product_category.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Product Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.product_name = ttk.Entry(form_frame)
        self.product_name.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Price:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.product_price = ttk.Entry(form_frame)
        self.product_price.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Stock:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.product_stock = ttk.Entry(form_frame)
        self.product_stock.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Buttons for actions
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(pady=10)
        
        self.add_product_btn = ttk.Button(btn_frame, text="Add Product", command=self.add_product)
        self.add_product_btn.pack(side=tk.LEFT, padx=5)
        
        self.update_product_btn = ttk.Button(btn_frame, text="Update Product", command=self.update_product)
        self.update_product_btn.pack(side=tk.LEFT, padx=5)
        self.update_product_btn.config(state=tk.DISABLED)
        
        self.delete_product_btn = ttk.Button(btn_frame, text="Delete Product", command=self.delete_product)
        self.delete_product_btn.pack(side=tk.LEFT, padx=5)
        self.delete_product_btn.config(state=tk.DISABLED)
        
        self.clear_product_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_product_form)
        self.clear_product_btn.pack(side=tk.LEFT, padx=5)
        
        # Right pane - Product list
        right_frame = ttk.Frame(product_frame, relief=tk.RIDGE, borderwidth=2)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(right_frame, text="Products", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Category filter
        filter_frame = ttk.Frame(right_frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Filter by Category:").pack(side=tk.LEFT, padx=5)
        self.filter_category = ttk.Combobox(filter_frame, width=30)
        self.filter_category.pack(side=tk.LEFT, padx=5)
        
        # Treeview for product list
        self.product_tree = ttk.Treeview(right_frame, columns=("category", "name", "price", "stock"), show="headings")
        self.product_tree.heading("category", text="Category")
        self.product_tree.heading("name", text="Product Name")
        self.product_tree.heading("price", text="Price")
        self.product_tree.heading("stock", text="Stock")
        self.product_tree.column("category", width=100)
        self.product_tree.column("name", width=150)
        self.product_tree.column("price", width=80)
        self.product_tree.column("stock", width=80)
        self.product_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind treeview selection
        self.product_tree.bind("<<TreeviewSelect>>", self.on_product_select)
        
        # Bind category filter change
        self.filter_category.bind("<<ComboboxSelected>>", self.filter_products)
        
        # Load categories
        self.refresh_categories()
        
        # Load products
        self.refresh_product_list()
    
    def refresh_categories(self):
        """Refresh the category dropdowns"""
        categories = self.admin_controller.get_categories()
        
        # Update category dropdown in product form
        self.product_category["values"] = categories
        if categories:
            self.product_category.current(0)
        
        # Update category filter dropdown
        self.filter_category["values"] = ["All Categories"] + categories
        self.filter_category.current(0)
    
    def refresh_product_list(self):
        """Refresh the product list"""
        # Clear the tree
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
            
        # Get filter category
        filter_category = self.filter_category.get()
        
        # Load products
        if filter_category == "All Categories":
            products = self.admin_controller.get_all_products()
        else:
            products = self.admin_controller.get_products_by_category(filter_category)
            
        for product in products:
            self.product_tree.insert("", tk.END, values=(
                product.category, product.name, f"${product.price:.2f}", product.stock
            ))
    
    def filter_products(self, event=None):
        """Filter products by category"""
        self.refresh_product_list()
    
    def on_product_select(self, event=None):
        """Handle product selection in treeview"""
        selected = self.product_tree.focus()
        if selected:
            values = self.product_tree.item(selected, "values")
            
            self.product_category.set(values[0])
            self.product_name.delete(0, tk.END)
            self.product_name.insert(0, values[1])
            self.product_price.delete(0, tk.END)
            self.product_price.insert(0, values[2].replace("$", ""))
            self.product_stock.delete(0, tk.END)
            self.product_stock.insert(0, values[3])
            
            # Enable update and delete buttons
            self.update_product_btn.config(state=tk.NORMAL)
            self.delete_product_btn.config(state=tk.NORMAL)
    
    def add_product(self):
        """Add a new product"""
        category = self.product_category.get().strip()
        name = self.product_name.get().strip()
        price = self.product_price.get().strip()
        stock = self.product_stock.get().strip()
        
        if not category or not name or not price or not stock:
            self.show_message("Error", "All fields are required", "error")
            return
        
        try:
            price = float(price)
            stock = int(stock)
            if price < 0 or stock < 0:
                raise ValueError()
        except ValueError:
            self.show_message("Error", "Price and stock must be positive numbers", "error")
            return
        
        success, message = self.admin_controller.add_product(category, name, price, stock)
        if success:
            self.show_message("Success", message)
            self.clear_product_form()
            self.refresh_categories()
            self.refresh_product_list()
            self.refresh_dashboard()
        else:
            self.show_message("Error", message, "error")
    
    def update_product(self):
        """Update an existing product"""
        selected = self.product_tree.focus()
        if not selected:
            self.show_message("Error", "No product selected", "error")
            return
        
        values = self.product_tree.item(selected, "values")
        old_category = values[0]
        old_name = values[1]
        
        new_category = self.product_category.get().strip()
        new_name = self.product_name.get().strip()
        new_price = self.product_price.get().strip()
        new_stock = self.product_stock.get().strip()
        
        if not new_category or not new_name or not new_price or not new_stock:
            self.show_message("Error", "All fields are required", "error")
            return
        
        try:
            new_price = float(new_price)
            new_stock = int(new_stock)
            if new_price < 0 or new_stock < 0:
                raise ValueError()
        except ValueError:
            self.show_message("Error", "Price and stock must be positive numbers", "error")
            return
        
        success, message = self.admin_controller.update_product(
            old_category, old_name, new_category, new_name, new_price, new_stock)
        if success:
            self.show_message("Success", message)
            self.clear_product_form()
            self.refresh_categories()
            self.refresh_product_list()
        else:
            self.show_message("Error", message, "error")
    
    def delete_product(self):
        """Delete an existing product"""
        selected = self.product_tree.focus()
        if not selected:
            self.show_message("Error", "No product selected", "error")
            return
        
        values = self.product_tree.item(selected, "values")
        category = values[0]
        name = values[1]
        
        success, message = self.admin_controller.delete_product(category, name)
        if success:
            self.show_message("Success", message)
            self.clear_product_form()
            self.refresh_categories()
            self.refresh_product_list()
            self.refresh_dashboard()
        else:
            self.show_message("Error", message, "error")
    
    def clear_product_form(self):
        """Clear the product form"""
        self.product_name.delete(0, tk.END)
        self.product_price.delete(0, tk.END)
        self.product_stock.delete(0, tk.END)
        self.update_product_btn.config(state=tk.DISABLED)
        self.delete_product_btn.config(state=tk.DISABLED)
        
        # Clear selection in treeview
        for selected in self.product_tree.selection():
            self.product_tree.selection_remove(selected)
    
    def create_stock_tab(self):
        """Create stock management tab"""
        stock_frame = ttk.Frame(self.notebook)
        self.notebook.add(stock_frame, text="Stock Management")
        
        # Title
        ttk.Label(stock_frame, text="Update Stock Levels", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Category filter
        filter_frame = ttk.Frame(stock_frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Filter by Category:").pack(side=tk.LEFT, padx=5)
        self.stock_filter_category = ttk.Combobox(filter_frame, width=30)
        self.stock_filter_category.pack(side=tk.LEFT, padx=5)
        
        # Treeview for stock list
        self.stock_tree = ttk.Treeview(stock_frame, columns=("category", "name", "price", "stock"), show="headings")
        self.stock_tree.heading("category", text="Category")
        self.stock_tree.heading("name", text="Product Name")
        self.stock_tree.heading("price", text="Price")
        self.stock_tree.heading("stock", text="Stock")
        self.stock_tree.column("category", width=100)
        self.stock_tree.column("name", width=150)
        self.stock_tree.column("price", width=80)
        self.stock_tree.column("stock", width=80)
        self.stock_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Update stock panel
        update_frame = ttk.Frame(stock_frame)
        update_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(update_frame, text="Selected Product:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.selected_product_label = ttk.Label(update_frame, text="None")
        self.selected_product_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(update_frame, text="Current Stock:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.current_stock_label = ttk.Label(update_frame, text="0")
        self.current_stock_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(update_frame, text="New Stock:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.new_stock_entry = ttk.Entry(update_frame)
        self.new_stock_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        update_stock_btn = ttk.Button(update_frame, text="Update Stock", command=self.update_stock)
        update_stock_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        # Bind treeview selection
        self.stock_tree.bind("<<TreeviewSelect>>", self.on_stock_select)
        
        # Bind category filter change
        self.stock_filter_category.bind("<<ComboboxSelected>>", self.filter_stock)
        
        # Load categories
        self.refresh_stock_categories()
        
        # Load products
        self.refresh_stock_list()
    
    def refresh_stock_categories(self):
        """Refresh the stock category dropdown"""
        categories = self.admin_controller.get_categories()
        
        # Update category filter dropdown
        self.stock_filter_category["values"] = ["All Categories"] + categories
        self.stock_filter_category.current(0)
    
    def refresh_stock_list(self):
        """Refresh the stock list"""
        # Clear the tree
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
            
        # Get filter category
        filter_category = self.stock_filter_category.get()
        
        # Load products
        if filter_category == "All Categories":
            products = self.admin_controller.get_all_products()
        else:
            products = self.admin_controller.get_products_by_category(filter_category)
            
        for product in products:
            self.stock_tree.insert("", tk.END, values=(
                product.category, product.name, f"${product.price:.2f}", product.stock
            ))
    
    def filter_stock(self, event=None):
        """Filter stock by category"""
        self.refresh_stock_list()
    
    def on_stock_select(self, event=None):
        """Handle stock selection in treeview"""
        selected = self.stock_tree.focus()
        if selected:
            values = self.stock_tree.item(selected, "values")
            
            self.selected_product_label.config(text=f"{values[0]} - {values[1]}")
            self.current_stock_label.config(text=values[3])
            self.new_stock_entry.delete(0, tk.END)
            self.new_stock_entry.insert(0, values[3])
    
    def update_stock(self):
        """Update stock for a product"""
        selected = self.stock_tree.focus()
        if not selected:
            self.show_message("Error", "No product selected", "error")
            return
        
        values = self.stock_tree.item(selected, "values")
        category = values[0]
        name = values[1]
        
        try:
            new_stock = int(self.new_stock_entry.get())
            if new_stock < 0:
                raise ValueError()
        except ValueError:
            self.show_message("Error", "Stock must be a positive integer", "error")
            return
        
        success, message = self.admin_controller.update_stock(category, name, new_stock)
        if success:
            self.show_message("Success", message)
            self.refresh_stock_list()
            self.refresh_dashboard()
        else:
            self.show_message("Error", message, "error")
    
    def logout(self):
        """Log out and return to login screen"""
        if self.logout_callback:
            self.logout_callback()
            self.close() 