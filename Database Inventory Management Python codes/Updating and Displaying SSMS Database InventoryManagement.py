import pyodbc


def get_product_id():
    while True:
        #   Tell user to enter ProductID and check if ProductID provided is an integer.
        try:
            product_id = int(input("Enter ProductID (integer): "))
            return product_id
        # if product ID provided by th user is not an integer, throw the exception error(ValueError)
        except ValueError:
            print("ProductID value is not acceptable. Please enter an integer.")

def get_product_name():
    while True:
        try:
            product_name = input("Enter ProductName (string): ")
            return product_name
        except ValueError:
            print("ProductName value is not acceptable. Please enter an String.")

def get_stock_quantity():
    while True:
        try:
            stock_quantity = int(input("Enter StockQuantity (should be equal to or greater than 0): "))
            if stock_quantity >= 0:
                return stock_quantity
            else:
                print("StockQuantity value is unacceptable. Please enter another value.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def is_product_id_taken(product_id, cursor):
    cursor.execute("SELECT COUNT(*) FROM Products WHERE ProductID = ?", product_id)
    return cursor.fetchone()[0] > 0

def display_table(cursor):
    # Retrieve and display data from the Products table
    cursor.execute("SELECT * FROM Products")
    rows = cursor.fetchall()

    if rows:
        print("Products Table:")
        print("ProductID | ProductName | StockQuantity")
        print("-" * 40)
        for row in rows:
            print(f"{row.ProductID:9} | {row.ProductName:12} | {row.StockQuantity:13}")
    else:
        print("No records found in the Products table.")

# Connection parameters
server = 'DESKTOP-SH1HJJ8\\SQLEXPRESS'
database = 'InventoryManagement'
trusted_connection = 'yes'
user = 'DESKTOP-SH1HJJ8\\Olaifa Olawale'

# Create a connection string
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};USER ID={user}'

while True:
    try:
        # Connect to the database
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Prompt user for ProductID
        product_id = get_product_id()

        # Check if ProductID is taken
        while is_product_id_taken(product_id, cursor):
            print("ProductID is already taken. Please enter another ProductID.")
            product_id = get_product_id()

        # Prompt user for ProductName
        product_name = get_product_name()

        # Prompt user for StockQuantity
        stock_quantity = get_stock_quantity()

        # Update the Products table
        cursor.execute("INSERT INTO Products (ProductID, ProductName, StockQuantity) VALUES (?, ?, ?)",
                       product_id, product_name, stock_quantity)
        connection.commit()

        print("Record updated successfully!")


        # Ask user to continue or terminate the program
        choice = input("Enter '!' to terminate or any other key to continue: ")
        if choice == '!':
            # Display the table and terminate the program
            display_table(cursor)
            break
    
    except pyodbc.Error as ex:
        print(f"Error: {ex}")
    finally:
        # Close the connection
        if 'connection' in locals():
            connection.close()

    
