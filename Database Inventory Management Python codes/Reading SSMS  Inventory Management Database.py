import pyodbc

# Connection parameters
server = 'DESKTOP-SH1HJJ8\\SQLEXPRESS'
database = 'InventoryManagement'
trusted_connection = 'yes'
user = 'DESKTOP-SH1HJJ8\\Olaifa Olawale'

# Create a connection string
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};USER ID={user}'

try:
    # Connect to the database
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

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

except pyodbc.Error as ex:
    print(f"Error: {ex}")

finally:
    # Close the connection
    if 'connection' in locals():
        connection.close()
