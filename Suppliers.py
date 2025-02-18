
import pyodbc
import re

class Suppliers:
    def __init__(self, connection_string):
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

    def display_suppliers_table(self):
        """Displays the entire Suppliers table with formatted output."""
        self.cursor.execute('SELECT * FROM Suppliers')
        rows = self.cursor.fetchall()

        if rows:
            print("Suppliers Table:")
            print("SupplierID | SupplierName         | Address               | Email                 | PhoneNumber")
            print("-" * 100)
            for row in rows:
                print(f"{row.SupplierID:10} | {row.SupplierName:20} | {row.Address:20} | {row.Email:20} | {row.PhoneNumber}")
        else:
            print("No records found in the Suppliers table.")

    def get_supplier_by_column(self):
        """Fetches and displays supplier details based on user input for any column."""
        while True:
            column_name = input("Enter the column name to search by (SupplierID, SupplierName, Address, Email, PhoneNumber): ").strip()
            
            valid_columns = ["SupplierID", "SupplierName", "Address", "Email", "PhoneNumber"]
            
            if column_name not in valid_columns:
                print("Invalid column name. Please enter a valid column header.")
                continue
            
            search_value = input(f"Enter the value to search for in {column_name}: ").strip()
            
            if column_name in ["SupplierID", "PhoneNumber"]:
                if not re.match("^[0-9]+$", search_value):
                    print("Invalid input. Please enter a numeric value.")
                    continue
                param = int(search_value)
                query = f"SELECT * FROM Suppliers WHERE {column_name} = ?"
            else:
                param = f"%{search_value}%"
                query = f"SELECT * FROM Suppliers WHERE {column_name} LIKE ?"
            
            self.cursor.execute(query, (param,))
            rows = self.cursor.fetchall()

            if rows:
                print("Matching Suppliers:")
                print("SupplierID | SupplierName         | Address               | Email                 | PhoneNumber")
                print("-" * 100)
                for row in rows:
                    print(f"{row.SupplierID:10} | {row.SupplierName:20} | {row.Address:20} | {row.Email:20} | {row.PhoneNumber}")
            else:
                print("No matching suppliers found.")
            
            break

    def run_program(self):
        """Runs the interactive menu-based program."""
        while True:
            print("\nOptions:")
            print("1. Display All Suppliers")
            print("2. Search for a Supplier by Any Column")
            print("3. Terminate the Program")

            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == '1':
                self.display_suppliers_table()
            elif choice == '2':
                self.get_supplier_by_column()
            elif choice == '3':
                print("Exiting program...")
                self.conn.close()
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    # Define the connection string for SQL Server
    connection_string = 'DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=InventoryManagement;Trusted_Connection=yes;'
    
    # Create an instance of the Suppliers class and run the program
    suppliers_app = Suppliers(connection_string)
    suppliers_app.run_program()

