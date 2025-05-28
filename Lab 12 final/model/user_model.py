class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role  # 'admin' or 'cashier'

class UserModel:
    def __init__(self):
        self.admin_file = "data/admin.txt"
        self.cashiers_file = "data/cashiers.txt"
    
    def authenticate_admin(self, username, password):
        """Authenticate admin credentials against admin.txt"""
        try:
            with open(self.admin_file, 'r') as file:
                admin_data = file.read().strip().split(',')
                if len(admin_data) >= 2 and username == admin_data[0] and password == admin_data[1]:
                    return User(username, password, 'admin')
        except FileNotFoundError:
            print("Admin file not found.")
        return None
    
    def authenticate_cashier(self, username, password):
        """Authenticate cashier credentials against cashiers.txt"""
        try:
            with open(self.cashiers_file, 'r') as file:
                for line in file:
                    cashier_data = line.strip().split(',')
                    if len(cashier_data) >= 2 and username == cashier_data[0] and password == cashier_data[1]:
                        return User(username, password, 'cashier')
        except FileNotFoundError:
            print("Cashiers file not found.")
        return None
    
    def get_all_cashiers(self):
        """Get list of all cashiers"""
        cashiers = []
        try:
            with open(self.cashiers_file, 'r') as file:
                for line in file:
                    if line.strip():
                        username, password = line.strip().split(',')
                        cashiers.append(User(username, password, 'cashier'))
        except FileNotFoundError:
            print("Cashiers file not found.")
        return cashiers
    
    def add_cashier(self, username, password):
        """Add a new cashier to cashiers.txt"""
        try:
            # Check if username already exists
            cashiers = self.get_all_cashiers()
            for cashier in cashiers:
                if cashier.username == username:
                    return False, "Username already exists"
            
            # Add new cashier
            with open(self.cashiers_file, 'a') as file:
                file.write(f"{username},{password}\n")
            return True, "Cashier added successfully"
        except Exception as e:
            return False, f"Error adding cashier: {str(e)}"
    
    def update_cashier(self, old_username, new_username, new_password):
        """Update an existing cashier's details"""
        cashiers = self.get_all_cashiers()
        found = False
        
        try:
            with open(self.cashiers_file, 'w') as file:
                for cashier in cashiers:
                    if cashier.username == old_username:
                        file.write(f"{new_username},{new_password}\n")
                        found = True
                    else:
                        file.write(f"{cashier.username},{cashier.password}\n")
            return found, "Cashier updated successfully" if found else "Cashier not found"
        except Exception as e:
            return False, f"Error updating cashier: {str(e)}"
    
    def delete_cashier(self, username):
        """Delete a cashier from cashiers.txt"""
        cashiers = self.get_all_cashiers()
        found = False
        
        try:
            with open(self.cashiers_file, 'w') as file:
                for cashier in cashiers:
                    if cashier.username != username:
                        file.write(f"{cashier.username},{cashier.password}\n")
                    else:
                        found = True
            return found, "Cashier deleted successfully" if found else "Cashier not found"
        except Exception as e:
            return False, f"Error deleting cashier: {str(e)}" 