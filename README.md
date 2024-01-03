# The-Inventory-management-Project
This is a project of two phases: The first phase requires using SQL Server Management Studio to design a database for inventory management. The second phase requires writing Python codes to connect, populate, query and display the inventory management database. Below is a simple breakdown of the tasks done.


-  Inventory Management Application.
-  Database: SQL Server Management Studio.
-  Backend Programming language: Python.
-  Requirements Analysis: I identified the requirements for inventory tracking. I listed out the entities like products, suppliers, and transactions.
-   atabase Schema Design: I created a relational database schema. I defined tables, relationships, and constraints.
-  SQL Implementation: I wrote SQL scripts to create the database and tables. I included triggers or stored procedures for transaction updates.
- Functional Implementation:  I developed SQL queries for adding new products, updating stock levels, and generating reports and ensured data accuracy during stock transactions.
- User Interface Integration: I integrated the SQL database with a simple user interface using Python scripting language.
- End-to-end functionality testing.

## Step by step documentation of each Python file:

### Python module 1: inventory_management/transactions.py
- Connect to the SQL Server.
- Create a get_product_input function: To prompt user and to check if the entered ProductName/user_input is in the product_list dictionary.
- Create a get_supplier_input function: To prompt user and to check if the entered SupplierName/user_input is in the supplier_list dictionary.
- Create a get_transaction_type_input function: To prompt user and to check if the entered transaction_type/user_input is in the transaction_type_list dictionary.Create a get_quantity_input function: To prompt user to enter Stock quantity and to check if the entered quantity is a positive integer.
- Auto-generate unique TransactionID with randomint method.
- Invoke function get_product_input to prompt user to enter ProductName from the Dictionary product_list
- Validate and get ProductID
- Invoke function get_supplier_input to prompt user to enter SupplierName from the Dictionary supplier_list
- Validate and get SupplierID
- Invoke function get_transaction_type_input to prompt user to enter TransactionType
- Invoke function get_quantity_input function: To prompt user to enter Quantity
- Use current date method to auto-generate the date and time
- Update the Table Transactions
- Display the Table Transactions
- Close the connection



### Python module 2: inventory_management/suppliers.py
-	Connect to the SQL Server
-	Dictionary of suppliers
-	Check if the number of rows in the table is not equal to the length of the dictionary
-	Prompt the user to enter a SupplierName from the given list of Suppliers
-	Check if the entered SupplierName is in the dictionary
-	Check if the SupplierName is already in the table
-	Find the corresponding SupplierID
-	Prompt user for Contact info
-	Update the table with the new values
-	Display the updated table
-	Close the connection


### Python module 3:inventory_management/products.py
-	Connect to the SQL Server
-	Dictionary of products
-	Check if the number of rows in the table is not equal to the length of the dictionary.
-	Prompt the user to enter a ProductName from the given list of products
-	Check if the entered ProductName is in the dictionary
-	Check if the ProductName is already in the table.
-	Find the corresponding ProductID
-	Prompt the user to enter StockQuantity
-	Update the table with the new values
-	Display the updated table
-	Close the connection

### Python module 4:	__innit__.py






