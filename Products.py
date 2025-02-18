
import pyodbc
import re

class Products:
    def __init__(self, connection_string):
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

    def display_products_table(self):
        """Displays the entire Products table with formatted output."""
        self.cursor.execute('SELECT * FROM Products')
        rows = self.cursor.fetchall()

        if rows:
            print("Products Table:")
            print("ProductID | ProductName          | StockQuantity")
            print("-" * 50)
            for row in rows:
                print(f"{row.ProductID:9} | {row.ProductName:20} | {row.StockQuantity:13}")
        else:
            print("No records found in the Products table.")

    def get_product_by_name_or_id(self):
        """Fetches and displays product details based on user input (ProductName or ProductID)."""
        while True:
            search_input = input("Enter Product Name or Product ID: ").strip()
            
            if re.match("^[0-9]+$", search_input):
                query = "SELECT * FROM Products WHERE ProductID = ?"
                param = int(search_input)
            else:
                query = "SELECT * FROM Products WHERE ProductName LIKE ?"
                param = f"%{search_input}%"
            
            self.cursor.execute(query, (param,))
            rows = self.cursor.fetchall()

            if rows:
                print("Matching Products:")
                print("ProductID | ProductName          | StockQuantity")
                print("-" * 50)
                for row in rows:
                    print(f"{row.ProductID:9} | {row.ProductName:20} | {row.StockQuantity:13}")
            else:
                print("No matching products found.")
            
            break

    def run_program(self):
        """Runs the interactive menu-based program."""
        while True:
            print("\nOptions:")
            print("1. Display All Products")
            print("2. Search for a Product by Name or ID")
            print("3. Terminate the Program")

            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == '1':
                self.display_products_table()
            elif choice == '2':
                self.get_product_by_name_or_id()
            elif choice == '3':
                print("Exiting program...")
                self.conn.close()
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    # Define the connection string for SQL Server
    connection_string = 'DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=InventoryManagement;Trusted_Connection=yes;'
    
    # Create an instance of the Products class and run the program
    products_app = Products(connection_string)
    products_app.run_program()
