#Suppliers.py

# Import the pyodbc module for working with SQL Server databases
import pyodbc



# Define the InventoryManager class
class InventoryManager:
    # Constructor: Initialize the class with a connection to the database and a cursor for executing queries
    def __init__(self, connection_string):
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

    # Define a method to create an empty dictionary for storing SupplierIDs and SupplierNames
    def create_empty_supplier_list(self):
        supplier_list = {}
        return supplier_list

    # Define a method to update the supplier_list dictionary with the latest data from the Suppliers table
    def update_supplier_list(self, supplier_list):
        self.cursor.execute('SELECT SupplierID, SupplierName FROM Suppliers')
        rows = self.cursor.fetchall()

        for row in rows:
            supplier_list[row.SupplierID] = row.SupplierName

        return supplier_list

    # Define a static method to check if ContactInfo is a non-empty string
    @staticmethod
    def is_valid_contact_info(contact_info):
        return contact_info is not None and len(contact_info.strip()) > 0

    # Define a method to execute a query to fetch all data from the Suppliers table and display it in a formatted table
    def display_suppliers_table(self):
        self.cursor.execute('SELECT * FROM Suppliers')
        rows = self.cursor.fetchall()

        if rows:
            print("Suppliers Table:")
            print("SupplierID |         SupplierName     | ContactInfo")
            print("-" * 56)
            for row in rows:
                print(f"{row.SupplierID:10} | {row.SupplierName:24} | {row.ContactInfo:13}")
        else:
            print("No records found in the Suppliers table.")

    # Define a method to add a new unique SupplierName and a matching unique SupplierID to the Suppliers table
    def add_new_supplier(self, updated_supplier_list):
        while True:
            try:
                # Prompt user to input the new new_supplier_name
                new_supplier_name = input("Enter the new SupplierName: ")

                # Check if new_supplier_name is empty or contains only whitespace characters
                if not new_supplier_name.strip():
                    raise ValueError("Supplier name cannot be empty or contain only whitespace characters.")

                # Check if the new_supplier_name already exists in the updated_supplier_list
                if new_supplier_name in updated_supplier_list.values():
                    print(f"{new_supplier_name} is an already existing SupplierName in the table Suppliers.")
                    continue

                # Execute a SQL query to get the maximum SupplierID from the Suppliers table
                self.cursor.execute("SELECT MAX(SupplierID) FROM Suppliers")
                current_max_id = self.cursor.fetchone()[0]
                new_supplier_id = current_max_id + 1 if current_max_id is not None else 1

                contact_info = input("Enter the ContactInfo: ")

                while not self.is_valid_contact_info(contact_info):
                    print("Invalid ContactInfo. Please enter a non-empty string.")
                    contact_info = input("Enter the ContactInfo: ")

                self.cursor.execute(
                    f"INSERT INTO Suppliers (SupplierID, SupplierName, ContactInfo) VALUES ({new_supplier_id}, '{new_supplier_name}', '{contact_info}')"
                )
                self.conn.commit()

                updated_supplier_list = self.update_supplier_list(updated_supplier_list)
                break

            # Handle exceptions related to invalid input (ValueError)
            except ValueError as e:
                print(f"Error: {e}")

    # Define a method to change the name of an old SupplierName in the Suppliers table
    def change_supplier_name(self, updated_supplier_list):
        # Start an infinite loop for continuous input until a valid entry is provided
        while True:
            try:
                # Prompt user to input the old SupplierName to be changed
                old_supplier_name = input("Enter the name of the old SupplierName you want to change: ")

                # Check if old_supplier_name is not an existing SupplierName in the updated_supplier_list
                if old_supplier_name not in updated_supplier_list.values():
                    print(f"{old_supplier_name} is not an existing SupplierName in the table Suppliers.")
                    continue

                # Continue looping until a valid new_supplier_name is provided
                while True:
                    # Prompt user to input the new SupplierName
                    new_supplier_name = input("Enter the new SupplierName: ")

                    # Check if new_supplier_name is empty or contains only whitespace characters
                    if not new_supplier_name.strip():
                        print("New SupplierName cannot be empty or contain only whitespace characters.")
                        continue

                    # Check if new_supplier_name is an existing SupplierName in the updated_supplier_list
                    if new_supplier_name in updated_supplier_list.values():
                        print(f"{new_supplier_name} is an existing supplierName in the table Suppliers.")
                        continue

                    # Get the old SupplierID based on the old SupplierName
                    old_supplier_id = [k for k, v in updated_supplier_list.items() if v == old_supplier_name][0]
                    
                    new_contact_info = input("Enter the ContactInfo: ")

                    while not self.is_valid_contact_info(new_contact_info):
                        print("Invalid ContactInfo. Please enter a non-empty string.")
                        new_contact_info = input("Enter the new ContactInfo: ")


                    #new_stock_quantity = input("Enter the new StockQuantity (greater than or equals to 0): ")
                    #while not self.is_valid_stock_quantity(new_stock_quantity):
                        #print("Invalid StockQuantity. Please enter a valid integer greater than or equals to 0.")
                        #new_stock_quantity = input("Enter the new StockQuantity (greater than or equals to 0): ")

                    # Execute a SQL query to update the old SupplierName and ContactInfo in the Suppliers table
                    self.cursor.execute(
                        f"UPDATE Suppliers SET SupplierName = '{new_supplier_name}', ContactInfo = {new_contact_info} WHERE SupplierID = {old_supplier_id}"
                    )
                    # Commit the changes to the database
                    self.conn.commit()

                    # Update the supplier list with the changes
                    updated_supplier_list = self.update_supplier_list(updated_supplier_list)
                    # Exit the loop after a successful entry
                    break

                # Exit the outer loop after a successful entry
                break

            # Handle exceptions related to invalid input (ValueError)
            except ValueError as e:
                print(f"Error: {e}")



    # Define a method to change only the ContactInfo of an old SupplierName in the Suppliers table
    def change_contact_info(self, updated_supplier_list):
        while True:
            old_supplier_name = input("Enter the name of the supplier you want to update: ")

            if old_supplier_name not in updated_supplier_list.values():
                print(f"{old_supplier_name} is not an existing SupplierName in the table Suppliers.")
                continue

            old_supplier_id = [k for k, v in updated_supplier_list.items() if v == old_supplier_name][0]

            new_contact_info = input("Enter the new ContactInfo: ")

            while not self.is_valid_contact_info(new_contact_info):
                print("Invalid ContactInfo. Please enter a non-empty string.")
                new_contact_info = input("Enter the new ContactInfo: ")

            self.cursor.execute(
                f"UPDATE Suppliers SET ContactInfo = '{new_contact_info}' WHERE SupplierID = {old_supplier_id}"
            )
            self.conn.commit()

            updated_supplier_list = self.update_supplier_list(updated_supplier_list)
            break

    # Define a method to delete a specified old SupplierName and its corresponding SupplierID and ContactInfo from the Suppliers table
    def delete_supplier(self, updated_supplier_list):
        while True:
            old_supplier_name = input("Enter the name of the old SupplierName you want to delete: ")

            if old_supplier_name not in updated_supplier_list.values():
                print(f"{old_supplier_name} is not an existing SupplierName in the table Suppliers.")
                continue

            old_supplier_id = [k for k, v in updated_supplier_list.items() if v == old_supplier_name][0]

            self.cursor.execute(f"DELETE FROM Suppliers WHERE SupplierID = {old_supplier_id}")
            self.conn.commit()

            updated_supplier_list = self.update_supplier_list(updated_supplier_list)
            break

    # Define a method to run the main program loop, allowing the user to interact with the inventory management system
    def run_program(self):
        while True:
            self.display_suppliers_table()

            supplier_list = self.create_empty_supplier_list()
            updated_supplier_list = self.update_supplier_list(supplier_list)

            print("\nOptions:")
            print("1. Add a new SupplierName")
            print("2. Change the name of an old SupplierName")
            print("3. Change only the ContactInfo of an old SupplierName")
            print("4. DELETE an old SupplierName and its entire row")
            print("5. Terminate the program")

            choice = input("Enter your choice (1, 2, 3, 4, or 5): ")

            if choice == '1':
                self.add_new_supplier(updated_supplier_list)
            elif choice == '2':
                self.change_supplier_name(updated_supplier_list)
            elif choice == '3':
                self.change_contact_info(updated_supplier_list)
            elif choice == '4':
                self.delete_supplier(updated_supplier_list)
            elif choice == '5':
                self.display_suppliers_table()
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





