

import pyodbc
import re

class Customers:
    def __init__(self, connection_string):
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

    def display_customers_table(self):
        """Displays the entire Customers table with formatted output."""
        self.cursor.execute('SELECT * FROM Customers')
        rows = self.cursor.fetchall()

        if rows:
            print("Customers Table:")
            print("CustomerID | CustomerName         | Gender  | Age | Country         | State           | County          | Email                 | PhoneNumber")
            print("-" * 130)
            for row in rows:
                print(f"{row.CustomerID:10} | {row.CustomerName:20} | {row.Gender:6} | {row.Age:3} | {row.Country:15} | {row.State:15} | {row.County:15} | {row.Email:20} | {row.PhoneNumber}")
        else:
            print("No records found in the Customers table.")

    def get_customer_by_column(self):
        """Fetches and displays customer details based on user input for any column."""
        while True:
            column_name = input("Enter the column name to search by (CustomerID, CustomerName, Gender, Age, Country, State, County, Email, PhoneNumber): ").strip()
            
            valid_columns = ["CustomerID", "CustomerName", "Gender", "Age", "Country", "State", "County", "Email", "PhoneNumber"]
            
            if column_name not in valid_columns:
                print("Invalid column name. Please enter a valid column header.")
                continue
            
            search_value = input(f"Enter the value to search for in {column_name}: ").strip()
            
            if column_name in ["CustomerID", "Age", "PhoneNumber"]:
                if not re.match("^[0-9]+$", search_value):
                    print("Invalid input. Please enter a numeric value.")
                    continue
                param = int(search_value)
                query = f"SELECT * FROM Customers WHERE {column_name} = ?"
            else:
                param = f"%{search_value}%"
                query = f"SELECT * FROM Customers WHERE {column_name} LIKE ?"
            
            self.cursor.execute(query, (param,))
            rows = self.cursor.fetchall()

            if rows:
                print("Matching Customers:")
                print("CustomerID | CustomerName         | Gender  | Age | Country         | State           | County          | Email                 | PhoneNumber")
                print("-" * 130)
                for row in rows:
                    print(f"{row.CustomerID:10} | {row.CustomerName:20} | {row.Gender:6} | {row.Age:3} | {row.Country:15} | {row.State:15} | {row.County:15} | {row.Email:20} | {row.PhoneNumber}")
            else:
                print("No matching customers found.")
            
            break

    def run_program(self):
        """Runs the interactive menu-based program."""
        while True:
            print("\nOptions:")
            print("1. Display All Customers")
            print("2. Search for a Customer by Any Column")
            print("3. Terminate the Program")

            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == '1':
                self.display_customers_table()
            elif choice == '2':
                self.get_customer_by_column()
            elif choice == '3':
                print("Exiting program...")
                self.conn.close()
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    # Define the connection string for SQL Server
    connection_string = 'DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=InventoryManagement;Trusted_Connection=yes;'
    
    # Create an instance of the Customers class and run the program
    customers_app = Customers(connection_string)
    customers_app.run_program()




























