import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Connect to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="labdatabase"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Create tables without foreign key constraints
def create_tables(connection):
    cursor = connection.cursor()
    create_table_queries = """
CREATE TABLE IF NOT EXISTS ProductCategory (
            ProductCategoryID INT PRIMARY KEY,
            CategoryType VARCHAR(255)
        );

		CREATE TABLE Owner (
			OwnerID INT PRIMARY KEY,
			OwnerName VARCHAR(255),
			ProductID INT  -- this should be present to avoid the "Unknown column" error
);

        CREATE TABLE IF NOT EXISTS Product (
            ProductID INT PRIMARY KEY,
            ProductName VARCHAR(255),
            ProductDescription VARCHAR(255),
            Total INT,
            Stock INT,
            ProductCategoryID INT,
            OwnerID INT,
            ListedDate DATE,
            AvgRating FLOAT
        );

        CREATE TABLE IF NOT EXISTS ProductCopy (
            ProductCopyID INT PRIMARY KEY,
            ProductID INT,
            Price FLOAT
        );

        CREATE TABLE IF NOT EXISTS User (
            UserID INT PRIMARY KEY,
            Username VARCHAR(255),
            Email VARCHAR(255),
            Password VARCHAR(255),
            DateJoined DATE,
            Role VARCHAR(255)
        );

        CREATE TABLE IF NOT EXISTS Comment (
            CommentID INT PRIMARY KEY,
            Comment TEXT,
            ProductID INT,
            UserID INT,
            PublishDate DATE,
            Rating FLOAT
        );

        CREATE TABLE IF NOT EXISTS ShoppingCart (
            CartID INT PRIMARY KEY,
            UserID INT,
            CreationDate DATE
        );

        CREATE TABLE IF NOT EXISTS CartItem (
            CartItemID INT PRIMARY KEY,
            CartID INT,
            DateAdded TIMESTAMP,
            Quantity INT,
            ProductCopyID INT
        );

        CREATE TABLE IF NOT EXISTS `Order` (
            OrderID INT PRIMARY KEY,
            UserID INT,
            Total FLOAT,
            Status VARCHAR(255),
            PaymentID INT,
            OrderDate DATE,
            AddressID INT
        );

        CREATE TABLE IF NOT EXISTS OrderItems (
            OrderItemsID INT PRIMARY KEY,
            ProductCopyID INT,
            OrderID INT,
            Quantity INT
        );

        CREATE TABLE IF NOT EXISTS PaymentMethod (
            PaymentID INT PRIMARY KEY,
            UserID INT,
            PaymentType VARCHAR(255),
            Company VARCHAR(255),
            CardNumber BIGINT,
            ExpDate DATE,
            IsMain BOOLEAN
        );

        CREATE TABLE IF NOT EXISTS Address (
            AddressID INT PRIMARY KEY,
            Street VARCHAR(255),
            AddressLine VARCHAR(255),
            City VARCHAR(255),
            CountryID INT
        );

        CREATE TABLE IF NOT EXISTS UserAddress (
            UserID INT,
            AddressID INT,
            PRIMARY KEY (UserID, AddressID)
        );

        CREATE TABLE IF NOT EXISTS Country (
            CountryID INT PRIMARY KEY,
            CountryName VARCHAR(255));
    """
    connection.commit()

def insert_data(connection):
    cursor = connection.cursor()

connection = create_connection()
if connection:
    create_tables(connection)
    insert_data(connection)
    connection.close()
    print("Data inserted and database connection closed.")
