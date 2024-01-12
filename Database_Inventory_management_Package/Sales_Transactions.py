
# Sales_Transactions.py

import pyodbc
import random
import re
from datetime import datetime

class SalesTransactions:
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

    def create_empty_customer_list(self):
        customer_list = {}
        return customer_list

    def update_customer_list(self, customer_list):
        self.cursor.execute('SELECT CustomerID, CustomerName FROM Customers')
        rows = self.cursor.fetchall()

        for row in rows:
            customer_list[row.CustomerID] = row.CustomerName

        return customer_list

    def get_valid_input(self, input_type, validation_pattern, error_message):
        while True:
            user_input = input(f"Enter the {input_type}: ").strip()
            user_input = user_input.title()  # Convert to Title case

            if not re.match(validation_pattern, user_input):
                print(error_message)
            else:
                return user_input

    def get_valid_customer_name(self):
        validation_pattern = "^[A-Za-z]+( [A-Za-z]+)*$"
        error_message = "Customer name must contain only English alphabets in sentence case."
        return self.get_valid_input("CustomerName", validation_pattern, error_message)


    def get_gender(self):
        gender_pattern = re.compile(r'^(male|female)$', re.IGNORECASE)

        while True:
            gender_input = input("Enter your gender (male/female): ").strip()

            if not gender_pattern.match(gender_input):
                print("Invalid input. Please enter either 'male' or 'female'.")
                continue

            return gender_input.title()
    
    def get_age(self):
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

        while True:
            dob_input = input("Enter your date of birth (YYYY-MM-DD): ").strip()

            if not date_pattern.match(dob_input):
                print("Invalid input. Please enter a valid date of birth in the format YYYY-MM-DD.")
                continue

            try:
                dob = datetime.strptime(dob_input, '%Y-%m-%d').date()
            except ValueError:
                print("Invalid date. Please enter a valid date in the format YYYY-MM-DD.")
                continue

            age = datetime.now().year - dob.year - ((datetime.now().month, datetime.now().day) < (dob.month, dob.day))

            return age

    def get_country(self):
        validation_pattern = "^[A-Za-z]+( [A-Za-z]+)*$"
        error_message = "Country must contain only English alphabets."
        return self.get_valid_input("Country", validation_pattern, error_message)
    
    def get_state(self):
        validation_pattern = "^[A-Za-z]+( [A-Za-z]+)*$"
        error_message = "State must contain only English alphabets."
        return self.get_valid_input("State", validation_pattern, error_message)
    
    def get_county(self):
        validation_pattern = "^[A-Za-z]+( [A-Za-z]+)*$"
        error_message = "County must contain only English alphabets."
        return self.get_valid_input("County", validation_pattern, error_message)
    
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
    
    def get_valid_product_name(self):
        validation_pattern = "^[A-Za-z]+( [A-Za-z]+)*$"
        error_message = "Product name must contain only English alphabets."
        return self.get_valid_input("ProductName", validation_pattern, error_message)


            
    
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

    def get_valid_selling_price(self):
        while True:
            selling_price = input("Enter the Unit Selling Price of the Product (greater than 0): ")

            if re.match("^[0-9]+$", selling_price):
                selling_price = int(selling_price)
                if selling_price > 0:
                    return selling_price
                else:
                    print("Invalid Selling Price. Please enter a non-negative integer.")
            else:
                print("Invalid Selling Price. Please enter a valid integer greater than 0.")
    
    

    def display_sales_transactions_table(self):
        self.cursor.execute('SELECT * FROM Sales_Transactions')
        rows = self.cursor.fetchall()

        if rows:
                print("Sales Transactions Table:")
                print("TransactionID | ProductID | CustomerID | ProductName  | CustomerName             | Gender | Age | Country | State | County | Email                 | PhoneNumber |  Quantity | Selling_Price | TransactionDate")
                print("-" * 160)
                for row in rows:
                    print(f"{row.TransactionID:8} | {row.ProductID:9} | {row.CustomerID:10} | {row.ProductName:12} | {row.CustomerName:24} | {row.Gender:9} | {row.Age:9} | {row.Country:12} | {row.State:12} | {row.County:12} | {row.Email:18} | {row.PhoneNumber:12} |  {row.Quantity:8} | {row.Selling_Price:12} | {row.TransactionDate}")
        else:
            print("No records found in the Sales Transactions table.")


    def add_transaction(self, updated_product_list, updated_customer_list):
        while True:
            try:
                existing_transaction_ids = [row.TransactionID for row in self.cursor.execute("SELECT TransactionID FROM Sales_Transactions")]

                # Generate unique TransactionID
                transaction_id = self.generate_unique_transaction_id(existing_transaction_ids)

                product_name = self.get_valid_product_name()
                
                #   while product name is in updated_product_list, match the corresponding product_id to the product name.
                while product_name in updated_product_list.values():
                    product_id = [k for k, v in updated_product_list.items() if v == product_name][0]

                    quantity = self.get_valid_quantity() 

                    updated_product_list = self.update_product_list(updated_product_list)
                    
                    selling_price = self.get_valid_selling_price()

                    customer_name = self.get_valid_customer_name()

                    gender = self.get_gender()
                    age = self.get_age()
                    country = self.get_country()
                    state = self.get_state()
                    county = self.get_county()
                    email = self.get_email()
                    phone = self.get_phone_number()

                    if customer_name in updated_customer_list.values():
                        customer_id = [k for k, v in updated_customer_list.items() if v == customer_name][0]
                    else:
                        # Execute a SQL query to get the maximum CustomerID from the Customers table
                        self.cursor.execute("SELECT MAX(CustomerID) FROM Customers")
                        current_max_id = self.cursor.fetchone()[0]
                        customer_id = current_max_id + 1 if current_max_id is not None else 1
                        

                        # EXECUTE A SQL QUERY TO INSERT CustomerID, CustomerName, Gender, Age, Country, State, County, Email, PhoneNumber INTO TABLE CUSTOMERS
                        self.cursor.execute(
                            "INSERT INTO Customers (CustomerID, CustomerName, Gender, Age, Country, State, County, Email, PhoneNumber) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            customer_id, customer_name, gender, age, country, state, county, email, phone
                        )
                        self.conn.commit()

                        updated_customer_list = self.update_customer_list(updated_customer_list)
                    
                    transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    self.cursor.execute(
                        "INSERT INTO Sales_Transactions (TransactionID, ProductID, CustomerID, ProductName, CustomerName, Gender, Age, Country, State, County, Email, PhoneNumber, Quantity, Selling_Price, TransactionDate) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        transaction_id, product_id, customer_id, product_name, customer_name, gender, age, country, state, county, email, phone, quantity, selling_price, transaction_date
                    )
                    self.conn.commit()

                    break

                while product_name not in updated_product_list.values():
                    print(f"{product_name} is currently not in stock.")
                    break

                break

            except ValueError as e:
                print(f"Error: {e}")

    def delete_transaction(self):
        while True:
            try:
                transaction_id = input("Enter the TransactionID to delete: ").strip()

                if not re.match("^[0-9]+$", transaction_id):
                    print("Invalid TransactionID. Please enter a valid integer.")
                    continue

                transaction_id = int(transaction_id)

                # Check if the transaction_id exists in the Sales_Transactions table
                if transaction_id not in [row.TransactionID for row in self.cursor.execute("SELECT TransactionID FROM Sales_Transactions")]:
                    print("Invalid TransactionID. The specified transaction does not exist.")
                    continue

                # Fetch information from the specified transaction_id
                transaction_info = self.cursor.execute(
                    f"SELECT * FROM Sales_Transactions WHERE TransactionID = {transaction_id}"
                ).fetchone()

                # Delete the row from Sales_Transactions
                self.cursor.execute(f"DELETE FROM Sales_Transactions WHERE TransactionID = {transaction_id}")
                self.conn.commit()


                print(f"Transaction with TransactionID {transaction_id} has been deleted successfully.")
                break

            except ValueError as e:
                print(f"Error: {e}")
    
    
    
    def run_program(self):
        while True:
            self.display_sales_transactions_table()

            product_list = self.create_empty_product_list()
            updated_product_list = self.update_product_list(product_list)

            customer_list = self.create_empty_customer_list()
            updated_customer_list = self.update_customer_list(customer_list)

            print("\nOptions:")
            print("1. Add a Sales Transaction")
            print("2. Delete a Sales Transaction")
            print("3. Terminate the program")

            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == '1':
                self.add_transaction(updated_product_list, updated_customer_list)
            elif choice == '2':
                self.delete_transaction()
            elif choice == '3':
                self.display_sales_transactions_table()
                self.conn.close()
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

# The following line creates an instance of the SalesTransactions class and executes the main program loop
if __name__ == "__main__":
    # Define the connection string with details to connect to the SQL Server
    connection_string = 'DRIVER={SQL Server};SERVER=DESKTOP-SH1HJJ8\\SQLEXPRESS;DATABASE=InventoryManagement;Trusted_Connection=yes;'
    
    # Create an instance of the SalesTransactions class
    sales_transactions = SalesTransactions(connection_string)
    
    # Run the program using the instance
    sales_transactions.run_program()
































