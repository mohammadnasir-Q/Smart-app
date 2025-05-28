from model.user_model import UserModel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()
        self.current_user = None
    
    def login(self, username, password, role):
        """Authenticate user based on role"""
        if role == 'admin':
            self.current_user = self.user_model.authenticate_admin(username, password)
        elif role == 'cashier':
            self.current_user = self.user_model.authenticate_cashier(username, password)
        
        return self.current_user is not None
    
    def logout(self):
        """Log out the current user"""
        self.current_user = None
    
    def get_current_user(self):
        """Get the currently logged in user"""
        return self.current_user
    
    def is_admin(self):
        """Check if current user is an admin"""
        return self.current_user is not None and self.current_user.role == 'admin'
    
    def is_cashier(self):
        """Check if current user is a cashier"""
        return self.current_user is not None and self.current_user.role == 'cashier' 