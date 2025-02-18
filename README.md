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



1. Supply_Transactions.py
📌 Purpose: Manages inventory supply transactions, allowing users to record purchases from suppliers.

🛠 Key Functionalities:
✅ Display all supply transactions from the database.
✅ Add a new supply transaction (records new product supply from a supplier).
✅ Delete an existing transaction by Transaction ID.
✅ Validate supplier and product names before adding a transaction.
✅ Generate unique transaction IDs.
✅ Ensure email and phone number formats are correct.
✅ Maintain a structured output table format for clarity.

2. Products.py
📌 Purpose: Manages all product-related operations in the inventory system.

🛠 Key Functionalities:
✅ Display all products in the inventory.
✅ Search for a product by Product Name or Product ID and display all matching records.
✅ Validate product name format before processing.
✅ Keep data structured and well-formatted for easy reading.
✅ Prevents incorrect or empty input values.

3. Customers.py
📌 Purpose: Manages customer-related data in the inventory system.

🛠 Key Functionalities:
✅ Display all customers in the database.
✅ Search for customers using any column (Customer Name, Customer ID, Gender, Age, Country, State, County, Email, or Phone Number).
✅ Ensures email and phone number formats are correct.
✅ Validates numeric fields (like Customer ID and Age) to prevent incorrect input.
✅ Maintains a structured table output for readability.

4. Suppliers.py
📌 Purpose: Manages supplier details, ensuring businesses can track their sources of stock.

🛠 Key Functionalities:
✅ Display all suppliers in the database.
✅ Search for suppliers using any column (Supplier Name, Supplier ID, Address, Email, or Phone Number).
✅ Validates supplier information before adding to the database.
✅ Ensures a consistent table format for displaying supplier details.

How Do These Files Work Together?
Supply_Transactions.py relies on Products.py and Suppliers.py to check product availability and supplier information before recording transactions.
Customers.py helps in identifying which customers are interacting with the inventory system.
The app ensures that data is validated, well-structured, and easy to manage across all tables in the database.





