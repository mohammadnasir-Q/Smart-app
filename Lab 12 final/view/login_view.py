import tkinter as tk
from tkinter import ttk
from view.base_view import BaseView

class LoginView(BaseView):
    def __init__(self, login_callback=None):
        """Initialize the login view"""
        super().__init__("Smart Mart System Login", "400x300")
        
        self.login_callback = login_callback
        
        # Create the login frame
        self.login_frame = ttk.Frame(self.main_frame)
        self.login_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = ttk.Label(self.login_frame, text="Smart Mart System Login", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Username field
        username_frame = ttk.Frame(self.login_frame)
        username_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(username_frame, text="Username:").pack(side=tk.LEFT)
        self.username_entry = ttk.Entry(username_frame)
        self.username_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        
        # Password field
        password_frame = ttk.Frame(self.login_frame)
        password_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(password_frame, text="Password:").pack(side=tk.LEFT)
        self.password_entry = ttk.Entry(password_frame, show="*")
        self.password_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        
        # Role selection
        role_frame = ttk.Frame(self.login_frame)
        role_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(role_frame, text="Login as:").pack(side=tk.LEFT)
        self.role_var = tk.StringVar(value="cashier")
        admin_radio = ttk.Radiobutton(role_frame, text="Admin", variable=self.role_var, value="admin")
        admin_radio.pack(side=tk.LEFT, padx=5)
        cashier_radio = ttk.Radiobutton(role_frame, text="Cashier", variable=self.role_var, value="cashier")
        cashier_radio.pack(side=tk.LEFT)
        
        # Login button
        button_frame = ttk.Frame(self.login_frame)
        button_frame.pack(pady=20)
        login_button = ttk.Button(button_frame, text="Login", command=self.login)
        login_button.pack(padx=5)
        
        # Bind Enter key to login
        self.root.bind("<Return>", lambda event: self.login())
    
    def login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        
        if not username or not password:
            self.show_message("Error", "Username and password are required", "error")
            return
        
        if self.login_callback:
            success = self.login_callback(username, password, role)
            if not success:
                self.show_message("Error", "Invalid username or password", "error")
    
    def reset_fields(self):
        """Reset form fields"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus() 