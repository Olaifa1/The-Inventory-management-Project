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

-- Create SupplyTransactions Table
CREATE TABLE Supply_Transactions (
    TransactionID INT PRIMARY KEY,
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    SupplierID INT FOREIGN KEY REFERENCES Suppliers(SupplierID),
    ProductName VARCHAR(255) NOT NULL,
	SupplierName VARCHAR(255) NOT NULL,
	TransactionType VARCHAR(3) CHECK (TransactionType IN ('In', 'Out')),
    Quantity INT NOT NULL,
    TransactionDate DATETIME -- Change the data type to DATETIME
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

SELECT *
FROM Suppliers


SELECT *
FROM Supply_Transactions