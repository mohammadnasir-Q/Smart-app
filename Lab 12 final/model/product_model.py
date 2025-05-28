class Product:
    def __init__(self, category, name, price, stock):
        self.category = category
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

class ProductModel:
    def __init__(self):
        self.products_file = "data/products.txt"
    
    def get_all_products(self):
        """Get all products from products.txt"""
        products = []
        try:
            with open(self.products_file, 'r') as file:
                for line in file:
                    if line.strip():
                        category, name, price, stock = line.strip().split(',')
                        products.append(Product(category, name, price, stock))
        except FileNotFoundError:
            print("Products file not found.")
        return products
    
    def get_products_by_category(self, category):
        """Get products filtered by category"""
        return [p for p in self.get_all_products() if p.category == category]
    
    def get_categories(self):
        """Get unique categories from products"""
        products = self.get_all_products()
        return sorted(list(set(p.category for p in products)))
    
    def add_product(self, category, name, price, stock):
        """Add a new product to products.txt"""
        try:
            # Check if product already exists
            products = self.get_all_products()
            for product in products:
                if product.category == category and product.name == name:
                    return False, "Product already exists in this category"
            
            # Add new product
            with open(self.products_file, 'a') as file:
                file.write(f"{category},{name},{price},{stock}\n")
            return True, "Product added successfully"
        except Exception as e:
            return False, f"Error adding product: {str(e)}"
    
    def update_product(self, category, name, new_category, new_name, new_price, new_stock):
        """Update an existing product's details"""
        products = self.get_all_products()
        found = False
        
        try:
            with open(self.products_file, 'w') as file:
                for product in products:
                    if product.category == category and product.name == name:
                        file.write(f"{new_category},{new_name},{new_price},{new_stock}\n")
                        found = True
                    else:
                        file.write(f"{product.category},{product.name},{product.price},{product.stock}\n")
            return found, "Product updated successfully" if found else "Product not found"
        except Exception as e:
            return False, f"Error updating product: {str(e)}"
    
    def delete_product(self, category, name):
        """Delete a product from products.txt"""
        products = self.get_all_products()
        found = False
        
        try:
            with open(self.products_file, 'w') as file:
                for product in products:
                    if not (product.category == category and product.name == name):
                        file.write(f"{product.category},{product.name},{product.price},{product.stock}\n")
                    else:
                        found = True
            return found, "Product deleted successfully" if found else "Product not found"
        except Exception as e:
            return False, f"Error deleting product: {str(e)}"
    
    def update_stock(self, category, name, new_stock):
        """Update a product's stock"""
        products = self.get_all_products()
        found = False
        
        try:
            with open(self.products_file, 'w') as file:
                for product in products:
                    if product.category == category and product.name == name:
                        file.write(f"{product.category},{product.name},{product.price},{new_stock}\n")
                        found = True
                    else:
                        file.write(f"{product.category},{product.name},{product.price},{product.stock}\n")
            return found, "Stock updated successfully" if found else "Product not found"
        except Exception as e:
            return False, f"Error updating stock: {str(e)}" 