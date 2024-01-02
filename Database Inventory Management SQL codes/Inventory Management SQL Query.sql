-- Create Database
CREATE DATABASE InventoryManagement;

-- Use the Database
USE InventoryManagement;

-- Create Products Table
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    StockQuantity INT NOT NULL CHECK (StockQuantity >= 0)
);

-- Create Suppliers Table
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY,
    SupplierName VARCHAR(255) NOT NULL,
    ContactInfo VARCHAR(255)
);

-- Create Transactions Table
CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    SupplierID INT FOREIGN KEY REFERENCES Suppliers(SupplierID),
    TransactionType VARCHAR(3) CHECK (TransactionType IN ('In', 'Out')),
    Quantity INT NOT NULL,
    TransactionDate DATE
);


-- Example Trigger for updating StockQuantity in Products table after each transaction
CREATE TRIGGER UpdateStock
ON Transactions
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE Products
    SET StockQuantity = StockQuantity + I.Quantity
    FROM Products
    INNER JOIN INSERTED AS I ON Products.ProductID = I.ProductID;
END;


-- Add new product
INSERT INTO Products (ProductID, ProductName, StockQuantity)
VALUES (1, 'ProductA', 100);

-- Update stock level
UPDATE Products
SET StockQuantity = StockQuantity + 50
WHERE ProductID = 1;

-- Generate stock report
SELECT ProductID, ProductName, StockQuantity
FROM Products;
