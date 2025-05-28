# Smart Mart System

A Point of Sale system built with Python and Tkinter, following the MVC architecture pattern.

## Features

### Admin Panel
- Login using admin credentials
- Dashboard with statistics
- Manage cashier accounts (add, update, delete)
- Manage products and categories
- Update product stock levels

### Cashier Panel
- Login using cashier credentials
- Browse products by category
- Add products to cart
- Apply payment methods (Cash or Card with 10% discount)
- Generate bills

## Setup and Installation

### Requirements
- Python 3.8 or higher
- Required packages in `requirements.txt`

### Steps
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Default Credentials

### Admin
- Username: admin
- Password: admin123

### Cashiers
- Username: john, Password: john123
- Username: mary, Password: mary123
- Username: alex, Password: alex123

## Project Structure

```
Smart_Mart_System/
│
├── controller/          # Controllers for business logic
│   ├── admin_controller.py
│   ├── auth_controller.py
│   └── cashier_controller.py
│
├── model/               # Data models and file operations
│   ├── bill_model.py
│   ├── product_model.py
│   └── user_model.py
│
├── view/                # UI components
│   ├── admin_view.py
│   ├── base_view.py
│   ├── cashier_view.py
│   └── login_view.py
│
├── data/                # Data storage files
│   ├── admin.txt
│   ├── bills.txt
│   ├── cashiers.txt
│   └── products.txt
│
├── images/              # Images and assets
│   └── background.png   
│
├── tests/               # Test files
│   ├── test_bill_model.py
│   └── test_user_model.py
│
├── main.py              # Main application entry point
├── requirements.txt     # Dependencies
└── README.md            # This file
```

## Tests

Run tests with pytest:
```
pytest tests/
```

## Build Executable

Build an executable with PyInstaller:
```
pyinstaller --onefile --windowed main.py
```

The executable will be created in the `dist` directory.

## License

This project is available under the MIT License. 