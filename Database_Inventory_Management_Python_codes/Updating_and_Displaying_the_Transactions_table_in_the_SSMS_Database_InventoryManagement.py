# inventory_management/transactions.py


import pyodbc
import random
from datetime import datetime

def connect_to_database():
    connection_string = 'DRIVER={SQL Server};SERVER=DESKTOP-SH1HJJ8\\SQLEXPRESS;DATABASE=InventoryManagement;Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    return conn, cursor

def get_product_input(prompt, input_type):
    product_list = {
        1: "Bournvita",
        2: "Milo",
        3: "Cornflakes",
        4: "Chivita",
        5: "Ribena",
        6: "Corn Oat",
        7: "Ovaltine",
        8: "Peak milk",
        9: "Five Alive",
        10: "Chocolate"
    }

    while True:
        try:
            user_input = input(prompt)
            # Check if the entered ProductName/user_input is in the dictionary
            if user_input not in product_list.values():
                print("ProductName not in the list. Please enter a valid ProductName.")
                continue
            else:
                return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")


def get_supplier_input(prompt, input_type):
    supplier_list = {
        1: "John Brews Rice farm",
        2: "Dave Poultry",
        3: "Stonebridge maize farm",
        4: "Dejones orange farm",
        5: "Quentin fish farm",
        6: "Adejumo Rice mill",
        7: "Rites Bottle factory",
        8: "Kelvin Paper mill",
        9: "Delight nylon factory",
        10: "Bua Sugar"
    }

    while True:
        try:
            user_input = input(prompt)
            # Check if the entered SupplierName/user_input is in the dictionary
            if user_input not in supplier_list.values():
                print("SupplierName not in the list. Please enter a valid SupplierName.")
                continue
            else:
                return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")

def get_transaction_type_input(prompt, input_type):
    transaction_type_list = {
        1: "In",
        2: "Out"
    }
    while True:
        try:
            user_input = input(prompt)
            # Check if the entered transaction_type/user_input is in the dictionary
            if user_input not in transaction_type_list.values():
                print("Transaction_type not acceptable. Please enter a valid transaction_type.")
                continue
            else:
                return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")

def get_quantity_input(prompt, input_type):
    
    while True:
        try:
            user_input = input(prompt)
            return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")


def get_id_from_dict(data_dict, name, id_key):
    return next(key for key, value in data_dict.items() if value == name)

def generate_unique_transaction_id(existing_transaction_ids):
    while True:
        transaction_id = random.randint(10000, 99999)
        if transaction_id not in existing_transaction_ids:
            return transaction_id
    
def update_transactions_table(conn, cursor, product_list, supplier_list):
    existing_transaction_ids = [row.TransactionID for row in cursor.execute("SELECT TransactionID FROM Transactions")]

    # Generate unique TransactionID
    transaction_id = generate_unique_transaction_id(existing_transaction_ids)

    # Prompt user to enter ProductName from the Dictionary product_list
    product_name = get_product_input("""Enter a Product Name from the given list of products:
                                Bournvita
                                Milo
                                Cornflakes
                                Chivita
                                Ribena
                                Corn Oat
                                Ovaltine
                                Peak milk
                                Five Alive
                                Chocolate
                            """, str)
    


    # Validate and get ProductID
    product_id = get_id_from_dict(product_list, product_name, 'ProductID')

    # Prompt user to enter SupplierName from the Dictionary supplier_list
    supplier_name = get_supplier_input(""" Enter a SupplierName from the given list of Suppliers:
                                    John Brews Rice farm
                                    Dave Poultry
                                    Stonebridge maize farm
                                    Dejones orange farm
                                    Quentin fish farm
                                    Adejumo Rice mill
                                    Bua Sugar
                                    Rites Bottle factory
                                    Kelvin Paper mill
                                    Delight nylon factory
                                """, str)

    # Validate and get SupplierID
    supplier_id = get_id_from_dict(supplier_list, supplier_name, 'SupplierID')

    # Prompt user to enter TransactionType
    transaction_type = get_transaction_type_input("Enter TransactionType (In/Out): ", str).capitalize()

    # Prompt user to enter Quantity
    quantity = get_quantity_input("Enter Quantity: ", int)

    # Use current date method to auto-generate the date and time
    transaction_date = datetime.now()

    # Update the Table Transactions
    cursor.execute("""
        INSERT INTO Transactions (TransactionID, ProductID, SupplierID, ProductName, SupplierName, TransactionType, Quantity, TransactionDate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, transaction_id, product_id, supplier_id, product_name, supplier_name, transaction_type, quantity, transaction_date)
    conn.commit()

    

def main():
    conn, cursor = connect_to_database()

    supplier_list = {
        1: "John Brews Rice farm",
        2: "Dave Poultry",
        3: "Stonebridge maize farm",
        4: "Dejones orange farm",
        5: "Quentin fish farm",
        6: "Adejumo Rice mill",
        7: "Rites Bottle factory",
        8: "Kelvin Paper mill",
        9: "Delight nylon factory",
        10: "Bua Sugar"
    }

    product_list = {
        1: "Bournvita",
        2: "Milo",
        3: "Cornflakes",
        4: "Chivita",
        5: "Ribena",
        6: "Corn Oat",
        7: "Ovaltine",
        8: "Peak milk",
        9: "Five Alive",
        10: "Chocolate"
    }

    while True:
        update_transactions_table(conn, cursor, product_list, supplier_list)
        choice = input("Enter '!' to terminate or any other key to continue: ")
        if choice == '!':
            # Display the Table Transactions
            cursor.execute("SELECT * FROM Transactions")
            rows = cursor.fetchall()

            if rows:
                print("Transactions Table:")
                print("TransactionID | ProductID | SupplierID | ProductName  | SupplierName             | TransactionType | Quantity | TransactionDate")
                print("-" * 130)
                for row in rows:
                    print(f"{row.TransactionID:13} | {row.ProductID:9} | {row.SupplierID:10} | {row.ProductName:12} | {row.SupplierName:24} | {row.TransactionType:15} | {row.Quantity:8} | {row.TransactionDate}")
            else:
                print("No records found in the Transactions table.")
            break

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
