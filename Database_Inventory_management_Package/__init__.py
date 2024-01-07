# __init__.py






# Transactions.py

import pyodbc
import random
from datetime import datetime

class InventoryManager:
    def __init__(self, connection_string):
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

    def create_empty_product_list(self):
        product_list = {}
        return product_list

    def update_product_list(self, product_list):
        self.cursor.execute('SELECT ProductID, ProductName FROM Products')
        rows = self.cursor.fetchall()

        for row in rows:
            product_list[row.ProductID] = row.ProductName

        return product_list

    def create_empty_supplier_list(self):
        supplier_list = {}
        return supplier_list

    def update_supplier_list(self, supplier_list):
        self.cursor.execute('SELECT SupplierID, SupplierName FROM Suppliers')
        rows = self.cursor.fetchall()

        for row in rows:
            supplier_list[row.SupplierID] = row.SupplierName

        return supplier_list

    @staticmethod
    def is_valid_stock_quantity(quantity):
        try:
            stock_quantity = int(quantity)
            return stock_quantity >= 0  # Compare stock_quantity (integer) with 0
        except ValueError:
            return False


    def generate_unique_transaction_id(self, existing_transaction_ids):
        while True:
            transaction_id = random.randint(10000, 99999)
            if transaction_id not in existing_transaction_ids:
                return transaction_id

    def display_transactions_table(self):
        self.cursor.execute('SELECT * FROM Transactions')
        rows = self.cursor.fetchall()

        if rows:
                print("Transactions Table:")
                print("TransactionID | ProductID | SupplierID | ProductName  | SupplierName             | TransactionType | Quantity | TransactionDate")
                print("-" * 130)
                for row in rows:
                    print(f"{row.TransactionID:13} | {row.ProductID:9} | {row.SupplierID:10} | {row.ProductName:12} | {row.SupplierName:24} | {row.TransactionType:15} | {row.Quantity:8} | {row.TransactionDate}")
        else:
            print("No records found in the Transactions table.")
               

    def add_transaction(self, updated_product_list, updated_supplier_list, existing_transaction_ids):
        while True:
            try:
                # Initialize quantity outside the if block
                quantity = None

                # Generate unique TransactionID
                transaction_id = self.generate_unique_transaction_id(existing_transaction_ids)

                product_name = input("Enter the ProductName: ")

                if not product_name.strip():
                    raise ValueError("Product name cannot be empty or contain only whitespace characters.")

                if product_name in updated_product_list.values():
                    product_id = [k for k, v in updated_product_list.items() if v == product_name][0]
                else:
                    self.cursor.execute("SELECT MAX(ProductID) FROM Products")
                    current_max_id = self.cursor.fetchone()[0]
                    product_id = current_max_id + 1 if current_max_id is not None else 1

                    # Move this block outside of the else block
                    quantity = input("Enter the new Quantity (greater than or equals to 0): ")

                    while not self.is_valid_stock_quantity(quantity):
                        print("Invalid Quantity. Please enter a valid integer greater than or equals to 0.")
                        quantity = input("Enter the new Quantity (greater than or equals to 0): ")

                    # Define new_stock_quantity here
                    new_stock_quantity = int(quantity)

                    self.cursor.execute(
                        f"INSERT INTO Products (ProductID, ProductName, StockQuantity) VALUES ({product_id}, '{product_name}', {new_stock_quantity})"
                    )
                    self.conn.commit()

                    updated_product_list = self.update_product_list(updated_product_list)

                    supplier_name = input("Enter the SupplierName: ")

                if not supplier_name.strip():
                    raise ValueError("Supplier name cannot be empty or contain only whitespace characters.")

                if supplier_name in updated_supplier_list.values():
                    supplier_id = [k for k, v in updated_supplier_list.items() if v == supplier_name][0]
                else:
                    self.cursor.execute("SELECT MAX(SupplierID) FROM Suppliers")
                    current_max_id = self.cursor.fetchone()[0]
                    supplier_id = current_max_id + 1 if current_max_id is not None else 1

                    contact_info = input("Enter the ContactInfo: ")

                    self.cursor.execute(
                        f"INSERT INTO Suppliers (SupplierID, SupplierName, ContactInfo) VALUES ({supplier_id}, '{supplier_name}', '{contact_info}')"
                    )
                    self.conn.commit()

                    updated_supplier_list = self.update_supplier_list(updated_supplier_list)

                transaction_type = input("Enter TransactionType 'In' or 'Out': ")

                if product_name and transaction_type == 'Out':
                    quantity = None
                else:
                    # quantity = new_stock_quantity
                    while not quantity.isdigit():
                        print("Invalid Quantity. Please enter a valid integer.")
                        quantity = input("Enter Quantity: ")

                    quantity = int(quantity)

                    if product_name and transaction_type == 'In':
                        old_quantity = [row.StockQuantity for row in self.cursor.execute(f"SELECT StockQuantity FROM Products WHERE ProductID = {product_id}")]
                        new_stock_quantity = old_quantity[0] + quantity

                        self.cursor.execute(
                            f"UPDATE Products SET StockQuantity = {new_stock_quantity} WHERE ProductID = {product_id}"
                        )
                        self.conn.commit()

                        updated_product_list = self.update_product_list(updated_product_list)

                    elif product_name and transaction_type == 'Out':
                        old_quantity = [row.StockQuantity for row in self.cursor.execute(f"SELECT StockQuantity FROM Products WHERE ProductID = {product_id}")]
                        if quantity <= old_quantity[0]:
                            new_stock_quantity = old_quantity[0] - quantity

                            self.cursor.execute(
                                f"UPDATE Products SET StockQuantity = {new_stock_quantity} WHERE ProductID = {product_id}"
                            )
                            self.conn.commit()

                            updated_product_list = self.update_product_list(updated_product_list)

                        else:
                            print("Enter Quantity less than or equals to old quantity.")
                            continue

                transaction_date = datetime.now().strftime('%Y-%m-%d')

                self.cursor.execute(
                    f"INSERT INTO Transactions (TransactionID, ProductID, SupplierID, ProductName, SupplierName, TransactionType, Quantity, TransactionDate) VALUES "
                    f"({transaction_id}, {product_id}, {supplier_id}, '{product_name}', '{supplier_name}', '{transaction_type}', {quantity}, '{transaction_date}')"
                )
                self.conn.commit()

                break

            except ValueError as e:
                print(f"Error: {e}")



    def run_program(self):
        while True:
            self.display_transactions_table()

            # Create and update product list
            product_list = self.create_empty_product_list()
            updated_product_list = self.update_product_list(product_list)

            # Create and update supplier list
            supplier_list = self.create_empty_supplier_list()
            updated_supplier_list = self.update_supplier_list(supplier_list)

            print("\nOptions:")
            print("1. Add a Transaction")
            print("2. Delete a Transaction")
            print("3. Terminate the program")

            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == '1':
                # Retrieve existing transaction IDs before calling add_transaction
                existing_transaction_ids = [row.TransactionID for row in self.cursor.execute("SELECT TransactionID FROM Transactions")]
                # Pass the updated lists and existing_transaction_ids to the add_transaction method
                self.add_transaction(updated_product_list, updated_supplier_list, existing_transaction_ids)
            elif choice == '2':
                self.delete_transaction(updated_product_list)
            elif choice == '3':
                self.display_transactions_table()
                self.conn.close()
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")






# Define the connection string with details to connect to the SQL Server
connection_string = 'DRIVER={SQL Server};SERVER=DESKTOP-SH1HJJ8\\SQLEXPRESS;DATABASE=InventoryManagement;Trusted_Connection=yes;'
# Specify the connection string with details to connect to the SQL Server database

# Create an instance of the InventoryManager class
inventory_manager = InventoryManager(connection_string)

# Run the program using the instance
inventory_manager.run_program()
# Create an instance of the InventoryManager class and execute the main program loop

