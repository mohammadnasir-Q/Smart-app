import tkinter as tk
from tkinter import ttk, messagebox
import os

class BaseView:
    def __init__(self, title, geometry="800x600"):
        """Initialize the base view with common settings"""
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.resizable(True, True)
        
        # Apply background image or styling
        self.setup_appearance()
    
    def setup_appearance(self):
        """Set up the appearance with styling or background image"""
        # Set up theme and styling
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a modern theme
        
        # Configure colors
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        
        # If background image exists, use it
        self.bg_image = None
        bg_path = "images/background.png"
        if os.path.exists(bg_path):
            try:
                from PIL import Image, ImageTk
                img = Image.open(bg_path)
                img = img.resize((800, 600), Image.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                
                bg_label = tk.Label(self.root, image=self.bg_image)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                bg_label.lower()  # Make sure it's behind everything
            except Exception as e:
                print(f"Error loading background image: {str(e)}")
        
        # Create a main frame that will contain all widgets
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def show_message(self, title, message, message_type="info"):
        """Show a message dialog"""
        if message_type == "info":
            messagebox.showinfo(title, message)
        elif message_type == "error":
            messagebox.showerror(title, message)
        elif message_type == "warning":
            messagebox.showwarning(title, message)
    
    def create_label_entry(self, parent, label_text, row, column=0):
        """Create a label and entry pair"""
        ttk.Label(parent, text=label_text).grid(row=row, column=column, sticky=tk.W, padx=5, pady=5)
        entry = ttk.Entry(parent)
        entry.grid(row=row, column=column+1, sticky=tk.W+tk.E, padx=5, pady=5)
        return entry
    
    def run(self):
        """Run the main event loop"""
        self.root.mainloop()
    
    def close(self):
        """Close the window"""
        self.root.destroy() 