import sys
import os
import pytest

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.bill_model import Bill, BillItem, BillModel
from model.product_model import Product
from model.user_model import User

class TestBillModel:
    @pytest.fixture
    def cashier_user(self):
        """Create a test cashier user"""
        return User("testcashier", "pass123", "cashier")
    
    @pytest.fixture
    def sample_product(self):
        """Create a sample product"""
        return Product("Electronics", "Laptop", 1000.00, 5)
    
    @pytest.fixture
    def bill(self, cashier_user):
        """Create a test bill"""
        return Bill(cashier_user)
    
    @pytest.fixture
    def bill_model(self, tmp_path):
        """Create a test bill model with a temporary bills file"""
        bills_file = tmp_path / "bills.txt"
        bills_file.write_text("Bill 1: 100.00\nBill 2: 200.00\n")
        
        model = BillModel()
        model.bills_file = str(bills_file)
        return model
    
    def test_bill_item_creation(self, sample_product):
        """Test that a bill item is created correctly"""
        item = BillItem(sample_product, 2)
        assert item.product == sample_product
        assert item.quantity == 2
        assert item.subtotal == 2000.00  # 2 * 1000.00
    
    def test_add_item_to_bill(self, bill, sample_product):
        """Test adding an item to the bill"""
        success, _ = bill.add_item(sample_product, 2)
        assert success is True
        assert len(bill.items) == 1
        assert bill.items[0].product == sample_product
        assert bill.items[0].quantity == 2
        assert bill.items[0].subtotal == 2000.00
    
    def test_add_item_exceeding_stock(self, bill, sample_product):
        """Test that adding an item exceeding available stock fails"""
        success, _ = bill.add_item(sample_product, 10)  # Stock is only 5
        assert success is False
        assert len(bill.items) == 0
    
    def test_remove_item_from_bill(self, bill, sample_product):
        """Test removing an item from the bill"""
        bill.add_item(sample_product, 2)
        assert len(bill.items) == 1
        
        success, _ = bill.remove_item(0)
        assert success is True
        assert len(bill.items) == 0
    
    def test_remove_nonexistent_item(self, bill):
        """Test that removing a nonexistent item fails"""
        success, _ = bill.remove_item(0)
        assert success is False
    
    def test_calculate_total(self, bill, sample_product):
        """Test calculating the bill total"""
        bill.add_item(sample_product, 2)
        
        # Add another product
        product2 = Product("Clothing", "T-Shirt", 20.00, 10)
        bill.add_item(product2, 3)
        
        total = bill.calculate_total()
        assert total == 2060.00  # (2 * 1000.00) + (3 * 20.00)
    
    def test_apply_cash_payment(self, bill, sample_product):
        """Test applying cash payment method (no discount)"""
        bill.add_item(sample_product, 2)
        bill.calculate_total()  # Total = 2000.00
        
        final_amount = bill.apply_payment_method("cash")
        assert bill.payment_method == "cash"
        assert bill.discount == 0.0
        assert bill.final_amount == 2000.00
        assert final_amount == 2000.00
    
    def test_apply_card_payment(self, bill, sample_product):
        """Test applying card payment method (10% discount)"""
        bill.add_item(sample_product, 2)
        bill.calculate_total()  # Total = 2000.00
        
        final_amount = bill.apply_payment_method("card")
        assert bill.payment_method == "card"
        assert bill.discount == 200.00  # 10% of 2000.00
        assert bill.final_amount == 1800.00  # 2000.00 - 200.00
        assert final_amount == 1800.00
    
    def test_get_next_bill_number(self, bill_model):
        """Test getting the next bill number"""
        assert bill_model.get_next_bill_number() == 3  # Already have Bill 1 and Bill 2
    
    def test_save_bill(self, bill_model, cashier_user, sample_product, monkeypatch):
        """Test saving a bill to file and updating stock"""
        # Create a bill with items
        bill = Bill(cashier_user)
        bill.add_item(sample_product, 2)
        bill.calculate_total()
        bill.apply_payment_method("cash")
        
        # Mock the ProductModel.update_stock method
        called_with = []
        
        def mock_update_stock(self, category, name, new_stock):
            called_with.append((category, name, new_stock))
            return True, "Stock updated"
        
        # Apply the monkeypatch
        from model.product_model import ProductModel
        monkeypatch.setattr(ProductModel, "update_stock", mock_update_stock)
        
        # Save the bill
        success, _ = bill_model.save_bill(bill)
        
        # Verify the bill was saved
        assert success is True
        
        # Verify the stock was updated
        assert len(called_with) == 1
        assert called_with[0][0] == "Electronics"  # category
        assert called_with[0][1] == "Laptop"  # name
        assert called_with[0][2] == 3  # new stock (5 - 2) 