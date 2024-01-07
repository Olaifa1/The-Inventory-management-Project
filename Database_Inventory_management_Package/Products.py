#Products.py

import pyodbc
# Import the pyodbc module for working with SQL Server databases

import re   #   Import the Regular Expression module

class InventoryManager:
    # Define an Init method to initialize the class with a connection to the database and a cursor for executing queries
    def __init__(self, connection_string):
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()
        
    # Define a method to create an empty dictionary for storing ProductIDs and ProductNames
    def create_empty_product_list(self):
        product_list = {}
        return product_list
        
    # Define a method to update the product_list dictionary with the latest data from the Products table
    def update_product_list(self, product_list):
        self.cursor.execute('SELECT ProductID, ProductName FROM Products')
        rows = self.cursor.fetchall()

        for row in rows:
            product_list[row.ProductID] = row.ProductName

        return product_list

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
        

    # Define a method to execute a query to fetch all data from the Products table and display it in a formatted table
    def display_products_table(self):
        self.cursor.execute('SELECT * FROM Products')
        rows = self.cursor.fetchall()

        if rows:
            print("Products Table:")
            print("ProductID | ProductName  | StockQuantity")
            print("-" * 40)
            for row in rows:
                print(f"{row.ProductID:9} | {row.ProductName:12} | {row.StockQuantity:13}")
        else:
            print("No records found in the Products table.")
        


    # Define a method to add a new unique ProductName and a matching unique ProductID to the Products table
    def add_new_product(self, updated_product_list):
        while True:
            try:
                new_product_name = self.get_valid_product_name()

                if new_product_name in updated_product_list.values():
                    print(f"{new_product_name} is an already existing ProductName in the table Products.")
                    continue

                self.cursor.execute("SELECT MAX(ProductID) FROM Products")
                current_max_id = self.cursor.fetchone()[0]
                new_product_id = current_max_id + 1 if current_max_id is not None else 1

                new_stock_quantity = input("Enter the new StockQuantity (greater than or equals to 0): ")

                while not re.match("^[0-9]+$", new_stock_quantity):
                    print("Invalid StockQuantity. Please enter a valid integer greater than or equals to 0.")
                    new_stock_quantity = input("Enter the new StockQuantity (greater than or equals to 0): ")

                new_stock_quantity = int(new_stock_quantity)

                self.cursor.execute(
                    f"INSERT INTO Products (ProductID, ProductName, StockQuantity) VALUES ({new_product_id}, '{new_product_name}', {new_stock_quantity})"
                )
                self.conn.commit()

                updated_product_list = self.update_product_list(updated_product_list)
                break

            except ValueError as e:
                print(f"Error: {e}")



    # Define a method to change the name of an old ProductName in the Products table
    def change_product_name(self, updated_product_list):
        while True:
            try:
                old_product_name = input("Enter the name of the old ProductName you want to change: ")

                old_product_name = old_product_name.title() # convert old_product_name to Title case

                if old_product_name not in updated_product_list.values():
                    print(f"{old_product_name} is not an existing ProductName in the table Products.")
                    continue

                while True:
                    new_product_name = self.get_valid_product_name()

                    if new_product_name in updated_product_list.values():
                        print(f"{new_product_name} is an existing ProductName in the table Products.")
                        continue

                    old_product_id = [k for k, v in updated_product_list.items() if v == old_product_name][0]

                    while True:
                        new_stock_quantity = input("Enter the new StockQuantity (greater than or equals to 0): ")

                        if not re.match("^[0-9]+$", new_stock_quantity):
                            print("Invalid StockQuantity. Please enter a valid integer greater than or equals to 0.")
                            continue

                        new_stock_quantity = int(new_stock_quantity)

                        self.cursor.execute(
                            f"UPDATE Products SET ProductName = '{new_product_name}', StockQuantity = {new_stock_quantity} WHERE ProductID = {old_product_id}"
                        )
                        self.conn.commit()

                        updated_product_list = self.update_product_list(updated_product_list)
                        break

                    break

                break

            except ValueError as e:
                print(f"Error: {e}")


    # Define a method to change only the StockQuantity of an old ProductName in the Products table
    def change_stock_quantity(self, updated_product_list):
        while True:
            old_product_name = input("Enter the name of the product you want to update: ")

            old_product_name = old_product_name.title() # convert old_product_name to Title case

            if old_product_name not in updated_product_list.values():
                print(f"{old_product_name} is not an existing ProductName in the table Products.")
                continue

            old_product_id = [k for k, v in updated_product_list.items() if v == old_product_name][0]

            new_stock_quantity = input("Enter the new StockQuantity (greater than or equals to 0): ")

            while not re.match("^[0-9]+$", new_stock_quantity):
                print("Invalid StockQuantity. Please enter a valid integer greater than or equals to 0.")
                new_stock_quantity = input("Enter the new StockQuantity (greater than or equals to 0): ")

            new_stock_quantity = int(new_stock_quantity)

            self.cursor.execute(
                f"UPDATE Products SET StockQuantity = {new_stock_quantity} WHERE ProductID = {old_product_id}"
            )
            self.conn.commit()

            updated_product_list = self.update_product_list(updated_product_list)
            break
        
    # Define a method to delete a specified old ProductName and its corresponding ProductID and StockQuantity from the Products table
    def delete_product(self, updated_product_list):
        while True:
            old_product_name = input("Enter the name of the old ProductName you want to delete: ")

            old_product_name = old_product_name.title() # convert old_product_name to Title case

            if old_product_name not in updated_product_list.values():
                print(f"{old_product_name} is not an existing ProductName in the table Products.")
                continue

            old_product_id = [k for k, v in updated_product_list.items() if v == old_product_name][0]

            self.cursor.execute(f"DELETE FROM Products WHERE ProductID = {old_product_id}")
            self.conn.commit()

            updated_product_list = self.update_product_list(updated_product_list)
            break
        
        
    # Define a method to run the main program loop, allowing the user to interact with the inventory management system
    def run_program(self):
        while True:
            self.display_products_table()

            product_list = self.create_empty_product_list()
            updated_product_list = self.update_product_list(product_list)

            print("\nOptions:")
            print("1. Add a new ProductName")
            print("2. Change the name of an old ProductName")
            print("3. Change only the StockQuantity of an old ProductName")
            print("4. DELETE an old ProductName and its entire row")
            print("5. Terminate the program")

            choice = input("Enter your choice (1, 2, 3, 4, or 5): ")

            if choice == '1':
                self.add_new_product(updated_product_list)
            elif choice == '2':
                self.change_product_name(updated_product_list)
            elif choice == '3':
                self.change_stock_quantity(updated_product_list)
            elif choice == '4':
                self.delete_product(updated_product_list)
            elif choice == '5':
                self.display_products_table()
                self.conn.close()
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
        

# Define the connection string with details to connect to the SQL Server
connection_string = 'DRIVER={SQL Server};SERVER=DESKTOP-SH1HJJ8\\SQLEXPRESS;DATABASE=InventoryManagement;Trusted_Connection=yes;'
# Specify the connection string with details to connect to the SQL Server database

# Create an instance of the InventoryManager class
inventory_manager = InventoryManager(connection_string)

# Run the program using the instance
inventory_manager.run_program()
# Create an instance of the InventoryManager class and execute the main program loop





































