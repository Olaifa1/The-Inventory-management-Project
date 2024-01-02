import pyodbc


def get_supplier_id():
    while True:
        #   Tell user to enter SupplierID and check if SupplierID provided is an integer.
        try:
            supplier_id = int(input("Enter SupplierID (integer): "))
            return supplier_id
        # if SupplierID provided by the user is not an integer, throw the exception error(ValueError)
        except ValueError:
            print("SupplierID value is not acceptable. Please enter an integer.")

def get_supplier_name():
    while True:
        try:
            supplier_name = input("Enter SupplierName (string): ")
            return supplier_name
        except ValueError:
            print("SupplierName value is not acceptable. Please enter an String.")

def get_contact_info():
    while True:
        try:
            contact_info = input("Enter contact_info (string): ")
            return contact_info
        except ValueError:
            print("Contact info value is not acceptable. Please enter an String.")

def is_supplier_id_taken(supplier_id, cursor):
    cursor.execute("SELECT COUNT(*) FROM Suppliers WHERE SupplierID = ?", supplier_id)
    return cursor.fetchone()[0] > 0

def display_table(cursor):
    # Retrieve and display data from the Suppliers table
    cursor.execute("SELECT * FROM Suppliers")
    rows = cursor.fetchall()

    if rows:
        print("Suppliers Table:")
        print("SupplierID |    SupplierName     | ContactInfo")
        print("-" * 46)
        for row in rows:
            print(f"{row.SupplierID:10} | {row.SupplierName:19} | {row.ContactInfo:13}")
    else:
        print("No records found in the Suppliers table.")

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

        # Prompt user for SupplierID
        supplier_id = get_supplier_id()

        # Check if SupplierID is taken
        while is_supplier_id_taken(supplier_id, cursor):
            print("SupplierID is already taken. Please enter another SupplierID.")
            supplier_id = get_supplier_id()

        # Prompt user for SupplierName
        supplier_name = get_supplier_name()

        # Prompt user for Contact info
        contact_info = get_contact_info()

        # Update the Suppliers table
        cursor.execute("INSERT INTO Suppliers (SupplierID, SupplierName, ContactInfo) VALUES (?, ?, ?)",
                       supplier_id, supplier_name, contact_info)
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

    
