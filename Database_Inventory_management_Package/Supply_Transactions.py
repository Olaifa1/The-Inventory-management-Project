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


            
    # Define a method to check if Address is a non-empty string
    def get_address(self):
        while True:
            address_input = input("Enter the address: ").strip()

            if not address_input:
                print("Invalid address. Please enter a non-empty string.")
            else:
                return address_input

    def get_email(self):
        validation_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        while True:
            email_input = input("Enter your email: ").strip()

            if not re.match(validation_pattern, email_input):
                print("Invalid email. Please enter a valid email address.")
            else:
                return email_input

    
    def get_phone_number(self):
        phone_pattern = re.compile(r'^\+\d{1,4}\d{7,14}$')

        while True:
            phone_input = input("Enter your phone number (including country code): ").strip()

            if not phone_pattern.match(phone_input):
                print("Invalid input. Please enter a valid phone number with the country code (e.g., +123456789012).")
            else:
                return phone_input


    
    def generate_unique_transaction_id(self, existing_transaction_ids):
        while True:
            transaction_id = random.randint(10000, 99999)
            if transaction_id not in existing_transaction_ids:
                return transaction_id

    def get_valid_quantity(self):
        while True:
            new_stock_quantity = input("Enter the Quantity (greater than 0): ")

            if re.match("^[0-9]+$", new_stock_quantity):
                new_stock_quantity = int(new_stock_quantity)
                if new_stock_quantity > 0:
                    return new_stock_quantity
                else:
                    print("Invalid StockQuantity. Please enter a non-negative integer.")
            else:
                print("Invalid StockQuantity. Please enter a valid integer greater than 0.")

    def get_valid_cost_price(self):
        while True:
            cost_price = input("Enter the Unit cost price of the Product (greater than 0): ")

            if re.match("^[0-9]+$", cost_price):
                cost_price = int(cost_price)
                if cost_price > 0:
                    return cost_price
                else:
                    print("Invalid cost price. Please enter a non-negative integer.")
            else:
                print("Invalid cost price. Please enter a valid integer greater than 0.")

    
    def display_transactions_table(self):
        self.cursor.execute('SELECT * FROM Supply_Transactions')
        rows = self.cursor.fetchall()

        if rows:
            print("Supply Transactions Table:")
            print("TransactionID | ProductID | SupplierID | ProductName  | SupplierName             | Address | Email | PhoneNumber | Quantity | Cost_Price | TransactionDate")
            print("-" * 130)
            for row in rows:
                print(f"{row.TransactionID:13} | {row.ProductID:9} | {row.SupplierID:10} | {row.ProductName:12} | {row.SupplierName:24} | {str(row.Address):15} | {str(row.Email):15} | {str(row.PhoneNumber):15} | {row.Quantity:8} | {row.Cost_Price:8} | {row.TransactionDate}")
        else:
            print("No records found in the Supply Transactions table.")


               

    def add_transaction(self, updated_product_list, updated_supplier_list):
        while True:
            try:

                existing_transaction_ids = [row.TransactionID for row in self.cursor.execute("SELECT TransactionID FROM Supply_Transactions")]
                
                # Generate unique TransactionID
                transaction_id = self.generate_unique_transaction_id(existing_transaction_ids)

                product_name = self.get_valid_product_name()
                
                #   while product name is in updated_product_list, match the corresponding product_id to the product name.
                while product_name in updated_product_list.values():
                    product_id = [k for k, v in updated_product_list.items() if v == product_name][0]
                    

                    quantity = self.get_valid_quantity()

                    updated_product_list = self.update_product_list(updated_product_list)
                    
                    cost_price = self.get_valid_cost_price()

                    supplier_name = self.get_valid_supplier_name()

                    address = self.get_address()
                    email = self.get_email()
                    phone = self.get_phone_number()

                    if supplier_name in updated_supplier_list.values():
                        supplier_id = [k for k, v in updated_supplier_list.items() if v == supplier_name][0]

                    elif supplier_name not in updated_supplier_list.values():
                        # Execute a SQL query to get the maximum SupplierID from the Suppliers table
                        self.cursor.execute("SELECT MAX(SupplierID) FROM Suppliers")
                        current_max_id = self.cursor.fetchone()[0]
                        supplier_id = current_max_id + 1 if current_max_id is not None else 1

                        self.cursor.execute(
                            "INSERT INTO Suppliers (SupplierID, SupplierName, Address, Email, PhoneNumber) "
                            "VALUES (?,?,?,?,?)",
                            supplier_id, supplier_name, address, email, phone
                        )
                        self.conn.commit()

                        updated_supplier_list = self.update_supplier_list(updated_supplier_list)

                    

                    transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    self.cursor.execute(
                        "INSERT INTO Supply_Transactions (TransactionID, ProductID, SupplierID, ProductName, SupplierName, Address, Email, PhoneNumber, Quantity, Cost_price, TransactionDate) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        transaction_id, product_id, supplier_id, product_name, supplier_name, address, email, phone, quantity, cost_price, transaction_date
                    )
                    self.conn.commit()

                    break

                

                #   while product name is not in updated_product_list, create a new product_id and match it to the product name.
                while product_name not in updated_product_list.values():

                    self.cursor.execute("SELECT MAX(ProductID) FROM Products")
                    current_max_id = self.cursor.fetchone()[0]
                    product_id = current_max_id + 1 if current_max_id is not None else 1
                    
                    quantity = self.get_valid_quantity()
                    cost_price = self.get_valid_cost_price()

                    self.cursor.execute(
                        "INSERT INTO Products (ProductID, ProductName, StockQuantity) "
                        "VALUES (?, ?, ?)",
                        product_id, product_name, quantity
                    )
                    self.conn.commit()

                    updated_product_list = self.update_product_list(updated_product_list)

                    supplier_name = self.get_valid_supplier_name()


                    address = self.get_address()
                    email = self.get_email()
                    phone = self.get_phone_number()

                    if supplier_name in updated_supplier_list.values():
                        supplier_id = [k for k, v in updated_supplier_list.items() if v == supplier_name][0]

                    elif supplier_name not in updated_supplier_list.values():
                        # Execute a SQL query to get the maximum SupplierID from the Suppliers table
                        self.cursor.execute("SELECT MAX(SupplierID) FROM Suppliers")
                        current_max_id = self.cursor.fetchone()[0]
                        supplier_id = current_max_id + 1 if current_max_id is not None else 1

                        self.cursor.execute(
                            "INSERT INTO Suppliers (SupplierID, SupplierName, Address, Email, PhoneNumber) "
                            "VALUES (?,?,?,?,?)",
                            supplier_id, supplier_name, address, email, phone
                        )
                        self.conn.commit()

                        updated_supplier_list = self.update_supplier_list(updated_supplier_list)



                    
                    transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    self.cursor.execute(
                        "INSERT INTO Supply_Transactions (TransactionID, ProductID, SupplierID, ProductName, SupplierName, Address, Email, PhoneNumber, Quantity, Cost_price, TransactionDate) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        transaction_id, product_id, supplier_id, product_name, supplier_name, address, email, phone, quantity, cost_price, transaction_date
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
















































# Supply_Transactions.py

import pyodbc
import random
import re
from datetime import datetime

class Supply_Transactions:
    def __init__(self, connection_string):
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

    def generate_unique_transaction_id(self, existing_transaction_ids):
        while True:
            transaction_id = random.randint(10000, 99999)
            if transaction_id not in existing_transaction_ids:
                return transaction_id

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
    
    def get_valid_product_name(self):
        validation_pattern = "^[A-Za-z]+( [A-Za-z]+)*$"
        error_message = "Product name must contain only English alphabets."
        return self.get_valid_input("ProductName", validation_pattern, error_message)


    def get_valid_supplier_name(self):
        validation_pattern = "^[A-Za-z]+( [A-Za-z]+)*$"
        error_message = "supplier name must contain only English alphabets in sentence case."
        return self.get_valid_input("SupplierName", validation_pattern, error_message)

    # Define a method to check if Address is a non-empty string
    def get_address(self):
        while True:
            address_input = input("Enter the address: ").strip()

            if not address_input:
                print("Invalid address. Please enter a non-empty string.")
            else:
                return address_input
    
    def get_email(self):
        validation_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        while True:
            email_input = input("Enter your email: ").strip()

            if not re.match(validation_pattern, email_input):
                print("Invalid email. Please enter a valid email address.")
            else:
                return email_input

    
    def get_phone_number(self):
        phone_pattern = re.compile(r'^\+\d{1,4}\d{7,14}$')

        while True:
            phone_input = input("Enter your phone number (including country code): ").strip()

            if not phone_pattern.match(phone_input):
                print("Invalid input. Please enter a valid phone number with the country code (e.g., +123456789012).")
                continue

            # Remove the leading '+' and convert the remaining digits to a bigint
            phone_number_as_bigint = int(phone_input[1:])

            return phone_number_as_bigint

    def get_valid_quantity(self):
        while True:
            new_stock_quantity = input("Enter the Quantity (greater than 0): ")

            if re.match("^[0-9]+$", new_stock_quantity):
                new_stock_quantity = int(new_stock_quantity)
                if new_stock_quantity > 0:
                    return new_stock_quantity
                else:
                    print("Invalid StockQuantity. Please enter a non-negative integer.")
            else:
                print("Invalid StockQuantity. Please enter a valid integer greater than 0.")

    def get_valid_cost_price(self):
        while True:
            cost_price = input("Enter the Unit cost price of the Product (greater than 0): ")

            if re.match("^[0-9]+$", cost_price):
                cost_price = int(cost_price)
                if cost_price > 0:
                    return cost_price
                else:
                    print("Invalid cost price. Please enter a non-negative integer.")
            else:
                print("Invalid cost price. Please enter a valid integer greater than 0.")
    
    

    def display_supply_transactions_table(self):
        self.cursor.execute('SELECT * FROM Supply_Transactions')
        rows = self.cursor.fetchall()

        if rows:
                print("Supply Transactions Table:")
                print("TransactionID | ProductID | SupplierID | ProductName  | SupplierName             | Address | Email                 | PhoneNumber |  Quantity | Cost_Price | TransactionDate")
                print("-" * 160)
                for row in rows:
                    print(f"{row.TransactionID:13} | {row.ProductID:9} | {row.SupplierID:10} | {row.ProductName:12} | {row.SupplierName:24} | {row.Address:12} | {row.Email:18} | {row.PhoneNumber:12} |  {row.Quantity:8} | {row.Cost_Price:12} | {row.TransactionDate}")
        else:
            print("No records found in the supply Transactions table.")


    def add_transaction(self, updated_product_list, updated_supplier_list):
        while True:
            try:
                existing_transaction_ids = [row.TransactionID for row in self.cursor.execute("SELECT TransactionID FROM Supply_Transactions")]

                # Generate unique TransactionID
                transaction_id = self.generate_unique_transaction_id(existing_transaction_ids)

                product_name = self.get_valid_product_name()

                while product_name in updated_product_list.values():
                    product_id = [k for k, v in updated_product_list.items() if v == product_name][0]

                    quantity = self.get_valid_quantity()
                    cost_price = self.get_valid_cost_price()

                    supplier_name = self.get_valid_supplier_name()

                    address = self.get_address()
                    email = self.get_email()
                    phone = self.get_phone_number()

                    if supplier_name in updated_supplier_list.values():
                        supplier_id = [k for k, v in updated_supplier_list.items() if v == supplier_name][0]
                    else:
                        supplier_id = self.get_or_insert_supplier_id(supplier_name, address, email, phone)
                        updated_supplier_list = self.update_supplier_list(updated_supplier_list)

                    transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    self.cursor.execute(
                        "INSERT INTO Supply_Transactions (TransactionID, ProductID, SupplierID, ProductName, SupplierName, Address, Email, PhoneNumber, Quantity, Cost_Price, TransactionDate) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        transaction_id, product_id, supplier_id, product_name, supplier_name, address, email, phone, quantity, cost_price, transaction_date
                    )
                    self.conn.commit()

                    break

                while product_name not in updated_product_list.values():
                    product_id = self.get_or_insert_product_id(product_name)

                    quantity = self.get_valid_quantity()
                    cost_price = self.get_valid_cost_price()

                    supplier_name = self.get_valid_supplier_name()

                
                    address = self.get_address()
                    email = self.get_email()
                    phone = self.get_phone_number()

                    if supplier_name in updated_supplier_list.values():
                        supplier_id = [k for k, v in updated_supplier_list.items() if v == supplier_name][0]
                    else:
                        supplier_id = self.get_or_insert_supplier_id(supplier_name, address, email, phone)
                        updated_supplier_list = self.update_supplier_list(updated_supplier_list)

                    transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    self.cursor.execute(
                        "INSERT INTO Supply_Transactions (TransactionID, ProductID, SupplierID, ProductName, SupplierName, Address, Email, PhoneNumber, Quantity, Cost_Price, TransactionDate) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        transaction_id, product_id, supplier_id, product_name, supplier_name, address, email, phone, quantity, cost_price, transaction_date
                    )
                    self.conn.commit()

                    break

                break

            except ValueError as e:
                print(f"Error: {e}")

    def get_or_insert_supplier_id(self, supplier_name, address, email, phone):
        self.cursor.execute(
            "INSERT INTO Suppliers (SupplierName, Address, Email, PhoneNumber) "
            "VALUES (?, ?, ?, ?)",
            supplier_name, address, email, phone
        )
        self.conn.commit()

        # Retrieve the newly inserted supplier_id
        self.cursor.execute("SELECT MAX(SupplierID) FROM Suppliers")
        return self.cursor.fetchone()[0]

    def get_or_insert_product_id(self, product_name):
        self.cursor.execute(
            "INSERT INTO Products (ProductName) VALUES (?)",
            product_name
        )
        self.conn.commit()

        # Retrieve the newly inserted product_id
        self.cursor.execute("SELECT MAX(ProductID) FROM Products")
        return self.cursor.fetchone()[0]


    
    def run_program(self):
        while True:
            self.display_supply_transactions_table()

            product_list = self.create_empty_product_list()
            updated_product_list = self.update_product_list(product_list)

            supplier_list = self.create_empty_supplier_list()
            updated_supplier_list = self.update_supplier_list(supplier_list)

            print("\nOptions:")
            print("1. Add a Supply Transaction")
            print("2. Delete a supply Transaction")
            print("3. Terminate the program")

            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == '1':
                self.add_transaction(updated_product_list, updated_supplier_list)
            elif choice == '2':
                self.delete_transaction(updated_product_list)
            elif choice == '3':
                self.display_supply_transactions_table()
                self.conn.close()
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

# The following line creates an instance of the Supply_Transactions class and executes the main program loop
if __name__ == "__main__":
    # Define the connection string with details to connect to the SQL Server
    connection_string = 'DRIVER={SQL Server};SERVER=DESKTOP-SH1HJJ8\\SQLEXPRESS;DATABASE=InventoryManagement;Trusted_Connection=yes;'
    
    # Create an instance of the Supply_Transactions class
    supply_transactions = Supply_Transactions(connection_string)
    
    # Run the program using the instance
    supply_transactions.run_program()





































































