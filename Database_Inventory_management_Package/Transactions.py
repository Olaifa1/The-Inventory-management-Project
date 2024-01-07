# Supply_Transactions.py

import pyodbc
import random
import re       #   Import the Regular Expression module
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

    def get_valid_input(self, input_type, validation_pattern, error_message):
        while True:
            user_input = input(f"Enter the {input_type}: ").strip()
            user_input = user_input.title()  # Convert to Title case

            if not re.match(validation_pattern, user_input):
                print(error_message)
            else:
                return user_input

    def get_valid_supplier_name(self):
        validation_pattern = "^[A-Za-z]+( [A-Za-z]+)*$"
        error_message = "Supplier name must contain only English alphabets in sentence case."
        return self.get_valid_input("SupplierName", validation_pattern, error_message)

    def get_valid_product_name(self):
        validation_pattern = "^[A-Za-z]+( [A-Za-z]+)*$"
        error_message = "Product name must contain only English alphabets."
        return self.get_valid_input("ProductName", validation_pattern, error_message)


            
    # Define a static method to check if ContactInfo is a non-empty string
    @staticmethod
    def is_valid_contact_info(contact_info):
        return contact_info is not None and len(contact_info.strip()) > 0
    
    def generate_unique_transaction_id(self, existing_transaction_ids):
        while True:
            transaction_id = random.randint(10000, 99999)
            if transaction_id not in existing_transaction_ids:
                return transaction_id

    def display_transactions_table(self):
        self.cursor.execute('SELECT * FROM Supply_Transactions')
        rows = self.cursor.fetchall()

        if rows:
                print("Supply Transactions Table:")
                print("TransactionID | ProductID | SupplierID | ProductName  | SupplierName             | TransactionType | Quantity | TransactionDate")
                print("-" * 130)
                for row in rows:
                    print(f"{row.TransactionID:13} | {row.ProductID:9} | {row.SupplierID:10} | {row.ProductName:12} | {row.SupplierName:24} | {row.TransactionType:15} | {row.Quantity:8} | {row.TransactionDate}")
        else:
            print("No records found in the Supply Transactions table.")
               

    def add_transaction(self, updated_product_list, updated_supplier_list):
        while True:
            try:

                existing_transaction_ids = [row.TransactionID for row in self.cursor.execute("SELECT TransactionID FROM Supply_Transactions")]
                
                # Generate unique TransactionID
                transaction_id = self.generate_unique_transaction_id(existing_transaction_ids)

                product_name = self.get_valid_product_name()
                
                #   while product name is in updated_product_list, match the corressponding product_id to the product name.
                while product_name in updated_product_list.values():
                    product_id = [k for k, v in updated_product_list.items() if v == product_name][0]
                    

                    quantity = input("Enter the Quantity (greater than or equals to 0): ")

                    while not re.match("^[0-9]+$", quantity):
                        print("Invalid Quantity. Please enter a valid integer greater than or equals to 0.")
                        quantity = input("Enter the new quantity (greater than or equals to 0): ")

                    quantity = int(quantity)

                    supplier_name = self.get_valid_supplier_name()

                    contact_info = input("Enter the Supplier's ContactInfo: ")

                    while not self.is_valid_contact_info(contact_info):
                        print("Invalid ContactInfo. Please enter a non-empty string.")
                        contact_info = input("Enter the Supplier's ContactInfo: ")

                    if supplier_name in updated_supplier_list.values():
                        supplier_id = [k for k, v in updated_supplier_list.items() if v == supplier_name][0]

                    elif supplier_name not in updated_supplier_list.values():
                        # Execute a SQL query to get the maximum SupplierID from the Suppliers table
                        self.cursor.execute("SELECT MAX(SupplierID) FROM Suppliers")
                        current_max_id = self.cursor.fetchone()[0]
                        supplier_id = current_max_id + 1 if current_max_id is not None else 1

                        self.cursor.execute(
                        f"INSERT INTO Suppliers (SupplierID, SupplierName, ContactInfo) VALUES ({supplier_id}, '{supplier_name}', '{contact_info}')"
                        )
                        self.conn.commit()

                        updated_supplier_list = self.update_supplier_list(updated_supplier_list)



                    # Assign "In" to TransactionType
                    transaction_type = "In"
                    transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    self.cursor.execute(
                        f"INSERT INTO Supply_Transactions (TransactionID, ProductID, SupplierID, ProductName, SupplierName, TransactionType, Quantity, TransactionDate) VALUES "
                        f"({transaction_id}, {product_id}, {supplier_id}, '{product_name}', '{supplier_name}', '{transaction_type}', {quantity}, '{transaction_date}')"
                    )
                    self.conn.commit()

                    break

                

                #   while product name is not in updated_product_list, create a new product_id and match it to the product name.
                while product_name not in updated_product_list.values():

                    self.cursor.execute("SELECT MAX(ProductID) FROM Products")
                    current_max_id = self.cursor.fetchone()[0]
                    product_id = current_max_id + 1 if current_max_id is not None else 1
                    #old_quantity = [row.StockQuantity for row in self.cursor.execute(f"SELECT StockQuantity FROM Products WHERE ProductID = {product_id}")]
                    #old_quantity = self.cursor.execute(f"SELECT StockQuantity FROM Products WHERE ProductID = {product_id}")

                    quantity = input("Enter the Quantity (greater than or equals to 0): ")

                    while not re.match("^[0-9]+$", quantity):
                        print("Invalid Quantity. Please enter a valid integer greater than or equals to 0.")
                        quantity = input("Enter the new quantity (greater than or equals to 0): ")

                    quantity = int(quantity)

                    self.cursor.execute(
                        f"INSERT INTO Products (ProductID, ProductName, StockQuantity) VALUES ({product_id}, '{product_name}', '{quantity}')"
                    )
                    self.conn.commit()

                    updated_product_list = self.update_product_list(updated_product_list)

                    supplier_name = self.get_valid_supplier_name()


                    contact_info = input("Enter the Supplier's ContactInfo: ")

                    while not self.is_valid_contact_info(contact_info):
                        print("Invalid ContactInfo. Please enter a non-empty string.")
                        contact_info = input("Enter the Supplier's ContactInfo: ")

                    if supplier_name in updated_supplier_list.values():
                        supplier_id = [k for k, v in updated_supplier_list.items() if v == supplier_name][0]

                    elif supplier_name not in updated_supplier_list.values():
                        # Execute a SQL query to get the maximum SupplierID from the Suppliers table
                        self.cursor.execute("SELECT MAX(SupplierID) FROM Suppliers")
                        current_max_id = self.cursor.fetchone()[0]
                        supplier_id = current_max_id + 1 if current_max_id is not None else 1

                        self.cursor.execute(
                            f"INSERT INTO Suppliers (SupplierID, SupplierName, ContactInfo) VALUES ({supplier_id}, '{supplier_name}', '{contact_info}')"
                        )
                        self.conn.commit()

                        updated_supplier_list = self.update_supplier_list(updated_supplier_list)



                    # Assign "In" to TransactionType
                    transaction_type = "In"
                    transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    self.cursor.execute(
                        f"INSERT INTO Supply_Transactions (TransactionID, ProductID, SupplierID, ProductName, SupplierName, TransactionType, Quantity, TransactionDate) VALUES "
                        f"({transaction_id}, {product_id}, {supplier_id}, '{product_name}', '{supplier_name}', '{transaction_type}', {quantity}, '{transaction_date}')"
                    )
                    self.conn.commit()

                    break

                
                
                break

            except ValueError as e:
                print(f"Error: {e}")


    def delete_transaction(self, updated_product_list):
        while True:
            try:
                transaction_id = input("Enter the TransactionID to delete: ").strip()

                if not re.match("^[0-9]+$", transaction_id):
                    print("Invalid TransactionID. Please enter a valid integer.")
                    continue

                transaction_id = int(transaction_id)

                # Check if the transaction_id exists in the Supply_Transactions table
                if transaction_id not in [row.TransactionID for row in self.cursor.execute("SELECT TransactionID FROM Supply_Transactions")]:
                    print("Invalid TransactionID. The specified transaction does not exist.")
                    continue

                # Fetch information from the specified transaction_id
                transaction_info = self.cursor.execute(
                    f"SELECT * FROM Supply_Transactions WHERE TransactionID = {transaction_id}"
                ).fetchone()

                # Delete the row from Supply_Transactions
                self.cursor.execute(f"DELETE FROM Supply_Transactions WHERE TransactionID = {transaction_id}")
                self.conn.commit()

                # Update the updated_product_list, updated_supplier_list, Products table, and Suppliers table
                #updated_product_list = self.update_product_list(updated_product_list)
                #updated_supplier_list = self.update_supplier_list(updated_supplier_list)

                # ... (update Products and Suppliers tables as needed)

                print(f"Transaction with TransactionID {transaction_id} has been deleted successfully.")
                break

            except ValueError as e:
                print(f"Error: {e}")

                
    def run_program(self):
        while True:
            self.display_transactions_table()


            product_list = self.create_empty_product_list()
            updated_product_list = self.update_product_list(product_list)

            supplier_list = self.create_empty_supplier_list()
            updated_supplier_list = self.update_supplier_list(supplier_list)

            print("\nOptions:")
            print("1. Add a Transaction")
            print("2. Delete a Transaction")
            print("3. Terminate the program")

            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == '1':
                self.add_transaction(updated_product_list, updated_supplier_list)
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


