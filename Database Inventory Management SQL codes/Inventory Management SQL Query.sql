-- Create Database
CREATE DATABASE InventoryManagement;

-- Use the Database
USE InventoryManagement;

select *
from INFORMATION_SCHEMA.TABLES

-- Create Products Table
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    StockQuantity INT NOT NULL CHECK (StockQuantity > 0)
);

-- Create Suppliers Table
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY,
    SupplierName VARCHAR(255) NOT NULL,
    Address VARCHAR(255) NOT NULL,
	Email VARCHAR(255) NOT NULL,
	PhoneNumber bigint NOT NULL
);

-- Create SupplyTransactions Table
CREATE TABLE Supply_Transactions (
    TransactionID INT PRIMARY KEY,
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    SupplierID INT FOREIGN KEY REFERENCES Suppliers(SupplierID),
    ProductName VARCHAR(255) NOT NULL,
	SupplierName VARCHAR(255) NOT NULL,
	Address VARCHAR(255) NOT NULL,
	Email VARCHAR(255) NOT NULL,
	PhoneNumber bigint NOT NULL,
    Quantity INT NOT NULL,
	Cost_Price INT NOT NULL,
    TransactionDate DATETIME 
);



-- Example Trigger for updating StockQuantity in Products table after each Supply_Transactions
CREATE TRIGGER UpdateStock
ON Supply_Transactions
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE Products
    SET StockQuantity = StockQuantity + I.Quantity
    FROM Products
    INNER JOIN INSERTED AS I ON Products.ProductID = I.ProductID;
END;


-- Trigger for updating StockQuantity in Products table after each deletion in Supply_Transactions
CREATE TRIGGER DeleteUpdateStock
ON Supply_Transactions
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE Products
    SET StockQuantity = StockQuantity - D.Quantity
    FROM Products
    INNER JOIN DELETED AS D ON Products.ProductID = D.ProductID;
END;


-- Create Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(255) NOT NULL,
	Gender VARCHAR(25) NOT NULL,
	Age INT NOT NULL,
	Country VARCHAR(255) NOT NULL,
	State VARCHAR(255) NOT NULL,
	County VARCHAR(255) NOT NULL, 
    Email VARCHAR(255) NOT NULL,
	PhoneNumber bigint NOT NULL
);

-- Create SalesTransactions Table
CREATE TABLE Sales_Transactions (
    TransactionID INT PRIMARY KEY,
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
    ProductName VARCHAR(255) NOT NULL,
	CustomerName VARCHAR(255) NOT NULL,
	Gender VARCHAR(25) NOT NULL,
	Age INT NOT NULL,
	Country VARCHAR(255) NOT NULL,
	State VARCHAR(255) NOT NULL,
	County VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
	PhoneNumber bigint NOT NULL,
    Quantity INT NOT NULL,
	Selling_Price INT NOT NULL,
    TransactionDate DATETIME NOT NULL
);

-- Example Trigger for updating StockQuantity in Products table after each Sales_Transactions
CREATE TRIGGER UpdateStock
ON Sales_Transactions
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE Products
    SET StockQuantity = StockQuantity - I.Quantity
    FROM Products
    INNER JOIN INSERTED AS I ON Products.ProductID = I.ProductID;
END;


-- Trigger for updating StockQuantity in Products table after each deletion in Sales_Transactions
CREATE TRIGGER DeleteSalesTransactionStock
ON Sales_Transactions
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE Products
    SET StockQuantity = StockQuantity - D.Quantity
    FROM Products
    INNER JOIN DELETED AS D ON Products.ProductID = D.ProductID;
END;

-- Generate stock report
SELECT ProductID, ProductName, StockQuantity
FROM Products;

SELECT *
FROM Suppliers

SELECT *
FROM Supply_Transactions


SELECT *
FROM Customers

SELECT *
FROM Sales_Transactions