# __init__.py





import pyodbc
import random
from datetime import datetime


# Connection parameters
server = 'DESKTOP-SH1HJJ8\\SQLEXPRESS'
database = 'InventoryManagement'
trusted_connection = 'yes'
user = 'DESKTOP-SH1HJJ8\\Olaifa Olawale'

# Create a connection string
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};USER ID={user}'



def generate_unique_transaction_id(existing_transaction_ids):
    while True:
        transaction_id = random.randint(1000, 9999)  # Adjust range as needed
        if transaction_id not in existing_transaction_ids:
            return transaction_id

        
def get_product_name():
    while True:
        product_name = input("Enter ProductName (string): ")
        if product_name:
            return product_name
        else:
            print("ProductName cannot be empty. Please enter a valid ProductName.")


def generate_unique_product_id(existing_product_ids):
    while True:
        product_id = random.randint(0, 11)  # Adjust range as needed
        if product_id not in existing_product_ids:
            return product_id    



def generate_unique_supplier_id(existing_supplier_ids):
    while True:
        supplier_id = random.randint(1000, 9999)  # Adjust range as needed
        if supplier_id not in existing_supplier_ids:
            return supplier_id
    

def get_transaction_type():
    while True:
        try:
            transaction_type = input("Enter TransactionType (In/Out): ").capitalize()
            if transaction_type in ['In', 'Out']:
                return transaction_type
            else:
                print("Invalid TransactionType. Please enter 'In' or 'Out'.")
        except ValueError:
            print("TransactionType value is not acceptable. Please enter 'In' or 'Out'.")

def get_quantity():
    while True:
        try:
            quantity = int(input("Enter Quantity: "))
            if quantity >= 0:
                return quantity
            else:
                print("Quantity value is unacceptable. Please enter a non-negative integer.")
        except ValueError:
            print("Quantity value is not acceptable. Please enter an integer.")

def display_table(cursor):
    cursor.execute("SELECT * FROM Transactions")
    rows = cursor.fetchall()

    if rows:
        print("Transactions Table:")
        print("TransactionID | ProductID | ProductName | SupplierID | TransactionType | Quantity | TransactionDate")
        print("-" * 90)
        for row in rows:
            print(f"{row.TransactionID:14} | {row.ProductID:9} | {row.ProductName:11} | {row.SupplierID:11} | {row.TransactionType:16} | {row.Quantity:8} | {row.TransactionDate}")
    else:
        print("No records found in the Transactions table.")



while True:
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Generate unique TransactionID
        existing_transaction_ids = [row.TransactionID for row in cursor.execute("SELECT TransactionID FROM Transactions")]
        transaction_id = generate_unique_transaction_id(existing_transaction_ids)
       
        
        #   Prompt user for Product name
        product_name = get_product_name()

        # Generate unique ProductID
        existing_product_ids = [row.ProductID for row in cursor.execute("SELECT ProductID FROM Transactions")]
        product_id = generate_unique_product_id(existing_product_ids)

        
        # Generate unique SupplierID
        existing_supplier_ids = [row.SupplierID for row in cursor.execute("SELECT SupplierID FROM Transactions")]
        supplier_id = generate_unique_supplier_id(existing_supplier_ids)
    
        
        transaction_type = get_transaction_type()
        quantity = get_quantity()
        transaction_date = datetime.now().date()

        
        
        cursor.execute("""
            INSERT INTO Transactions (TransactionID, ProductID, ProductName, SupplierID, TransactionType, Quantity, TransactionDate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, transaction_id, product_id, product_name, supplier_id, transaction_type, quantity, transaction_date)
        connection.commit()

        print("Record updated successfully!")

        choice = input("Enter '!' to terminate or any other key to continue: ")
        if choice == '!':
            display_table(cursor)
            break

    except pyodbc.Error as ex:
        print(f"Error: {ex}")
    finally:
        if 'connection' in locals():
            connection.close()
