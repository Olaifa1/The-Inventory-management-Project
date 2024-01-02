# Suppliers.py

import pyodbc


def get_contact_info():
    while True:
        try:
            contact_info = input("Enter contact_info (string): ")
            return contact_info
        except ValueError:
            print("Contact info value is not acceptable. Please enter an String.")

def update_supplier_table():
    # Connect to the SQL Server
    connection_string = 'DRIVER={SQL Server};SERVER=DESKTOP-SH1HJJ8\\SQLEXPRESS;DATABASE=InventoryManagement;Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Dictionary of suppliers
    supplier_list = {1: "John Brews Rice farm",
                     2: "Dave Poultry",
                     3: "Stonebridge maize farm",
                     4: "Dejones orange farm",
                     5: "Quentin fish farm",
                     6: "Adejumo Rice mill",
                     7: "Rites Bottle factory",
                     8: "Kelvin Paper mill",
                     9: "Delight nylon factory",
                     10: "Bua Sugar"}

    # Check if the number of rows in the table is not equal to the length of the dictionary
    while True:
        cursor.execute("SELECT COUNT(*) FROM Suppliers")
        num_rows = cursor.fetchone()[0]

        if num_rows == len(supplier_list):
            break

        # Prompt the user to enter a SupplierName
        supplier_name = input(""" Enter a SupplierName from the given list of Suppliers:
                                    John Brews Rice farm,
                                    Dave Poultry,
                                    Stonebridge maize farm,
                                    Dejones orange farm,
                                    Quentin fish farm,
                                    Adejumo Rice mill,
                                    Bua Sugar,
                                    Rites Bottle factory,
                                    Kelvin Paper mill,
                                    Delight nylon factory
                                """)

        # Check if the entered SupplierName is in the dictionary
        if supplier_name not in supplier_list.values():
            print("SupplierName not in the list. Please enter a valid SupplierName.")
            continue

        # Check if the SupplierName is already in the table
        cursor.execute("SELECT COUNT(*) FROM Suppliers WHERE SupplierName = ?", supplier_name)
        if cursor.fetchone()[0] > 0:
            print(f"{supplier_name} is already taken. Please enter another SupplierName.")
            continue

        # Find the corresponding SupplierID
        supplier_id = [key for key, value in supplier_list.items() if value == supplier_name][0]

        # Prompt user for Contact info
        contact_info = get_contact_info()

        # Update the table with the new values
        cursor.execute("INSERT INTO Suppliers (SupplierID, SupplierName, ContactInfo) VALUES (?, ?, ?)", supplier_id, supplier_name, contact_info)
        conn.commit()

    # Display the updated table
    cursor.execute("SELECT * FROM Suppliers")
    rows = cursor.fetchall()

    if rows:
        print("Suppliers Table:")
        print("SupplierID | SupplierName             | ContactInfo")
        print("-" * 46)
        for row in rows:
            print(f"{row.SupplierID:10} | {row.SupplierName:24} | {row.ContactInfo:13}")
    else:
        print("No records found in the Suppliers table.")

    # Close the connection
    conn.close()

# Call the function
update_supplier_table()



































