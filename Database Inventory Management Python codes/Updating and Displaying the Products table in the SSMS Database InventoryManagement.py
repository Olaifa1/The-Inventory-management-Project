import pyodbc

def update_product_table():
    # Connect to the SQL Server
    connection_string = 'DRIVER={SQL Server};SERVER=DESKTOP-SH1HJJ8\\SQLEXPRESS;DATABASE=InventoryManagement;Trusted_Connection=yes;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Dictionary of products
    product_list = {1: "Bournvita",
                    2: "Milo",
                    3: "Cornflakes",
                    4: "Chivita",
                    5: "Ribena",
                    6: "Corn Oat",
                    7: "Ovaltine",
                    8: "Peak milk",
                    9: "Five Alive",
                    10: "Chocolate"}

    # Check if the number of rows in the table is not equal to the length of the dictionary
    while True:
        cursor.execute("SELECT COUNT(*) FROM Products")
        num_rows = cursor.fetchone()[0]

        if num_rows == len(product_list):
            break

        # Prompt the user to enter a ProductName
        product_name = input("Enter a ProductName from the given list of products: Bournvita, Milo, Cornflakes, Chivita, Ribena, Corn Oat, Ovaltine, Peak milk, Five Alive, Chocolate\n")

        # Check if the entered ProductName is in the dictionary
        if product_name not in product_list.values():
            print("ProductName not in the list. Please enter a valid ProductName.")
            continue

        # Check if the ProductName is already in the table
        cursor.execute("SELECT COUNT(*) FROM Products WHERE ProductName = ?", product_name)
        if cursor.fetchone()[0] > 0:
            print(f"{product_name} is already taken. Please enter another ProductName.")
            continue

        # Find the corresponding ProductID
        product_id = [key for key, value in product_list.items() if value == product_name][0]

        # Prompt the user to enter StockQuantity
        while True:
            stock_quantity = int(input(f"Enter StockQuantity for {product_name}: "))

            if stock_quantity < 0:
                print("StockQuantity value is unacceptable. Please enter another StockQuantity equal to or greater than 0.")
            else:
                break

        # Update the table with the new values
        cursor.execute("INSERT INTO Products (ProductID, ProductName, StockQuantity) VALUES (?, ?, ?)", product_id, product_name, stock_quantity)
        conn.commit()

    # Display the updated table
    cursor.execute("SELECT * FROM Products")
    rows = cursor.fetchall()

    if rows:
        print("Products Table:")
        print("ProductID | ProductName  | StockQuantity")
        print("-" * 40)
        for row in rows:
            print(f"{row.ProductID:9} | {row.ProductName:12} | {row.StockQuantity:13}")
    else:
        print("No records found in the Products table.")

    # Close the connection
    conn.close()

# Call the function
update_product_table()



































