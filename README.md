# The-Inventory-management-Project
The Inventory management system is an application that is able to keep real-time records of stocks supplied and supplier details, stocks sold and customer details, time and price of sales, stock balance in the warehouse/stock-house, salespersons involved in the transaction, Supply Order unique Identity and Sales Order unique Identity for the purpose of investigating  fraudulent supply or sales transactions.
This is a project of two phases: The first phase requires using SQL Server Management Studio to design a database for inventory management. The second phase requires writing Python codes to prompt users for inputs and then connect, query, update or populate, and display the inventory management database. Below is a simple breakdown of the tasks done.


-  Inventory Management Application.
-  Database: SQL Server Management Studio.
-  Backend Programming language: Python.
-  Requirements Analysis: I identified the requirements for inventory tracking. I listed out the entities like products, suppliers, and transactions.
-   Database Schema Design: I created a relational database schema. I defined tables, relationships, and constraints.
-  SQL Implementation: I wrote SQL scripts to create the database and tables. I included triggers (stored procedures) for transaction updates.
- Functional Implementation:  I developed SQL queries for adding new products, updating stock levels, and generating reports and ensured data accuracy during stock transactions.
- User Interface Integration: I integrated the SQL database with a simple user interface using Python scripting language.
- End-to-end functionality testing.

## Step by step documentation of each Python file:

### Python module 1: inventory_management/transactions.py
####  This Python program is like a smart manager for an inventory system. It can add and delete transactions, ensuring that the data entered is valid and stored in a SQL Server database.
- Connect to the SQL Server.
- Create a get_product_input function: To prompt user and to check if the entered ProductName/user_input is in the product_list dictionary.
- Create a get_supplier_input function: To prompt user and to check if the entered SupplierName/user_input is in the supplier_list dictionary.
- Create a get_transaction_type_input function: To prompt user and to check if the entered transaction_type/user_input is in the transaction_type_list dictionary.
- Create a get_quantity_input function: To prompt user to enter Stock quantity and to check if the entered quantity is a positive integer.
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

### Python module 2:inventory_management/products.py
-	Import the pyodbc module for working with SQL Server databases.
-	Initialize the class with a connection to the database and a cursor for executing queries.
-	Define a method to create an empty dictionary for storing ProductIDs and ProductNames
-	Define a method to update the product_list dictionary with the latest data from the Products table
-	Define a static method to check if StockQuantity is an integer and greater than or equals to 0
-	Define a method to execute a query to fetch all data from the Products table and display it in a formatted table

-	Define a method to add a new unique ProductName and a matching unique ProductID to the Products table
-	Start an infinite loop for continuous input until a valid entry is provided
-	Prompt user to input the new ProductName
-	Check if new_product_name is empty or contains only whitespace characters
-	Check if the new ProductName already exists in the updated_product_list
-	Execute a SQL query to get the maximum ProductID from the Products table
-	Generate a new ProductID based on the current maximum ProductID
-	Execute a SQL query to insert the new product into the Products table
-	Commit the changes to the database
-	Update the product list with the new entry
-	Exit the loop after a successful entry
-	Handle exceptions related to invalid input (ValueError)

-	Define a method to change the name of an old ProductName in the Products table
-	Start an infinite loop for continuous input until a valid entry is provided
-	Prompt user to input the old ProductName to be changed
-	Check if old_product_name is not an existing ProductName in the updated_product_list
-	Continue looping until a valid new_product_name is provided
-	Prompt user to input the new ProductName
-	Check if new_product_name is empty or contains only whitespace characters
-	Check if new_product_name is an existing ProductName in the updated_product_list
-	Get the old ProductID based on the old ProductName
-	Execute a SQL query to update the old ProductName and StockQuantity in the Products table
-	Commit the changes to the database
-	Update the product list with the changes
-	Exit the loop after a successful entry
-	Exit the outer loop after a successful entry
-	Handle exceptions related to invalid input (ValueError)

-	Define a method to change only the StockQuantity of an old ProductName in the Products table
-	Define a method to delete a specified old ProductName and its corresponding ProductID and StockQuantity from the Products table
-	Define a method to run the main program loop, allowing the user to interact with the inventory management system

-	Define the connection string with details to connect to the SQL Server
-	Specify the connection string with details to connect to the SQL Server database
-	Create an instance of the InventoryManager class
-	Run the program using the instance



### Python module 3: inventory_management/suppliers.py
-	Define the InventoryManager class
-	Constructor: Initialize the class with a connection to the database and a cursor for executing queries
-	Define a method to create an empty dictionary for storing SupplierIDs and SupplierNames
-	Define a method to update the supplier_list dictionary with the latest data from the Suppliers table
-	Define a static method to check if ContactInfo is a non-empty string
-	Define a method to execute a query to fetch all data from the Suppliers table and display it in a formatted table
-	Define a method to add a new unique SupplierName and a matching unique SupplierID to the Suppliers table
-	Prompt user to input the new new_supplier_name
-	Check if new_supplier_name is empty or contains only whitespace characters
-	Check if the new_supplier_name already exists in the updated_supplier_list
-	Execute a SQL query to get the maximum SupplierID from the Suppliers table
-	Handle exceptions related to invalid input (ValueError)

-  Define a method to change the name of an old SupplierName in the Suppliers table
-  Start an infinite loop for continuous input until a valid entry is provided
-  Prompt user to input the old SupplierName to be changed
-  Check if old_supplier_name is not an existing SupplierName in the updated_supplier_list
-  Continue looping until a valid new_supplier_name is provided
-  Prompt user to input the new SupplierName
-  Check if new_supplier_name is empty or contains only whitespace characters
-  Check if new_supplier_name is an existing SupplierName in the updated_supplier_list
-  Get the old SupplierID based on the old SupplierName
-  Execute a SQL query to update the old SupplierName and ContactInfo in the Suppliers table
-  Commit the changes to the database
-  Update the supplier list with the changes
-  Exit the loop after a successful entry
-  Exit the outer loop after a successful entry
-  Handle exceptions related to invalid input (ValueError)
-  Define a method to change only the ContactInfo of an old SupplierName in the Suppliers table

-  Define a method to delete a specified old SupplierName and its corresponding SupplierID and ContactInfo from the Suppliers table

-  Define a method to run the main program loop, allowing the user to interact with the inventory management system

-  Define the connection string with details to connect to the SQL Server
-  Specify the connection string with details to connect to the SQL Server database
-  Create an instance of the InventoryManager class
-  Run the program using the instance







### Python module 4:	__innit__.py






