import sys
import os
import pytest

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.user_model import UserModel, User

class TestUserModel:
    @pytest.fixture
    def user_model(self, tmp_path):
        """Create a temporary UserModel for testing"""
        # Create temporary admin.txt
        admin_file = tmp_path / "admin.txt"
        admin_file.write_text("testadmin,adminpass\n")
        
        # Create temporary cashiers.txt
        cashiers_file = tmp_path / "cashiers.txt"
        cashiers_file.write_text("john,john123\nmary,mary123\nalex,alex123\n")
        
        # Create user model with test files
        model = UserModel()
        model.admin_file = str(admin_file)
        model.cashiers_file = str(cashiers_file)
        
        return model
    
    def test_authenticate_admin_success(self, user_model):
        """Test that admin authentication works with correct credentials"""
        user = user_model.authenticate_admin("testadmin", "adminpass")
        assert user is not None
        assert user.username == "testadmin"
        assert user.password == "adminpass"
        assert user.role == "admin"
    
    def test_authenticate_admin_failure(self, user_model):
        """Test that admin authentication fails with incorrect credentials"""
        user = user_model.authenticate_admin("testadmin", "wrongpass")
        assert user is None
        
        user = user_model.authenticate_admin("wronguser", "adminpass")
        assert user is None
    
    def test_authenticate_cashier_success(self, user_model):
        """Test that cashier authentication works with correct credentials"""
        user = user_model.authenticate_cashier("john", "john123")
        assert user is not None
        assert user.username == "john"
        assert user.password == "john123"
        assert user.role == "cashier"
    
    def test_authenticate_cashier_failure(self, user_model):
        """Test that cashier authentication fails with incorrect credentials"""
        user = user_model.authenticate_cashier("john", "wrongpass")
        assert user is None
        
        user = user_model.authenticate_cashier("wronguser", "john123")
        assert user is None
    
    def test_get_all_cashiers(self, user_model):
        """Test getting all cashiers"""
        cashiers = user_model.get_all_cashiers()
        assert len(cashiers) == 3
        assert cashiers[0].username == "john"
        assert cashiers[1].username == "mary"
        assert cashiers[2].username == "alex"
    
    def test_add_cashier(self, user_model):
        """Test adding a new cashier"""
        success, _ = user_model.add_cashier("newcashier", "newpass")
        assert success is True
        
        # Check that the cashier was added
        cashiers = user_model.get_all_cashiers()
        assert len(cashiers) == 4
        assert cashiers[3].username == "newcashier"
        assert cashiers[3].password == "newpass"
    
    def test_add_duplicate_cashier(self, user_model):
        """Test adding a duplicate cashier fails"""
        success, _ = user_model.add_cashier("john", "newpass")
        assert success is False
        
        # Check that no cashier was added
        cashiers = user_model.get_all_cashiers()
        assert len(cashiers) == 3
    
    def test_update_cashier(self, user_model):
        """Test updating an existing cashier"""
        success, _ = user_model.update_cashier("john", "johnnew", "newpass")
        assert success is True
        
        # Check that the cashier was updated
        cashiers = user_model.get_all_cashiers()
        assert len(cashiers) == 3
        assert cashiers[0].username == "johnnew"
        assert cashiers[0].password == "newpass"
    
    def test_update_nonexistent_cashier(self, user_model):
        """Test updating a nonexistent cashier fails"""
        success, _ = user_model.update_cashier("nonexistent", "johnnew", "newpass")
        assert success is False
        
        # Check that no cashier was updated
        cashiers = user_model.get_all_cashiers()
        assert len(cashiers) == 3
        assert cashiers[0].username == "john"
    
    def test_delete_cashier(self, user_model):
        """Test deleting an existing cashier"""
        success, _ = user_model.delete_cashier("john")
        assert success is True
        
        # Check that the cashier was deleted
        cashiers = user_model.get_all_cashiers()
        assert len(cashiers) == 2
        assert cashiers[0].username == "mary"
        assert cashiers[1].username == "alex"
    
    def test_delete_nonexistent_cashier(self, user_model):
        """Test deleting a nonexistent cashier fails"""
        success, _ = user_model.delete_cashier("nonexistent")
        assert success is False
        
        # Check that no cashier was deleted
        cashiers = user_model.get_all_cashiers()
        assert len(cashiers) == 3 