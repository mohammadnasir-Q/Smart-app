import tkinter as tk
from tkinter import ttk
from view.base_view import BaseView

class CashierView(BaseView):
    def __init__(self, cashier_controller, logout_callback=None):
        """Initialize the cashier view"""
        super().__init__("Cashier Panel", "900x600")
        
        self.cashier_controller = cashier_controller
        self.logout_callback = logout_callback
        
        # Split the main frame into left and right sections
        self.main_frame.columnconfigure(0, weight=3)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create left section (product browsing)
        self.create_product_section()
        
        # Create right section (cart and billing)
        self.create_cart_section()
    
    def create_toolbar(self):
        """Create toolbar with cashier info and logout button"""
        toolbar = ttk.Frame(self.main_frame)
        toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Cashier label
        cashier_name = self.cashier_controller.current_bill.cashier.username
        cashier_label = ttk.Label(toolbar, text=f"Cashier: {cashier_name}", font=("Arial", 12, "bold"))
        cashier_label.pack(side=tk.LEFT, padx=5)
        
        # Logout button
        logout_btn = ttk.Button(toolbar, text="Logout", command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=5)
    
    def create_product_section(self):
        """Create the product browsing section"""
        product_frame = ttk.Frame(self.main_frame, relief=tk.RIDGE, borderwidth=2)
        product_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Title
        ttk.Label(product_frame, text="Products", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Category selection
        category_frame = ttk.Frame(product_frame)
        category_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(category_frame, text="Category:").pack(side=tk.LEFT, padx=5)
        self.category_combo = ttk.Combobox(category_frame, width=30)
        self.category_combo.pack(side=tk.LEFT, padx=5)
        
        # Load categories
        categories = self.cashier_controller.get_categories()
        self.category_combo["values"] = categories
        if categories:
            self.category_combo.current(0)
        
        # Bind category selection change
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_change)
        
        # Product list
        product_list_frame = ttk.Frame(product_frame)
        product_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Product treeview
        self.product_tree = ttk.Treeview(product_list_frame, columns=("name", "price", "stock"), show="headings")
        self.product_tree.heading("name", text="Product Name")
        self.product_tree.heading("price", text="Price")
        self.product_tree.heading("stock", text="Available")
        self.product_tree.column("name", width=200)
        self.product_tree.column("price", width=100)
        self.product_tree.column("stock", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(product_list_frame, orient="vertical", command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.product_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add to cart section
        add_frame = ttk.Frame(product_frame)
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(add_frame, text="Quantity:").pack(side=tk.LEFT, padx=5)
        self.quantity_entry = ttk.Entry(add_frame, width=10)
        self.quantity_entry.pack(side=tk.LEFT, padx=5)
        self.quantity_entry.insert(0, "1")
        
        add_btn = ttk.Button(add_frame, text="Add to Cart", command=self.add_to_cart)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Load products for initial category
        self.load_products_for_category()
    
    def create_cart_section(self):
        """Create the cart and billing section"""
        cart_frame = ttk.Frame(self.main_frame, relief=tk.RIDGE, borderwidth=2)
        cart_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Title
        ttk.Label(cart_frame, text="Shopping Cart", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Cart items
        cart_list_frame = ttk.Frame(cart_frame)
        cart_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Cart treeview
        self.cart_tree = ttk.Treeview(cart_list_frame, columns=("name", "price", "quantity", "subtotal"), show="headings")
        self.cart_tree.heading("name", text="Product")
        self.cart_tree.heading("price", text="Price")
        self.cart_tree.heading("quantity", text="Qty")
        self.cart_tree.heading("subtotal", text="Subtotal")
        self.cart_tree.column("name", width=150)
        self.cart_tree.column("price", width=80)
        self.cart_tree.column("quantity", width=50)
        self.cart_tree.column("subtotal", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(cart_list_frame, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Remove item button
        remove_btn = ttk.Button(cart_frame, text="Remove Selected Item", command=self.remove_from_cart)
        remove_btn.pack(pady=5)
        
        # Totals section
        totals_frame = ttk.Frame(cart_frame, relief=tk.GROOVE, borderwidth=2)
        totals_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Subtotal row
        subtotal_frame = ttk.Frame(totals_frame)
        subtotal_frame.pack(fill=tk.X, pady=2)
        ttk.Label(subtotal_frame, text="Subtotal:").pack(side=tk.LEFT, padx=5)
        self.subtotal_label = ttk.Label(subtotal_frame, text="$0.00")
        self.subtotal_label.pack(side=tk.RIGHT, padx=5)
        
        # Discount row
        discount_frame = ttk.Frame(totals_frame)
        discount_frame.pack(fill=tk.X, pady=2)
        ttk.Label(discount_frame, text="Discount:").pack(side=tk.LEFT, padx=5)
        self.discount_label = ttk.Label(discount_frame, text="$0.00")
        self.discount_label.pack(side=tk.RIGHT, padx=5)
        
        # Total row
        total_frame = ttk.Frame(totals_frame)
        total_frame.pack(fill=tk.X, pady=2)
        ttk.Label(total_frame, text="Total:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.total_label = ttk.Label(total_frame, text="$0.00", font=("Arial", 10, "bold"))
        self.total_label.pack(side=tk.RIGHT, padx=5)
        
        # Payment method section
        payment_frame = ttk.Frame(cart_frame)
        payment_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(payment_frame, text="Payment Method:").pack(side=tk.LEFT, padx=5)
        self.payment_var = tk.StringVar(value="cash")
        cash_radio = ttk.Radiobutton(payment_frame, text="Cash", variable=self.payment_var, value="cash", command=self.on_payment_change)
        cash_radio.pack(side=tk.LEFT, padx=5)
        card_radio = ttk.Radiobutton(payment_frame, text="Card (10% discount)", variable=self.payment_var, value="card", command=self.on_payment_change)
        card_radio.pack(side=tk.LEFT)
        
        # Payment button
        pay_btn = ttk.Button(cart_frame, text="Complete Payment", command=self.complete_payment)
        pay_btn.pack(pady=10)
    
    def on_category_change(self, event=None):
        """Handle category selection change"""
        self.load_products_for_category()
    
    def load_products_for_category(self):
        """Load products for the selected category"""
        # Clear the treeview
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Get selected category
        category = self.category_combo.get()
        
        # Load products
        products = self.cashier_controller.get_products_by_category(category)
        for product in products:
            self.product_tree.insert("", tk.END, values=(
                product.name, f"${product.price:.2f}", product.stock
            ), tags=(product.category, product.name))
    
    def add_to_cart(self):
        """Add selected product to cart"""
        selected = self.product_tree.focus()
        if not selected:
            self.show_message("Error", "No product selected", "error")
            return
        
        # Get selected product details
        values = self.product_tree.item(selected, "values")
        tags = self.product_tree.item(selected, "tags")
        category = tags[0]
        name = values[0]
        
        # Get quantity
        try:
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            self.show_message("Error", "Quantity must be a positive integer", "error")
            return
        
        # Get product object
        products = self.cashier_controller.get_products_by_category(category)
        product = next((p for p in products if p.name == name), None)
        
        if not product:
            self.show_message("Error", "Product not found", "error")
            return
        
        # Add to cart
        success, message = self.cashier_controller.add_to_cart(product, quantity)
        
        if success:
            self.show_message("Success", message)
            self.refresh_cart()
        else:
            self.show_message("Error", message, "error")
    
    def remove_from_cart(self):
        """Remove selected item from cart"""
        selected = self.cart_tree.focus()
        if not selected:
            self.show_message("Error", "No item selected", "error")
            return
        
        # Get index
        index = self.cart_tree.index(selected)
        
        # Remove from cart
        success, message = self.cashier_controller.remove_from_cart(index)
        
        if success:
            self.show_message("Success", message)
            self.refresh_cart()
        else:
            self.show_message("Error", message, "error")
    
    def refresh_cart(self):
        """Refresh the cart display"""
        # Clear the treeview
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Get cart items
        items = self.cashier_controller.get_cart_items()
        
        # Add to treeview
        for item in items:
            self.cart_tree.insert("", tk.END, values=(
                item.product.name,
                f"${item.product.price:.2f}",
                item.quantity,
                f"${item.subtotal:.2f}"
            ))
        
        # Update totals
        self.update_totals()
    
    def update_totals(self):
        """Update the totals display"""
        # Calculate subtotal
        subtotal = self.cashier_controller.calculate_total()
        self.subtotal_label.config(text=f"${subtotal:.2f}")
        
        # Apply payment method to get discount and total
        payment_method = self.payment_var.get()
        final_amount = self.cashier_controller.apply_payment_method(payment_method)
        
        # Get discount
        discount = self.cashier_controller.current_bill.discount
        self.discount_label.config(text=f"${discount:.2f}")
        
        # Update total
        self.total_label.config(text=f"${final_amount:.2f}")
    
    def on_payment_change(self, event=None):
        """Handle payment method change"""
        self.update_totals()
    
    def complete_payment(self):
        """Process payment and generate bill"""
        # Check if cart is empty
        items = self.cashier_controller.get_cart_items()
        if not items:
            self.show_message("Error", "Cart is empty", "error")
            return
        
        # Save bill
        success, message = self.cashier_controller.save_bill()
        
        if success:
            # Show success message with bill details
            bill_number = message.split(" ")[1]
            total = self.cashier_controller.current_bill.final_amount
            payment_method = self.payment_var.get().capitalize()
            
            success_message = f"Bill {bill_number} saved successfully.\n" + \
                             f"Total Amount: ${total:.2f}\n" + \
                             f"Payment Method: {payment_method}"
            
            self.show_message("Payment Complete", success_message)
            
            # Start a new bill
            self.cashier_controller.new_bill(self.cashier_controller.current_bill.cashier)
            
            # Refresh the cart display
            self.refresh_cart()
            
            # Refresh the product list to update stock
            self.load_products_for_category()
        else:
            self.show_message("Error", message, "error")
    
    def logout(self):
        """Log out and return to login screen"""
        if self.logout_callback:
            self.logout_callback()
            self.close() 